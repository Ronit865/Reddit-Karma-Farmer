# 🚀 How to Run Reddit Karma Farmer

## Option 1: Quick Start (Batch File) ⚡

**The Easiest Way - Just Double Click!**

1. Double-click `Start_Reddit_Bot.bat`
2. The GUI window will open automatically
3. Configure your settings and click "▶ Start Bot"

That's it! 🎉

---

## Option 2: Create Windows Executable (.exe) 📦

Want a standalone app you can run anywhere? Follow these steps:

### Step 1: Install PyInstaller
```powershell
pip install pyinstaller
```

### Step 2: Build the Executable
```powershell
python build_exe.py
```

### Step 3: Find Your App
- Look in the `dist` folder
- You'll find `RedditKarmaFarmer.exe`
- Double-click to run!

### Step 4: (Optional) Create Desktop Shortcut
1. Right-click `RedditKarmaFarmer.exe`
2. Click "Send to" → "Desktop (create shortcut)"
3. Now you can launch from your desktop! 🖥️

**Note:** Keep the `.env` file in the same folder as the .exe

---

## Option 3: Run Directly with Python 🐍

If you prefer the command line:

```powershell
python reddit_bot_gui.py
```

---

## 🎯 Using the GUI

1. **Select Categories** - Check boxes for the subreddit types you want
2. **Configure Settings**:
   - Language (auto/english/hinglish)
   - Daily comment limit
   - Minimum upvotes/comments for posts
3. **Click "▶ Start Bot"** - Watch it work in real-time!
4. **Click "⏹ Stop Bot"** - Stop whenever you want

---

## ⚙️ Configuration

Make sure your `.env` file contains:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
OPENAI_API_KEY=your_openai_key
```

---

## 📝 Default Settings

- **Categories**: Memes & Humor, Indian Memes (pre-selected)
- **Language**: Auto-detect
- **Daily Limit**: 50 comments
- **Min Upvotes**: 100
- **Min Comments**: 10

Customize everything in the GUI! 🎨

---

## 🆘 Troubleshooting

**GUI won't open?**
- Make sure Python is installed
- Run: `pip install -r requirements.txt`

**Bot won't start?**
- Check your `.env` file credentials
- Verify Reddit API access

**Need help?**
- Check the status log in the GUI for error messages
