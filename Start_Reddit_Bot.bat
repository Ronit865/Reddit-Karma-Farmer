@echo off
title Reddit Karma Farmer
echo.
echo ========================================
echo    Reddit Karma Farmer Launcher
echo ========================================
echo.
echo Starting GUI...
echo.

python reddit_bot_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start the application!
    echo Make sure Python is installed and all dependencies are available.
    echo.
    pause
)
