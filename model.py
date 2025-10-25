from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_comment(
    post_title: str, post_text: str, comments: list[tuple[str, int]], language: str = "auto"
) -> str:
    """
    Generates a high-quality comment for a Reddit post using Groq's API with Llama model.

    :param post_title: The title of the Reddit post.
    :param post_text: The text content of the Reddit post.
    :param comments: A list of tuples containing the comment content and upvotes.
    :param language: Language for the comment ('hinglish', 'english', or 'auto' to match post)
    :return: The generated comment for the post.
    """

    comments = sorted(comments, key=lambda comment: comment[1], reverse=True)
    
    # Get top 6-8 comments for deeper analysis (if available)
    if len(comments) >= 8:
        comments = comments[:8]
    elif len(comments) >= 6:
        comments = comments[:6]
    else:
        comments = comments[: len(comments)]
    
    # Format comments with their scores to show what gets upvoted
    formatted_comments = []
    for comment_text, score in comments:
        # Truncate very long comments for context
        if len(comment_text) > 200:
            comment_text = comment_text[:200] + "..."
        formatted_comments.append(f"[{score}↑] {comment_text}")
    comments_str = "\n".join(formatted_comments)

    # Determine language instruction
    if language == "hinglish":
        lang_instruction = "IMPORTANT: Generate your comment in HINGLISH - Hindi words written in English/Roman script mixed with English (like 'bahut accha hai bro', 'bilkul sahi point', 'yeh to kamaal hai yaar', 'ekdum mast', 'arrey bhai bhai', 'lmao yaar'). Use casual Indian English mixed with Hindi words in Roman letters. This is the natural way Indians communicate online. "
    elif language == "english":
        lang_instruction = "IMPORTANT: Generate your comment in ENGLISH only. Use clear, natural English with good grammar and internet slang. "
    else:  # auto
        lang_instruction = "IMPORTANT: Detect the language and style of the post and top comments. If they use Hinglish (Hindi words in English letters mixed with English), respond in Hinglish. If they use English, respond in English. Match their communication style naturally. "

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Fast and smart Groq model
        messages=[
            {
                "role": "system",
                "content": f"You are a Reddit expert who writes comments that get MAXIMUM UPVOTES across ANY type of post. {lang_instruction}\n\n🎯 UPVOTE-WINNING STRATEGIES (adapt based on post type):\n\n📸 For Images/Pics/Memes:\n✅ Funny observations: 'This is so accurate it hurts 😭'\n✅ Relatable reactions: 'I'm in this picture and I don't like it'\n✅ Build on the joke: 'And then proceeds to [funny next step]'\n✅ Perfect timing: 'This hit different 💀'\n\n❓ For AskReddit/Questions:\n✅ Personal stories (short): 'This happened to me once...'\n✅ Unexpected twists: 'Plot twist: [surprising perspective]'\n✅ Witty answers: Clever, concise responses\n✅ Relatable: 'We've all been there'\n\n📚 For TIL/Facts/News:\n✅ Add context: 'Fun fact: [related info]'\n✅ Personal connection: 'I actually experienced this...'\n✅ Smart observation: 'This explains why...'\n✅ Question that adds value: 'Does this mean...?'\n\n🎮 For Gaming/Tech/Specific Topics:\n✅ Share experience: 'I remember when...'\n✅ Technical insight: 'Actually, [interesting detail]'\n✅ Community jokes: Reference shared experiences\n✅ Helpful additions: Useful info briefly\n\n🔥 UNIVERSAL UPVOTE RULES:\n✅ SHORT (1-2 sentences max)\n✅ NATURAL emojis (😂 💀 🔥 😭 only if they fit)\n✅ Match the VIBE of top comments\n✅ Add VALUE (humor, insight, or relatability)\n✅ AUTHENTIC tone (like a real person)\n✅ Timing matters - quick wit wins\n\n❌ AVOID:\n❌ Generic ('nice', 'cool', 'this')\n❌ Too long/preachy\n❌ Trying too hard\n❌ Being negative/mean\n❌ Repeating others\n\n💡 ANALYZE the top comments to understand WHAT WORKS for THIS specific post, then create something similar but unique!",
            },
            {
                "role": "user",
                "content": f"POST TYPE: Analyze and adapt your style\n\nTitle: {post_title}\n\nContent: {post_text}\n\nTOP COMMENTS WITH UPVOTES:\n{comments_str}\n\n🎯 TASK: Analyze these top comments to understand:\n1. What style/tone is getting upvoted here?\n2. Is this funny, serious, informative, or emotional?\n3. What type of responses work best?\n\nThen write ONE comment (1-2 sentences) that will get upvotes. Match the proven style. Add value. Be natural. Output ONLY the comment text.",
            },
        ],
        temperature=0.85,  # Balanced creativity
        max_tokens=100,  # Allow slightly longer for non-meme posts
        top_p=0.9,  # Quality control
    )

    response = response.choices[0].message.content
    response = response.split("#")[0].replace('"', "").strip()

    return response
