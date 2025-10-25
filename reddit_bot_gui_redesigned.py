import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from dotenv import load_dotenv
from redditbot import RedditBot
import threading
import sys
from datetime import datetime
import json

load_dotenv()

# Vibrant Modern Color Scheme
THEME = {
    # Base Colors - More colorful gradients
    'bg_dark': '#0F172A',           # Dark slate blue
    'bg_medium': '#1E293B',         # Medium slate
    'bg_light': '#334155',          # Light slate
    'bg_card': '#1A2332',           # Card background with blue tint
    'bg_gradient_start': '#6366F1', # Indigo gradient
    'bg_gradient_end': '#8B5CF6',   # Purple gradient
    
    # Accent Colors - More vibrant
    'primary': '#3B82F6',           # Bright blue
    'secondary': '#8B5CF6',         # Vivid purple
    'accent': '#EC4899',            # Hot pink
    'highlight': '#F59E0B',         # Bright amber
    'success': '#10B981',           # Emerald green
    'warning': '#F59E0B',           # Amber
    'danger': '#EF4444',            # Bright red
    'cyan': '#06B6D4',              # Cyan
    'teal': '#14B8A6',              # Teal
    'lime': '#84CC16',              # Lime
    'orange': '#F97316',            # Orange
    'rose': '#F43F5E',              # Rose
    
    # Text Colors
    'text_primary': '#F1F5F9',      # Off-white
    'text_secondary': '#CBD5E1',    # Light gray
    'text_muted': '#94A3B8',        # Muted gray
    'text_dark': '#0F172A',         # Dark for badges
    'text_bright': '#FFFFFF',       # Pure white
}

class ModernButton(tk.Frame):
    """Custom modern button with hover effects"""
    def __init__(self, parent, text, command, bg_color, fg_color='#FFFFFF', 
                 hover_color=None, height=50, icon=""):
        super().__init__(parent, bg=parent['bg'])
        
        self.bg_color = bg_color
        self.hover_color = hover_color or bg_color
        self.command = command
        
        # Button container
        self.btn = tk.Frame(self, bg=bg_color, cursor='hand2')
        self.btn.pack(fill=tk.BOTH, expand=True)
        
        # Button content
        content = tk.Frame(self.btn, bg=bg_color)
        content.pack(expand=True)
        
        # Icon
        if icon:
            tk.Label(content, text=icon, bg=bg_color, fg=fg_color,
                    font=('Segoe UI Emoji', 14)).pack(side=tk.LEFT, padx=(0, 10))
        
        # Text
        self.label = tk.Label(content, text=text, bg=bg_color, fg=fg_color,
                             font=('Segoe UI', 11, 'bold'))
        self.label.pack(side=tk.LEFT)
        
        # Bind events
        self.btn.bind('<Button-1>', lambda e: command())
        self.label.bind('<Button-1>', lambda e: command())
        self.btn.bind('<Enter>', self.on_enter)
        self.btn.bind('<Leave>', self.on_leave)
        self.label.bind('<Enter>', self.on_enter)
        self.label.bind('<Leave>', self.on_leave)
        
        # Set height
        self.config(height=height)
        self.pack_propagate(False)
    
    def on_enter(self, e):
        self.btn.config(bg=self.hover_color)
        self.label.config(bg=self.hover_color)
        for widget in self.btn.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=self.hover_color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.hover_color)
    
    def on_leave(self, e):
        self.btn.config(bg=self.bg_color)
        self.label.config(bg=self.bg_color)
        for widget in self.btn.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=self.bg_color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.bg_color)

class GradientFrame(tk.Canvas):
    """Custom frame with gradient background"""
    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)
        
    def _draw_gradient(self, event=None):
        """Draw gradient background"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height
        
        # Parse colors
        r1, g1, b1 = self._hex_to_rgb(self._color1)
        r2, g2, b2 = self._hex_to_rgb(self._color2)
        
        # Create gradient
        for i in range(limit):
            ratio = i / limit
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.tag_lower("gradient")
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class BlurredFrame(tk.Frame):
    """Frame with blur/frosted glass effect using transparency and borders"""
    def __init__(self, parent, bg, blur_opacity=0.7, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        # Create layered effect for blur simulation
        # Outer border for glow
        self.configure(
            bg=bg,
            highlightthickness=2,
            highlightbackground=self._add_alpha(bg, 40),
            highlightcolor=self._add_alpha(bg, 60)
        )
        
        # Add inner shadow effect
        inner_frame = tk.Frame(self, bg=bg, highlightthickness=1,
                              highlightbackground=self._add_alpha(bg, 20))
        inner_frame.place(x=2, y=2, relwidth=1, relheight=1, width=-4, height=-4)
    
    def _add_alpha(self, hex_color, lighten_amount):
        """Lighten a color to simulate transparency"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + lighten_amount)
        g = min(255, g + lighten_amount)
        b = min(255, b + lighten_amount)
        return f'#{r:02x}{g:02x}{b:02x}'

class RedditBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reddit Karma Farmer By Ronit")
        self.root.geometry("1400x850")
        self.root.minsize(1200, 700)  # Set minimum window size
        
        # Create gradient background
        self.background = GradientFrame(
            self.root, 
            color1='#1a0b2e',  # Deep purple
            color2='#16213e',  # Dark blue
            highlightthickness=0
        )
        self.background.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Fullscreen support
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.is_fullscreen = False
        
        # State variables
        self.bot = None
        self.is_running = False
        self.is_meme_mode = False  # New: Track meme mode state
        self.stats = {
            'comments': 0,
            'karma': 0,
            'subreddits': 0,
            'categories': 0,
            'session_start': None
        }
        
        # Bot settings (default values)
        self.settings = {
            'daily_limit': 50,
            'min_delay': 60,
            'max_delay': 240,
            'min_upvotes': 100,
            'min_comments': 10,
            'language': 'auto',
            'upvote_mode': False  # New: prioritize posts where comments get most upvotes
        }
        
        # Subreddit categories with emojis - optimized for upvote mode
        self.categories = {
            "🎭 Memes & Humor": ["memes", "dankmemes", "me_irl", "wholesomememes", "AdviceAnimals", "funny", "facepalm", "HolUp", "cursedcomments", "technicallythetruth"],
            "🇮🇳 Indian Memes": ["IndianDankMemes", "Saimansays", "SamayRaina", "indiameme", "IndianMemeTemplates"],
            "🎮 Gaming": ["gaming", "pcmasterrace", "PS5", "leagueoflegends", "Minecraft", "FortniteCompetitive"],
            "💬 Casual Talk": ["CasualConversation", "AskReddit", "NoStupidQuestions", "TooAfraidToAsk", "DoesAnybodyElse"],
            "🎬 Entertainment": ["movies", "television", "netflix", "Marvel", "marvelstudios", "StarWars"],
            "📰 News & Events": ["worldnews", "news", "nottheonion", "offbeat"],
            "⚽ Sports": ["Cricket", "sports", "nba", "soccer", "formula1"]
        }
        
        # Define meme-only subreddits for Meme Mode
        self.meme_subreddits = [
            "meme", "funny"
        ]
        
        self.category_vars = {}
        
        # Build UI
        self.build_ui()
        self.update_stats_display()
        
    def build_ui(self):
        """Build the entire UI"""
        # Top bar
        self.create_top_bar()
        
        # Main content area - use gradient background color
        main = tk.Frame(self.root, bg='#16213e')
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 25))
        
        # Left panel (40%)
        left_panel = tk.Frame(main, bg='#16213e')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))
        
        # Right panel (60%)
        right_panel = tk.Frame(main, bg='#16213e')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(12, 0))
        
        # Left panel contents
        self.create_stats_panel(left_panel)
        self.create_category_selector(left_panel)
        
        # Right panel contents
        self.create_activity_monitor(right_panel)
        self.create_control_panel(right_panel)
    
    def create_top_bar(self):
        """Create sleek top navigation bar with gradient effect"""
        topbar = tk.Frame(self.root, bg=THEME['bg_gradient_start'], height=80)
        topbar.pack(fill=tk.X)
        topbar.pack_propagate(False)
        
        # Content container
        content = tk.Frame(topbar, bg=THEME['bg_gradient_start'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Left side - Branding
        left = tk.Frame(content, bg=THEME['bg_gradient_start'])
        left.pack(side=tk.LEFT)
        
        # Logo
        logo = tk.Label(left, text="⚡", bg=THEME['bg_gradient_start'], 
                       fg=THEME['warning'], font=('Segoe UI Emoji', 28))
        logo.pack(side=tk.LEFT, padx=(0, 15))
        
        # Title
        title_container = tk.Frame(left, bg=THEME['bg_gradient_start'])
        title_container.pack(side=tk.LEFT)
        
        tk.Label(title_container, text="REDDIT KARMA FARMER", 
                bg=THEME['bg_gradient_start'], fg=THEME['text_bright'],
                font=('Segoe UI', 18, 'bold')).pack(anchor='w')
        
        tk.Label(title_container, text="By Ronit • Intelligent Comment Automation", 
                bg=THEME['bg_gradient_start'], fg=THEME['text_secondary'],
                font=('Segoe UI', 9)).pack(anchor='w', pady=(3, 0))
        
        # Right side - Status indicator
        right = tk.Frame(content, bg=THEME['bg_gradient_start'])
        right.pack(side=tk.RIGHT)
        
        # Meme Mode button
        self.meme_mode_btn = tk.Label(right, text="😂 MEME", 
                                     bg=THEME['bg_light'], fg=THEME['text_bright'],
                                     font=('Segoe UI', 10, 'bold'),
                                     cursor='hand2', padx=15, pady=8)
        self.meme_mode_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.meme_mode_btn.bind('<Button-1>', lambda e: self.toggle_meme_mode())
        self.meme_mode_btn.bind('<Enter>', lambda e: self.meme_mode_btn.config(bg=THEME['accent']))
        self.meme_mode_btn.bind('<Leave>', lambda e: self.meme_mode_btn.config(
            bg=THEME['lime'] if self.is_meme_mode else THEME['bg_light']))
        
        # Upvote Mode toggle button
        self.upvote_toggle_btn = tk.Label(right, text="🔥 UPVOTE", 
                                         bg=THEME['bg_light'], fg=THEME['text_bright'],
                                         font=('Segoe UI', 10, 'bold'),
                                         cursor='hand2', padx=15, pady=8)
        self.upvote_toggle_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.upvote_toggle_btn.bind('<Button-1>', lambda e: self.toggle_upvote_mode())
        self.upvote_toggle_btn.bind('<Enter>', lambda e: self.upvote_toggle_btn.config(bg=THEME['accent']))
        self.upvote_toggle_btn.bind('<Leave>', lambda e: self.upvote_toggle_btn.config(
            bg=THEME['orange'] if self.settings.get('upvote_mode', False) else THEME['bg_light']))
        
        # Update button colors based on initial state
        if self.settings.get('upvote_mode', False):
            self.upvote_toggle_btn.config(bg=THEME['orange'])
        
        # Settings button
        settings_btn = tk.Label(right, text="⚙", bg=THEME['secondary'],
                               fg=THEME['text_bright'], font=('Segoe UI', 16),
                               cursor='hand2', padx=12, pady=8)
        settings_btn.pack(side=tk.LEFT, padx=(0, 10))
        settings_btn.bind('<Button-1>', lambda e: self.show_settings())
        settings_btn.bind('<Enter>', lambda e: settings_btn.config(bg=THEME['accent'], fg=THEME['text_bright']))
        settings_btn.bind('<Leave>', lambda e: settings_btn.config(bg=THEME['secondary'], fg=THEME['text_bright']))
        
        # Fullscreen toggle button
        fullscreen_btn = tk.Label(right, text="⛶", bg=THEME['secondary'],
                                 fg=THEME['text_bright'], font=('Segoe UI', 14),
                                 cursor='hand2', padx=12, pady=8)
        fullscreen_btn.pack(side=tk.LEFT, padx=(0, 15))
        fullscreen_btn.bind('<Button-1>', self.toggle_fullscreen)
        fullscreen_btn.bind('<Enter>', lambda e: fullscreen_btn.config(bg=THEME['accent'], fg=THEME['text_bright']))
        fullscreen_btn.bind('<Leave>', lambda e: fullscreen_btn.config(bg=THEME['secondary'], fg=THEME['text_bright']))
        
        # Upvote Mode Indicator (removed - now using toggle button)
        
        self.status_indicator = tk.Frame(right, bg='#2d1b4e')
        self.status_indicator.pack(padx=20, pady=5)
        
        status_content = tk.Frame(self.status_indicator, bg='#2d1b4e')
        status_content.pack(padx=20, pady=10)
        
        # Status dot
        self.status_dot = tk.Canvas(status_content, width=12, height=12,
                                   bg='#2d1b4e', highlightthickness=0)
        self.status_dot.pack(side=tk.LEFT, padx=(0, 10))
        self.status_dot.create_oval(2, 2, 10, 10, fill=THEME['success'], outline='')
        
        # Status text
        self.status_text = tk.Label(status_content, text="IDLE", 
                                   bg='#2d1b4e', fg=THEME['success'],
                                   font=('Segoe UI', 10, 'bold'))
        self.status_text.pack(side=tk.LEFT)
    
    def create_stats_panel(self, parent):
        """Create statistics dashboard"""
        container = BlurredFrame(parent, bg='#1a1a3e')
        container.pack(fill=tk.X, pady=(0, 18))
        
        # Header
        header = tk.Frame(container, bg='#252550')
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📊 LIVE STATISTICS", bg='#252550',
                fg=THEME['text_primary'], font=('Segoe UI', 12, 'bold')
                ).pack(anchor='w', padx=22, pady=14)
        
        # Stats grid
        stats_grid = tk.Frame(container, bg='#1a1a3e')
        stats_grid.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)
        
        # Configure grid
        for i in range(2):
            stats_grid.columnconfigure(i, weight=1)
        
        # Stat items with vibrant colors
        stats_config = [
            ("💬", "Comments", "comments", THEME['cyan']),
            ("⭐", "Karma", "karma", THEME['lime']),
            ("🎯", "Subreddits", "subreddits", THEME['orange']),
            ("📁", "Categories", "categories", THEME['rose'])
        ]
        
        self.stat_labels = {}
        
        for idx, (icon, label, key, color) in enumerate(stats_config):
            row = idx // 2
            col = idx % 2
            
            # Create card with enhanced blur effect
            stat_card = tk.Frame(stats_grid, bg='#141b30', 
                               highlightthickness=2, highlightbackground='#2a3555',
                               relief=tk.FLAT)
            stat_card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
            
            # Icon
            tk.Label(stat_card, text=icon, bg='#141b30',
                    font=('Segoe UI Emoji', 20)).pack(pady=(18, 8))
            
            # Value
            value_label = tk.Label(stat_card, text="0", bg='#141b30',
                                  fg=color, font=('Segoe UI', 28, 'bold'))
            value_label.pack()
            self.stat_labels[key] = value_label
            
            # Label
            tk.Label(stat_card, text=label.upper(), bg='#141b30',
                    fg=THEME['text_muted'], font=('Segoe UI', 8, 'bold')
                    ).pack(pady=(5, 18))
        
        # Make grid cells equal height
        for i in range(2):
            stats_grid.rowconfigure(i, weight=1, minsize=110)
    
    def create_category_selector(self, parent):
        """Create category selection panel with 3 columns"""
        container = BlurredFrame(parent, bg='#1a1a3e')
        container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(container, bg='#252550')
        header.pack(fill=tk.X)
        
        header_content = tk.Frame(header, bg='#252550')
        header_content.pack(fill=tk.X, padx=22, pady=14)
        
        tk.Label(header_content, text="🎯 TARGET CATEGORIES", 
                bg='#252550', fg=THEME['text_primary'],
                font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # Select all button
        select_all_btn = tk.Label(header_content, text="Select All", 
                                 bg='#252550', fg=THEME['primary'],
                                 font=('Segoe UI', 9, 'underline'), cursor='hand2')
        select_all_btn.pack(side=tk.RIGHT)
        select_all_btn.bind('<Button-1>', lambda e: self.select_all_categories())
        
        # Grid container for categories (3 columns)
        grid_container = tk.Frame(container, bg='#1a1a3e')
        grid_container.pack(fill=tk.BOTH, expand=True, padx=18, pady=(12, 18))
        
        # Configure grid weights for equal column widths
        for i in range(3):
            grid_container.columnconfigure(i, weight=1)
        
        # Category items in grid layout with rainbow colors
        accent_colors = [THEME['primary'], THEME['teal'], THEME['orange'], 
                        THEME['rose'], THEME['secondary'], THEME['cyan'], THEME['lime']]
        
        categories_list = list(self.categories.items())
        
        for idx, (category, subreddits) in enumerate(categories_list):
            var = tk.BooleanVar(value=(idx < 2))  # First 2 selected by default
            self.category_vars[category] = var
            
            # Calculate grid position (3 columns)
            row = idx // 3
            col = idx % 3
            
            # Category card with enhanced blur
            card = tk.Frame(grid_container, bg='#141b30',
                          highlightthickness=2, highlightbackground='#2a3555',
                          relief=tk.FLAT)
            card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
            
            # Top accent bar
            accent = tk.Frame(card, bg=accent_colors[idx], height=3)
            accent.pack(fill=tk.X)
            accent.pack_propagate(False)
            
            # Content
            content = tk.Frame(card, bg='#141b30')
            content.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
            
            # Checkbox and label
            cb = tk.Checkbutton(content, text=category, variable=var,
                              bg='#141b30', fg=THEME['text_primary'],
                              selectcolor='#1a1a3e',
                              activebackground='#141b30',
                              activeforeground=THEME['text_primary'],
                              font=('Segoe UI', 9, 'bold'),
                              cursor='hand2',
                              wraplength=180,
                              command=self.update_stats_display)
            cb.pack(anchor='w')
            
            # Subreddit count
            tk.Label(content, text=f"{len(subreddits)} subs", 
                    bg='#141b30', fg=THEME['text_muted'],
                    font=('Segoe UI', 8)).pack(anchor='w', pady=(3, 0))
        
        # Make all rows equal height
        for i in range((len(categories_list) + 2) // 3):
            grid_container.rowconfigure(i, weight=1, minsize=70)
    
    def create_activity_monitor(self, parent):
        """Create activity log monitor"""
        container = BlurredFrame(parent, bg='#1a1a3e')
        container.pack(fill=tk.BOTH, expand=True, pady=(0, 18))
        
        # Header with controls
        header = tk.Frame(container, bg='#252550')
        header.pack(fill=tk.X)
        
        header_content = tk.Frame(header, bg='#252550')
        header_content.pack(fill=tk.X, padx=22, pady=14)
        
        tk.Label(header_content, text="📡 ACTIVITY MONITOR", 
                bg='#252550', fg=THEME['text_primary'],
                font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # Clear log button
        clear_btn = tk.Label(header_content, text="Clear", 
                           bg='#252550', fg=THEME['text_muted'],
                           font=('Segoe UI', 9, 'underline'), cursor='hand2')
        clear_btn.pack(side=tk.RIGHT)
        clear_btn.bind('<Button-1>', lambda e: self.clear_log())
        
        # Log area
        log_container = tk.Frame(container, bg='#0e1626')
        log_container.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        self.log_text = scrolledtext.ScrolledText(
            log_container,
            bg='#0e1626',
            fg=THEME['text_secondary'],
            font=('Consolas', 9),
            wrap=tk.WORD,
            borderwidth=0,
            insertbackground=THEME['primary'],
            padx=22, pady=18,
            state='disabled'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output with vibrant colors
        self.log_text.tag_config('success', foreground=THEME['lime'])
        self.log_text.tag_config('warning', foreground=THEME['orange'])
        self.log_text.tag_config('error', foreground=THEME['rose'])
        self.log_text.tag_config('info', foreground=THEME['cyan'])
        self.log_text.tag_config('header', foreground=THEME['text_bright'], font=('Consolas', 9, 'bold'))
        
        # Welcome message
        self.log("═" * 70, 'header')
        self.log("⚡ REDDIT KARMA FARMER BY RONIT", 'header')
        self.log("═" * 70, 'header')
        self.log("")
        self.log("✓ System initialized", 'success')
        self.log("✓ AI engine ready", 'success')
        self.log("✓ Reddit API connected", 'success')
        self.log("")
        self.log("→ Select target categories and press START to begin", 'info')
        self.log("")
    
    def create_control_panel(self, parent):
        """Create bot control panel"""
        container = BlurredFrame(parent, bg='#1a1a3e')
        container.pack(fill=tk.X)
        
        # Header
        header = tk.Frame(container, bg='#252550')
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🎮 CONTROLS", bg='#252550',
                fg=THEME['text_primary'], font=('Segoe UI', 12, 'bold')
                ).pack(anchor='w', padx=22, pady=14)
        
        # Button container
        btn_container = tk.Frame(container, bg='#1a1a3e')
        btn_container.pack(fill=tk.BOTH, expand=True, padx=22, pady=(14, 22))
        
        # Start button with gradient-like colors
        self.start_btn = ModernButton(
            btn_container, 
            "START AUTOMATION",
            self.start_bot,
            bg_color=THEME['success'],
            hover_color=THEME['lime'],
            fg_color=THEME['text_bright'],
            icon="▶",
            height=56
        )
        self.start_btn.pack(fill=tk.X, pady=(0, 12))
        
        # Stop button
        self.stop_btn = ModernButton(
            btn_container,
            "STOP AUTOMATION",
            self.stop_bot,
            bg_color=THEME['danger'],
            hover_color=THEME['rose'],
            fg_color=THEME['text_bright'],
            icon="⏹",
            height=56
        )
        self.stop_btn.pack(fill=tk.X, pady=(0, 12))
        
        # Info text
        info_frame = tk.Frame(btn_container, bg='#1a1a3e')
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(info_frame, text="💡 Tip: Use ⚙ in top bar for settings",
                bg='#1a1a3e', fg=THEME['text_muted'],
                font=('Segoe UI', 8)).pack()
    
    def log(self, message, tag=None):
        """Add message to activity log"""
        self.log_text.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if tag:
            self.log_text.insert(tk.END, f"[{timestamp}] ", 'info')
            self.log_text.insert(tk.END, f"{message}\n", tag)
        else:
            self.log_text.insert(tk.END, f"{message}\n")
        
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def clear_log(self):
        """Clear the activity log"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.log("Activity log cleared", 'info')
    
    def update_stats_display(self):
        """Update the statistics display"""
        selected_subs = self.get_selected_subreddits()
        
        # In meme mode, show correct count
        if self.is_meme_mode:
            selected_cats = 1  # Meme Mode (r/meme + r/funny)
        else:
            selected_cats = sum(1 for var in self.category_vars.values() if var.get())
        
        self.stats['subreddits'] = len(selected_subs)
        self.stats['categories'] = selected_cats
        
        self.stat_labels['comments'].config(text=str(self.stats['comments']))
        self.stat_labels['karma'].config(text=str(self.stats['karma']))
        self.stat_labels['subreddits'].config(text=str(self.stats['subreddits']))
        self.stat_labels['categories'].config(text=str(self.stats['categories']))
    
    def get_selected_subreddits(self):
        """Get list of selected subreddits"""
        # If meme mode is active, return only meme subreddits
        if self.is_meme_mode:
            return self.meme_subreddits
        
        # Otherwise, return selected categories
        selected = []
        for category, var in self.category_vars.items():
            if var.get():
                selected.extend(self.categories[category])
        return selected
    
    def select_all_categories(self):
        """Select all categories"""
        for var in self.category_vars.values():
            var.set(True)
        self.update_stats_display()
    
    def toggle_meme_mode(self):
        """Toggle Meme Mode - selects only memes/funny subreddits and enables upvote mode"""
        self.is_meme_mode = not self.is_meme_mode
        
        if self.is_meme_mode:
            # Enable meme mode
            self.meme_mode_btn.config(bg=THEME['lime'])
            
            # Select only meme categories (for visual feedback)
            for category, var in self.category_vars.items():
                if "Memes" in category or "Humor" in category:
                    var.set(True)
                else:
                    var.set(False)
            
            # Enable upvote mode
            self.settings['upvote_mode'] = True
            self.upvote_toggle_btn.config(bg=THEME['orange'])
            
            self.log("😂 MEME MODE ACTIVATED!", 'success')
            self.log(f"→ Targeting r/meme and r/funny ONLY", 'info')
            self.log("→ Upvote mode enabled for maximum karma", 'info')
        else:
            # Disable meme mode
            self.meme_mode_btn.config(bg=THEME['bg_light'])
            
            # Select first 2 categories by default
            for idx, (category, var) in enumerate(self.category_vars.items()):
                var.set(idx < 2)
            
            self.log("ℹ️ Meme Mode disabled", 'info')
        
        self.update_stats_display()
    
    def toggle_upvote_mode(self):
        """Toggle Upvote Mode on/off"""
        self.settings['upvote_mode'] = not self.settings['upvote_mode']
        
        if self.settings['upvote_mode']:
            self.upvote_toggle_btn.config(bg=THEME['orange'])
            self.log("🔥 UPVOTE MODE ENABLED - Prioritizing high-engagement posts", 'success')
        else:
            self.upvote_toggle_btn.config(bg=THEME['bg_light'])
            self.log("ℹ️ Upvote Mode disabled - Normal post selection", 'info')
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Bot Settings")
        settings_window.geometry("550x650")
        settings_window.configure(bg=THEME['bg_dark'])
        settings_window.resizable(False, False)
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (650 // 2)
        settings_window.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(settings_window, bg=THEME['bg_medium'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="⚙ Bot Configuration", bg=THEME['bg_medium'],
                fg=THEME['text_primary'], font=('Segoe UI', 16, 'bold')
                ).pack(pady=20)
        
        # Scrollable content area
        scroll_container = tk.Frame(settings_window, bg=THEME['bg_dark'])
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 10))
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(scroll_container, bg=THEME['bg_dark'], highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_container, orient='vertical', command=canvas.yview,
                                bg=THEME['bg_medium'], troughcolor=THEME['bg_dark'])
        scrollable_frame = tk.Frame(canvas, bg=THEME['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Content container with padding
        content = tk.Frame(scrollable_frame, bg=THEME['bg_dark'])
        content.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        
        # Settings fields
        settings_data = {}
        
        # Daily Limit
        self.create_setting_field(content, "💬 Daily Comment Limit", 
                                 "Maximum comments per day", 
                                 self.settings['daily_limit'],
                                 settings_data, 'daily_limit', 0)
        
        # Minimum Delay
        self.create_setting_field(content, "⏱️ Minimum Delay (seconds)", 
                                 "Minimum wait time between comments", 
                                 self.settings['min_delay'],
                                 settings_data, 'min_delay', 1)
        
        # Maximum Delay
        self.create_setting_field(content, "⏱️ Maximum Delay (seconds)", 
                                 "Maximum wait time between comments", 
                                 self.settings['max_delay'],
                                 settings_data, 'max_delay', 2)
        
        # Minimum Upvotes
        self.create_setting_field(content, "⬆️ Minimum Post Upvotes", 
                                 "Only comment on posts with this many upvotes", 
                                 self.settings['min_upvotes'],
                                 settings_data, 'min_upvotes', 3)
        
        # Minimum Comments
        self.create_setting_field(content, "💭 Minimum Post Comments", 
                                 "Only comment on posts with this many comments", 
                                 self.settings['min_comments'],
                                 settings_data, 'min_comments', 4)
        
        # Language Selection
        lang_frame = tk.Frame(content, bg=THEME['bg_card'])
        lang_frame.pack(fill=tk.X, pady=(0, 15))
        
        inner_frame = tk.Frame(lang_frame, bg=THEME['bg_card'])
        inner_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(inner_frame, text="🌐 Comment Language", 
                bg=THEME['bg_card'], fg=THEME['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        tk.Label(inner_frame, text="Language style for generated comments", 
                bg=THEME['bg_card'], fg=THEME['text_muted'],
                font=('Segoe UI', 8)).pack(anchor='w', pady=(2, 8))
        
        lang_var = tk.StringVar(value=self.settings['language'])
        settings_data['language'] = lang_var
        
        lang_options = tk.Frame(inner_frame, bg=THEME['bg_card'])
        lang_options.pack(fill=tk.X)
        
        for lang, label in [('auto', 'Auto-detect'), ('english', 'English'), ('hinglish', 'Hinglish')]:
            rb = tk.Radiobutton(lang_options, text=label, variable=lang_var, value=lang,
                              bg=THEME['bg_card'], fg=THEME['text_secondary'],
                              selectcolor=THEME['bg_dark'],
                              activebackground=THEME['bg_card'],
                              font=('Segoe UI', 9),
                              cursor='hand2')
            rb.pack(side=tk.LEFT, padx=(0, 15))
        
        # Upvote Mode Toggle
        upvote_frame = tk.Frame(content, bg=THEME['bg_card'])
        upvote_frame.pack(fill=tk.X, pady=(0, 15))
        
        upvote_inner = tk.Frame(upvote_frame, bg=THEME['bg_card'])
        upvote_inner.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(upvote_inner, text="🔥 Upvote Mode", 
                bg=THEME['bg_card'], fg=THEME['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        tk.Label(upvote_inner, text="Prioritize posts where comments get the most upvotes", 
                bg=THEME['bg_card'], fg=THEME['text_muted'],
                font=('Segoe UI', 8)).pack(anchor='w', pady=(2, 8))
        
        upvote_var = tk.BooleanVar(value=self.settings['upvote_mode'])
        settings_data['upvote_mode'] = upvote_var
        
        upvote_check = tk.Checkbutton(upvote_inner, text="Enable Upvote Mode (smart post selection)", 
                                     variable=upvote_var,
                                     bg=THEME['bg_card'], fg=THEME['text_secondary'],
                                     selectcolor=THEME['bg_dark'],
                                     activebackground=THEME['bg_card'],
                                     activeforeground=THEME['text_primary'],
                                     font=('Segoe UI', 9),
                                     cursor='hand2')
        upvote_check.pack(anchor='w')
        
        # Unbind mousewheel when window closes
        settings_window.protocol("WM_DELETE_WINDOW", lambda: self._close_settings(settings_window, canvas))
        
        # Buttons
        btn_frame = tk.Frame(settings_window, bg=THEME['bg_dark'])
        btn_frame.pack(fill=tk.X, padx=30, pady=(0, 25))
        
        # Save button with vibrant color
        save_btn = ModernButton(
            btn_frame,
            "SAVE SETTINGS",
            lambda: self.save_settings(settings_data, settings_window),
            bg_color=THEME['success'],
            hover_color=THEME['lime'],
            fg_color=THEME['text_bright'],
            icon="✓",
            height=50
        )
        save_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Cancel button
        cancel_btn = ModernButton(
            btn_frame,
            "CANCEL",
            lambda: self._close_settings(settings_window, canvas),
            bg_color=THEME['secondary'],
            hover_color=THEME['accent'],
            fg_color=THEME['text_bright'],
            icon="✕",
            height=45
        )
        cancel_btn.pack(fill=tk.X)
    
    def _close_settings(self, window, canvas):
        """Close settings window and unbind mousewheel"""
        canvas.unbind_all("<MouseWheel>")
        window.destroy()
    
    def create_setting_field(self, parent, title, description, default_value, data_dict, key, index):
        """Create a setting input field"""
        frame = tk.Frame(parent, bg=THEME['bg_card'])
        frame.pack(fill=tk.X, pady=(0, 15))
        
        inner = tk.Frame(frame, bg=THEME['bg_card'])
        inner.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(inner, text=title, bg=THEME['bg_card'], fg=THEME['text_primary'],
                font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        tk.Label(inner, text=description, bg=THEME['bg_card'], fg=THEME['text_muted'],
                font=('Segoe UI', 8)).pack(anchor='w', pady=(2, 8))
        
        entry_frame = tk.Frame(inner, bg=THEME['bg_dark'])
        entry_frame.pack(fill=tk.X)
        
        entry = tk.Entry(entry_frame, bg=THEME['bg_dark'], fg=THEME['text_primary'],
                        font=('Segoe UI', 11), insertbackground=THEME['primary'],
                        borderwidth=1, relief=tk.SOLID)
        entry.pack(fill=tk.X, ipady=8, padx=2, pady=2)
        entry.insert(0, str(default_value))
        
        data_dict[key] = entry
    
    def save_settings(self, settings_data, window):
        """Save settings from dialog"""
        try:
            # Validate and save settings
            self.settings['daily_limit'] = int(settings_data['daily_limit'].get())
            self.settings['min_delay'] = int(settings_data['min_delay'].get())
            self.settings['max_delay'] = int(settings_data['max_delay'].get())
            self.settings['min_upvotes'] = int(settings_data['min_upvotes'].get())
            self.settings['min_comments'] = int(settings_data['min_comments'].get())
            self.settings['language'] = settings_data['language'].get()
            self.settings['upvote_mode'] = settings_data['upvote_mode'].get()
            
            # Update upvote mode button color in top bar
            if self.settings['upvote_mode']:
                self.upvote_toggle_btn.config(bg=THEME['orange'])
            else:
                self.upvote_toggle_btn.config(bg=THEME['bg_light'])
            
            # Validate values
            if self.settings['daily_limit'] < 1 or self.settings['daily_limit'] > 200:
                raise ValueError("Daily limit must be between 1 and 200")
            
            if self.settings['min_delay'] < 10 or self.settings['min_delay'] > 600:
                raise ValueError("Minimum delay must be between 10 and 600 seconds")
            
            if self.settings['max_delay'] < self.settings['min_delay']:
                raise ValueError("Maximum delay must be greater than minimum delay")
            
            if self.settings['min_upvotes'] < 0:
                raise ValueError("Minimum upvotes cannot be negative")
            
            if self.settings['min_comments'] < 0:
                raise ValueError("Minimum comments cannot be negative")
            
            # Close window
            window.destroy()
            
            # Show success message
            self.log("⚙ Settings saved successfully", 'success')
            self.log(f"→ Daily limit: {self.settings['daily_limit']} comments", 'info')
            self.log(f"→ Delay: {self.settings['min_delay']}-{self.settings['max_delay']}s", 'info')
            self.log(f"→ Min upvotes: {self.settings['min_upvotes']}", 'info')
            self.log(f"→ Language: {self.settings['language']}", 'info')
            self.log(f"→ Upvote Mode: {'ENABLED' if self.settings['upvote_mode'] else 'DISABLED'}", 'info')
            self.log("")
            
        except ValueError as e:
            messagebox.showerror("Invalid Settings", str(e), parent=window)
    
    def start_bot(self):
        """Start the Reddit bot"""
        # Verify credentials
        if not all([os.getenv("REDDIT_CLIENT_ID"), 
                   os.getenv("REDDIT_CLIENT_SECRET"),
                   os.getenv("REDDIT_USERNAME"), 
                   os.getenv("REDDIT_PASSWORD")]):
            messagebox.showerror("Configuration Error", 
                               "Missing Reddit API credentials!\n\n" +
                               "Please configure your .env file.")
            return
        
        # Check category selection
        selected = self.get_selected_subreddits()
        if not selected:
            messagebox.showwarning("No Categories Selected", 
                                 "Please select at least one category to target.")
            return
        
        # Update state
        self.is_running = True
        self.stats['comments'] = 0
        self.stats['session_start'] = datetime.now()
        
        # Update status
        self.status_text.config(text="RUNNING", fg=THEME['primary'])
        self.status_dot.delete("all")
        self.status_dot.create_oval(2, 2, 10, 10, fill=THEME['primary'], outline='')
        
        self.log("")
        self.log("═" * 70, 'header')
        self.log("🚀 AUTOMATION STARTED", 'success')
        self.log(f"→ Targeting {len(selected)} subreddits", 'info')
        self.log(f"→ {self.stats['categories']} categories selected", 'info')
        if self.settings['upvote_mode']:
            self.log("→ 🔥 UPVOTE MODE: Prioritizing high-engagement posts", 'success')
        self.log("═" * 70, 'header')
        self.log("")
        
        # Initialize bot with current settings
        self.bot = RedditBot(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            target_subreddits=selected,
            language=self.settings['language'],
            daily_limit=self.settings['daily_limit'],
            min_upvotes=self.settings['min_upvotes'],
            min_comments=self.settings['min_comments'],
            upvote_mode=self.settings['upvote_mode']
        )
        
        # Run in thread
        thread = threading.Thread(target=self.run_bot_thread, daemon=True)
        thread.start()
    
    def stop_bot(self):
        """Stop the Reddit bot"""
        self.is_running = False
        
        self.status_text.config(text="STOPPED", fg=THEME['warning'])
        self.status_dot.delete("all")
        self.status_dot.create_oval(2, 2, 10, 10, fill=THEME['warning'], outline='')
        
        self.log("")
        self.log("⏹ AUTOMATION STOPPED BY USER", 'warning')
        self.log("")
    
    def run_bot_thread(self):
        """Run bot in background thread"""
        try:
            # Redirect stdout to GUI
            class GUILogger:
                def __init__(self, log_func, root):
                    self.log_func = log_func
                    self.root = root
                
                def write(self, message):
                    if message and message.strip():
                        msg = message.strip()
                        
                        # Determine message type
                        tag = None
                        if '✅' in msg or 'success' in msg.lower():
                            tag = 'success'
                        elif '⚠️' in msg or 'warning' in msg.lower():
                            tag = 'warning'
                        elif '❌' in msg or 'error' in msg.lower():
                            tag = 'error'
                        else:
                            tag = 'info'
                        
                        self.root.after(0, self.log_func, msg, tag)
                
                def flush(self):
                    pass
            
            original_stdout = sys.stdout
            sys.stdout = GUILogger(self.log, self.root)
            
            # Run bot
            trending = self.bot.get_trending_topics()
            
            for submission in trending:
                if not self.is_running:
                    break
                
                try:
                    title = self.bot.extract_text_title(submission)
                    content = self.bot.extract_text_content(submission)
                    comments = self.bot.extract_comment_content_and_upvotes(submission)
                    
                    self.bot.generate_comment(submission, title, content, comments)
                    
                    # Update stats
                    self.stats['comments'] += 1
                    self.root.after(0, self.update_stats_display)
                    
                    # Check limits
                    if self.bot.comments_today >= self.bot.daily_limit:
                        break
                    
                    # Cooldown using settings
                    from random import randint
                    from time import sleep
                    cooldown = randint(self.settings['min_delay'], self.settings['max_delay'])
                    self.log(f"⏳ Cooldown: {cooldown}s", 'info')
                    sleep(cooldown)
                    
                except Exception as e:
                    self.log(f"Error processing post: {str(e)}", 'error')
                    continue
            
            self.log("")
            self.log(f"✓ Session complete! {self.stats['comments']} comments posted", 'success')
            self.log("")
            
        except Exception as e:
            self.log(f"Critical error: {str(e)}", 'error')
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            sys.stdout = original_stdout
            self.is_running = False
            self.root.after(0, self.reset_status)
    
    def reset_status(self):
        """Reset status to idle"""
        self.status_text.config(text="IDLE", fg=THEME['success'])
        self.status_dot.delete("all")
        self.status_dot.create_oval(2, 2, 10, 10, fill=THEME['success'], outline='')
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        return 'break'
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
        return 'break'


def main():
    root = tk.Tk()
    app = RedditBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
