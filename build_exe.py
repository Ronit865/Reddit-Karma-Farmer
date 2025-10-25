# Build script to create standalone Windows executable
# Run this to create RedditKarmaFarmer.exe

import PyInstaller.__main__
import os

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'reddit_bot_gui_redesigned.py',
    '--onefile',                    # Create single executable
    '--windowed',                   # No console window
    '--name=RedditKarmaFarmer',    # Name of the executable
    '--icon=NONE',                  # Add icon if you have one
    '--add-data=.env;.',           # Include .env file
    '--hidden-import=praw',
    '--hidden-import=openai',
    '--hidden-import=fake_useragent',
    '--hidden-import=dotenv',
    '--clean',                      # Clean build cache
])

print("\n" + "="*50)
print("✅ Build Complete!")
print("="*50)
print(f"\nYour executable is located at:")
print(f"  {os.path.join(current_dir, 'dist', 'RedditKarmaFarmer.exe')}")
print("\nYou can now:")
print("  1. Double-click RedditKarmaFarmer.exe to run")
print("  2. Create a desktop shortcut")
print("  3. Share the .exe file (with .env file)")
print("="*50)
