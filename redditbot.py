"""
Reddit bot implementation used by the GUI.

Requirements (install in your Python env if missing):
  pip install praw python-dotenv groq

Environment variables expected (loaded by the GUI via .env):
  - REDDIT_CLIENT_ID
  - REDDIT_CLIENT_SECRET
  - REDDIT_USERNAME
  - REDDIT_PASSWORD
  - GROQ_API_KEY (for AI comment generation in model.py)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Iterable, List, Tuple, Any
import sys
import traceback

# Import model locally; this file is placed in the same folder
import model  # type: ignore


@dataclass
class BotConfig:
    client_id: str
    client_secret: str
    username: str
    password: str
    target_subreddits: List[str]
    language: str = "auto"
    daily_limit: int = 50
    min_upvotes: int = 100
    min_comments: int = 10
    upvote_mode: bool = False


class RedditBot:
    """Minimal Reddit bot that the GUI expects.

    Exposes methods:
      - get_trending_topics() -> iterable of submissions
      - extract_text_title(submission) -> str
      - extract_text_content(submission) -> str
      - extract_comment_content_and_upvotes(submission) -> list[(str, int)]
      - generate_comment(submission, title, content, comments) -> None

    Attributes used by GUI:
      - daily_limit (int)
      - comments_today (int)
    """

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        target_subreddits: List[str],
        language: str = "auto",
        daily_limit: int = 50,
        min_upvotes: int = 100,
        min_comments: int = 10,
        upvote_mode: bool = False,
    ) -> None:
        # Lazy import to avoid ImportError during mere import of this module
        try:
            import praw  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "Missing dependency 'praw'. Install it with: pip install praw"
            ) from e

        import praw  # type: ignore  # re-import for typing/context

        self._praw = praw
        self.config = BotConfig(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            target_subreddits=list(dict.fromkeys([s.strip() for s in target_subreddits if s.strip()])),
            language=language,
            daily_limit=int(daily_limit),
            min_upvotes=int(min_upvotes),
            min_comments=int(min_comments),
            upvote_mode=bool(upvote_mode),
        )

        # Public attributes expected by GUI
        self.daily_limit = self.config.daily_limit
        self.comments_today = 0

        # Track reset per new day
        self._last_comment_day: date | None = None

        # Create Reddit client
        self.reddit = self._praw.Reddit(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            username=self.config.username,
            password=self.config.password,
            user_agent="RedditKarmaFarmer/1.0 (+https://github.com/)",
        )

        print("✅ Reddit client initialized")

    # ---- Helpers ----
    def _reset_counter_if_new_day(self) -> None:
        today = datetime.utcnow().date()
        if self._last_comment_day is None or self._last_comment_day != today:
            self.comments_today = 0
            self._last_comment_day = today

    # ---- Public API used by GUI ----
    def _calculate_upvote_potential(self, submission: Any) -> float:
        """Calculate a score for how likely comments are to get upvotes on this post.
        
        Fast calculation using only metadata - no comment fetching to avoid freezing.
        
        Factors considered:
        - Post score (higher = more visibility)
        - Comment count (more comments = active discussion)
        - Comment-to-upvote ratio
        - Recency (fresher posts = better chance)
        """
        try:
            # Gather basic metrics (fast - no API calls)
            post_score = max(getattr(submission, "score", 0), 1)
            num_comments = max(getattr(submission, "num_comments", 0), 1)
            
            # Engagement ratio: comments per upvote (higher = more active discussion)
            engagement_ratio = num_comments / post_score
            
            # Comment activity score (more comments = better, but diminishing returns)
            comment_activity = min(num_comments / 50.0, 2.0)  # Cap at 2x bonus
            
            # Recency bonus (posts created in last 4 hours get bonus)
            created_utc = getattr(submission, "created_utc", 0)
            hours_old = (datetime.utcnow().timestamp() - created_utc) / 3600
            recency_bonus = max(0, 1.5 - (hours_old / 4.0))  # Linear decay over 4 hours
            
            # Post popularity (higher score = more visibility for comments)
            popularity_score = min(post_score / 1000.0, 5.0)  # Cap at 5x
            
            # Combine factors (weighted for fast sorting)
            potential_score = (
                popularity_score * 30 +              # Post visibility (30%)
                comment_activity * 30 +              # Activity level (30%)
                engagement_ratio * 100 * 20 +        # Engagement rate (20%)
                recency_bonus * 20                   # Recency advantage (20%)
            )
            
            return potential_score
            
        except Exception as e:
            print(f"⚠️ Failed to calculate upvote potential: {e}")
            return 0.0
    
    def get_trending_topics(self) -> Iterable[Any]:
        """Yield submissions from target subreddits meeting thresholds.

        Strategy: grab hot posts from each subreddit, filter by score and
        comment count, ignore stickied posts. If upvote_mode is enabled,
        sort by upvote potential.
        """
        seen_ids = set()
        submissions_list = []
        
        for sub_name in self.config.target_subreddits:
            try:
                subreddit = self.reddit.subreddit(sub_name)
                # Fetch a reasonable number to filter; GUI handles pacing
                for submission in subreddit.hot(limit=25):
                    if getattr(submission, "stickied", False):
                        continue
                    if submission.id in seen_ids:
                        continue
                    if getattr(submission, "score", 0) < self.config.min_upvotes:
                        continue
                    if getattr(submission, "num_comments", 0) < self.config.min_comments:
                        continue

                    seen_ids.add(submission.id)
                    submissions_list.append(submission)

            except Exception as e:
                print(f"⚠️ Failed to fetch from r/{sub_name}: {e}")
                continue
        
        # If upvote mode is enabled, sort by upvote potential
        if self.config.upvote_mode and submissions_list:
            print("🔥 Upvote Mode: Analyzing posts for comment upvote potential...")
            
            # Calculate scores for all submissions (fast - no API calls)
            scored_submissions = []
            for idx, submission in enumerate(submissions_list):
                score = self._calculate_upvote_potential(submission)
                scored_submissions.append((submission, score))
                
                # Progress indicator every 10 posts
                if (idx + 1) % 10 == 0:
                    print(f"  📊 Analyzed {idx + 1}/{len(submissions_list)} posts...")
            
            # Sort by potential score (highest first)
            scored_submissions.sort(key=lambda x: x[1], reverse=True)
            
            # Log top candidates
            print(f"✅ Sorted {len(scored_submissions)} posts by upvote potential")
            print(f"📊 Top 5 candidates:")
            for i, (sub, score) in enumerate(scored_submissions[:5], 1):
                title = getattr(sub, "title", "")[:60]
                subreddit = getattr(sub, 'subreddit', 'unknown')
                comments = getattr(sub, 'num_comments', 0)
                upvotes = getattr(sub, 'score', 0)
                print(f"  {i}. [{score:.1f}] {title}... (r/{subreddit} | ⬆️{upvotes} 💬{comments})")
            print("")
            
            # Yield sorted submissions
            for submission, score in scored_submissions:
                yield submission
        else:
            # Normal mode: yield as-is
            for submission in submissions_list:
                yield submission

    def extract_text_title(self, submission: Any) -> str:
        return getattr(submission, "title", "").strip()

    def extract_text_content(self, submission: Any) -> str:
        # For text posts
        if getattr(submission, "is_self", False):
            return (getattr(submission, "selftext", "") or "").strip()

        # For link/image/video posts: provide minimal context string
        url = getattr(submission, "url", "")
        # Some subs use gallery; we still return URL as context
        return f"[Link Post] {url}".strip()

    def extract_comment_content_and_upvotes(self, submission: Any) -> List[Tuple[str, int]]:
        try:
            # Replace MoreComments to get a clean list of top-level comments
            submission.comments.replace_more(limit=0)
            comments = []
            for c in submission.comments[:20]:  # top 20
                body = getattr(c, "body", "").strip()
                score = int(getattr(c, "score", 0))
                if body:
                    comments.append((body, score))
            # Sort by score descending
            comments.sort(key=lambda x: x[1], reverse=True)
            # Return top N for model
            return comments[:10]
        except Exception as e:
            print(f"⚠️ Failed to read comments: {e}")
            return []

    def generate_comment(
        self,
        submission: Any,
        title: str,
        content: str,
        comments: List[Tuple[str, int]],
    ) -> None:
        """Generate and post a comment to a submission.

        Uses Groq (via model.py) to craft the text, honors daily limit,
        and handles common API errors gracefully.
        """
        self._reset_counter_if_new_day()
        if self.comments_today >= self.daily_limit:
            print("⚠️ Daily limit reached, skipping further comments.")
            return

        try:
            # Generate comment text using AI model
            text = model.generate_comment(
                post_title=title,
                post_text=content,
                comments=comments,
                language=self.config.language,
            )

            if not text or len(text.strip()) == 0:
                print("⚠️ Model returned empty comment, skipping.")
                return

            # Post the comment
            reply = submission.reply(text)
            self.comments_today += 1
            link = f"https://reddit.com{getattr(reply, 'permalink', '')}" if reply else ""
            print(f"✅ Comment posted ({self.comments_today}/{self.daily_limit}) → {link}")

        except Exception as e:
            # Try to surface useful error info
            err = f"❌ Failed to comment: {e}"
            print(err)
            traceback.print_exc(file=sys.stdout)
