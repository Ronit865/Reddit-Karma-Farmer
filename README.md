# ⚡ Reddit Karma Farmer

<div align="center">

![Reddit Karma Farmer](https://img.shields.io/badge/Reddit-Karma%20Farmer-FF4500?style=for-the-badge&logo=reddit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![AI Powered](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)

**An intelligent Reddit bot with a modern GUI that uses AI to automatically post engaging comments on trending posts**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Configuration](#️-configuration) • [How It Works](#-how-it-works)

</div>

---

## 📸 Screenshot

![Reddit Karma Farmer GUI](https://github.com/Valkam-Git/Reddit-Karma-Farmer/assets/82890199/bd915d5c-a861-462a-a23f-5c5cd38b39e1)

*Results after running the bot for a few hours*

---

## ✨ Features

### 🎯 **Intelligent Comment Generation**
- **AI-Powered**: Uses Groq's Llama 3.3 70B model for natural, engaging comments
- **Context-Aware**: Analyzes post title, content, and top comments for relevant responses
- **Upvote Mode**: Smart algorithm prioritizes posts where comments get the most upvotes
- **Multi-Language**: Supports Auto-detect, English, and Hinglish

### 🎨 **Modern GUI Interface**
- Beautiful gradient-based dark theme
- Real-time activity monitoring
- Live statistics dashboard
- Fullscreen mode support (F11)
- Easy category selection

### 🔥 **Special Modes**
- **Meme Mode** (😂): Exclusively targets r/meme and r/funny with upvote optimization
- **Upvote Mode** (🔥): Prioritizes posts with high engagement potential
- **Smart Filtering**: Customizable upvote/comment thresholds

### 🛡️ **Safe & Configurable**
- Daily comment limits to avoid spam detection
- Customizable delays between comments (60-240s default)
- Post quality filters (minimum upvotes/comments)
- Session tracking and statistics

### 🎯 **Target Multiple Categories**
- 🎭 Memes & Humor
- 🇮🇳 Indian Memes  
- 🎮 Gaming
- 💬 Casual Talk
- 🎬 Entertainment
- 📰 News & Events
- ⚽ Sports

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Reddit Account
- Reddit API Credentials ([Get them here](https://www.reddit.com/prefs/apps))
- Groq API Key ([Get free key](https://console.groq.com))

### Step 1: Clone the Repository
```bash
git clone https://github.com/Ronit865/Reddit-Karma-Farmer.git
cd Reddit-Karma-Farmer
```

### Step 2: Install Dependencies
```bash
pip install praw python-dotenv groq
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Reddit API Credentials
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password

# AI Model API Key
GROQ_API_KEY=your_groq_api_key_here
```

#### 📝 Getting Reddit API Credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the form:
   - **name**: Reddit Karma Farmer (or any name)
   - **redirect uri**: http://localhost:8080
5. Copy your **client ID** (under the app name) and **client secret**

#### 🤖 Getting Groq API Key:
1. Visit https://console.groq.com
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

---

## ⚡ Quick Start

### Method 1: Double-Click to Run (Easiest)
```bash
# Windows
Start_Reddit_Bot.bat

# The GUI will launch automatically!
```

### Method 2: Run with Python
```bash
python reddit_bot_gui_redesigned.py
```

### Method 3: Build Standalone Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
python build_exe.py

# Find your exe in the dist/ folder
# dist/RedditKarmaFarmer.exe
```

---

## 🎮 Using the GUI

### 1️⃣ **Select Target Categories**
- Check the boxes for subreddit categories you want to target
- Or use **Meme Mode** for exclusive meme subreddit targeting

### 2️⃣ **Configure Settings** (⚙️ button)
- **Daily Limit**: Max comments per day (default: 50)
- **Delays**: Time between comments (60-240s)
- **Filters**: Minimum upvotes/comments on posts
- **Language**: Auto/English/Hinglish
- **Upvote Mode**: Enable smart post selection

### 3️⃣ **Start the Bot**
- Click "▶ START AUTOMATION"
- Watch real-time activity in the monitor
- Stats update automatically

### 4️⃣ **Monitor & Control**
- View live statistics (comments, karma, subreddits)
- Check activity logs with color-coded messages
- Stop anytime with "⏹ STOP AUTOMATION"

---

## ⚙️ Configuration

### Default Settings
```python
Daily Limit: 50 comments
Min Delay: 60 seconds
Max Delay: 240 seconds
Min Upvotes: 100
Min Comments: 10
Language: Auto-detect
Upvote Mode: Disabled
```

### Customization Options

#### In GUI Settings (⚙️):
- Adjust all timing and filtering parameters
- Change language preferences
- Toggle upvote mode
- Set comment limits

#### In Code (`redditbot.py`):
```python
bot = RedditBot(
    client_id="...",
    client_secret="...",
    username="...",
    password="...",
    target_subreddits=["memes", "funny"],
    language="auto",          # "auto", "english", "hinglish"
    daily_limit=50,
    min_upvotes=100,
    min_comments=10,
    upvote_mode=False
)
```

---

## 🤖 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                      │
│           (reddit_bot_gui_redesigned.py)                │
│  • Category Selection  • Settings  • Controls           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    Reddit Bot Core                      │
│                   (redditbot.py)                        │
│  • Fetch trending posts  • Filter by criteria           │
│  • Extract context  • Upvote mode ranking               │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  AI Comment Engine                      │
│                    (model.py)                           │
│  • Groq Llama 3.3 70B  • Context analysis               │
│  • Style matching  • Language adaptation                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    Reddit API                           │
│                     (PRAW)                              │
│  • Post comments  • Track karma  • Monitor posts        │
└─────────────────────────────────────────────────────────┘
```

### Workflow

1. **Fetch Posts**: Gets hot/trending posts from selected subreddits
2. **Filter**: Applies upvote/comment thresholds and removes stickied posts
3. **Upvote Mode** (if enabled): Ranks posts by engagement potential
4. **Extract Context**: Gathers post title, content, and top comments
5. **AI Generation**: Groq analyzes context and generates natural comment
6. **Post Comment**: Submits comment via Reddit API
7. **Track Stats**: Updates karma count and session statistics
8. **Cooldown**: Waits random delay (60-240s) before next comment

### AI Comment Strategy

The bot uses sophisticated prompts to:
- ✅ Analyze what gets upvoted on each specific post
- ✅ Match the tone and style of top comments
- ✅ Adapt to different post types (memes, questions, news, etc.)
- ✅ Keep comments short and natural (1-2 sentences)
- ✅ Add value through humor, insight, or relatability
- ✅ Use appropriate language (English/Hinglish)

---

## 📁 Project Structure

```
Reddit-Karma-Farmer/
├── reddit_bot_gui_redesigned.py   # Main GUI application
├── redditbot.py                    # Bot logic and Reddit API
├── model.py                        # AI comment generation
├── build_exe.py                    # Executable builder
├── Start_Reddit_Bot.bat            # Quick launch script
├── .env                            # Environment variables (you create)
├── commented_posts.txt             # Tracking file
├── LICENSE                         # MIT License
├── README.md                       # This file
├── HOW_TO_RUN.md                   # Detailed run instructions
└── UI_IMPROVEMENTS.md              # UI documentation
```

---

## 🔥 Advanced Features

### Upvote Mode Algorithm

When enabled, the bot calculates an "upvote potential score" for each post using:

```python
Factors:
- Post popularity (score/1000)
- Comment activity (num_comments/50)
- Engagement ratio (comments per upvote)
- Recency bonus (fresher posts prioritized)

Formula:
potential = (popularity × 30%) + (activity × 30%) 
          + (engagement × 20%) + (recency × 20%)
```

Posts are sorted by this score, ensuring you comment where engagement is highest.

### Meme Mode

Exclusively targets `r/meme` and `r/funny` with:
- Automatic upvote mode activation
- Optimized for humor-based comments
- Visual indicator in UI

---

## 🛡️ Safety & Best Practices

### Rate Limiting
- Default: 50 comments/day (configurable)
- Random delays: 60-240 seconds between comments
- Prevents Reddit spam detection

### Ethical Usage
⚠️ **Important**: This bot is for educational purposes. Please:
- ✅ Use responsibly and follow Reddit's ToS
- ✅ Don't spam or harass
- ✅ Respect subreddit rules
- ✅ Set reasonable daily limits
- ✅ Use quality filters to avoid low-effort posts

### Account Safety
- Use a dedicated account for botting
- Start with low daily limits (20-30)
- Monitor for shadowbans
- Avoid suspicious patterns

---

## � Troubleshooting

### GUI won't open
```bash
# Reinstall dependencies
pip install --upgrade praw python-dotenv groq tkinter
```

### "Missing credentials" error
- Check your `.env` file exists in the project root
- Verify all 5 variables are set (REDDIT_CLIENT_ID, etc.)
- No quotes needed in `.env` file

### Comments not posting
- Verify Reddit credentials are correct
- Check if account has sufficient karma (some subs require minimum)
- Look for error messages in activity log
- Ensure API rate limits aren't exceeded

### "Module not found" error
```bash
pip install praw python-dotenv groq
```

---

## 📊 Statistics & Monitoring

The GUI displays real-time stats:
- 💬 **Comments**: Total comments posted this session
- ⭐ **Karma**: Estimated karma earned
- 🎯 **Subreddits**: Number of targeted subreddits
- 📁 **Categories**: Active category count

Activity monitor shows:
- ✅ Success messages (green)
- ⚠️ Warnings (orange)
- ❌ Errors (red)
- ℹ️ Info (cyan)

---

## 🔧 Development

### Requirements
```txt
praw>=7.7.1
python-dotenv>=1.0.0
groq>=0.4.0
```

### Building from Source
```bash
# Clone repo
git clone https://github.com/Ronit865/Reddit-Karma-Farmer.git

# Install dependencies
pip install -r requirements.txt  # If available
# OR
pip install praw python-dotenv groq

# Run
python reddit_bot_gui_redesigned.py
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## � License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2023 Valkam
Modified by Ronit865
```

---

## 🙏 Acknowledgments

- Original concept by [Valkam](https://github.com/Valkam-Git)
- Enhanced and redesigned by [Ronit865](https://github.com/Ronit865)
- Powered by [Groq](https://groq.com) and [PRAW](https://praw.readthedocs.io)
- UI built with Python Tkinter

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. The developers are not responsible for:
- Violations of Reddit's Terms of Service
- Account bans or suspensions
- Misuse of the software
- Any consequences of using this bot

Use at your own risk and always follow platform guidelines.

---

## 📞 Support

Having issues? 
- 📖 Check [HOW_TO_RUN.md](HOW_TO_RUN.md) for detailed instructions
- 🐛 [Open an issue](https://github.com/Ronit865/Reddit-Karma-Farmer/issues)
- 💬 Review existing discussions

---

<div align="center">

**Made with ❤️ by Ronit**

⭐ Star this repo if you found it useful!

[Report Bug](https://github.com/Ronit865/Reddit-Karma-Farmer/issues) • [Request Feature](https://github.com/Ronit865/Reddit-Karma-Farmer/issues)

</div>
