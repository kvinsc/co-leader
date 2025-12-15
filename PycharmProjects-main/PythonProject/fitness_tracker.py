import datetime
from datetime import timezone
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import datetime
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# App Constants
# ---------------------------
APP_NAME = "Markyle Fitness Tracker"
DATA_FILE = "users.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "dark_mode": True,
    "sidebar_collapsed": False
}



# Data Utilities
# ---------------------------
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            s = json.load(f)
            out = DEFAULT_SETTINGS.copy()
            out.update(s)
            return out
    except:
        return DEFAULT_SETTINGS.copy()


def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)

        # Set window size to 80% of screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())
        self.is_fullscreen = False
        self.data = load_data()
        self.settings = load_settings()
        self.current_user = None
        self.is_logged_in = False
        self.dark_mode = self.settings.get("dark_mode", True)
        self.update_theme()
        self.show_login_screen()

    def update_theme(self):
        if self.dark_mode:
            self.bg_color = "#0a0e27"
            self.panel_color = "#1a1f3a"
            self.text_color = "#e8eaf6"
            self.muted_text = "#9ca3af"
            self.accent_color = "#6366f1"
            self.accent_hover = "#4f46e5"
            self.input_bg = "#2d3250"
            self.sidebar_bg = "#161b33"
        else:
            self.bg_color = "#f8fafc"
            self.panel_color = "#ffffff"
            self.text_color = "#1e293b"
            self.muted_text = "#64748b"
            self.accent_color = "#6366f1"
            self.accent_hover = "#4f46e5"
            self.input_bg = "#f1f5f9"
            self.sidebar_bg = "#ffffff"
        self.root.configure(bg=self.bg_color)

    def create_brand_text(self, parent):
        """Create clear, prominent brand text with icon"""
        frame = tk.Frame(parent, bg=self.panel_color)

        # Large, clear icon with better visibility
        tk.Label(
            frame,
            text="💪",
            font=("Segoe UI", 60),
            bg=self.panel_color,
            fg="#f59e0b"
        ).pack(pady=(0, 10))

        tk.Label(
            frame,
            text="MARKYLE",
            font=("Segoe UI", 26, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack()

        tk.Label(
            frame,
            text="Fitness Tracker",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(pady=(2, 0))

        return frame

    def create_logo(self, parent):
        """Alias for create_brand_text for compatibility"""
        return self.create_brand_text(parent)

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        try:
            from PIL import Image, ImageTk, ImageFilter, ImageEnhance
            bg_image = Image.open("gym_background.jpg")
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            bg_image = bg_image.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
            bg_image = ImageEnhance.Brightness(bg_image).enhance(0.3)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(main_frame, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass

        login_frame = tk.Frame(main_frame, bg=self.panel_color, padx=50, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.create_brand_text(login_frame).pack(pady=(0, 30))

        tk.Label(login_frame, text="USERNAME", font=("Segoe UI", 9, "bold"), bg=self.panel_color,
                 fg=self.muted_text).pack(anchor="w", pady=(0, 5))
        uc = tk.Frame(login_frame, bg=self.input_bg)
        uc.pack(fill="x", pady=(0, 15))
        tk.Label(uc, text="👤", font=("Segoe UI", 18), bg=self.input_bg, fg=self.muted_text).pack(side="left",
                                                                                                 padx=(10, 5))
        self.username_entry = tk.Entry(uc, font=("Segoe UI", 12), bg=self.input_bg, fg=self.text_color,
                                       insertbackground=self.text_color, border=0, relief="flat")
        self.username_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

        tk.Label(login_frame, text="PASSWORD", font=("Segoe UI", 9, "bold"), bg=self.panel_color,
                 fg=self.muted_text).pack(anchor="w", pady=(0, 5))
        pc = tk.Frame(login_frame, bg=self.input_bg)
        pc.pack(fill="x", pady=(0, 10))
        tk.Label(pc, text="🔒", font=("Segoe UI", 18), bg=self.input_bg, fg=self.muted_text).pack(side="left",
                                                                                                 padx=(10, 5))
        self.password_entry = tk.Entry(pc, font=("Segoe UI", 12), bg=self.input_bg, fg=self.text_color,
                                       insertbackground=self.text_color, show="●", border=0, relief="flat")
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(login_frame, text="Show password", variable=self.show_password_var, command=self.toggle_password,
                       font=("Segoe UI", 9), bg=self.panel_color, fg=self.muted_text, selectcolor=self.input_bg,
                       activebackground=self.panel_color, activeforeground=self.text_color, cursor="hand2").pack(
            anchor="w", pady=(0, 25))

        lb = tk.Button(login_frame, text="LOGIN", font=("Segoe UI", 12, "bold"), bg=self.accent_color, fg="white",
                       activebackground=self.accent_hover, activeforeground="white", relief="flat", cursor="hand2",
                       command=self.login, borderwidth=0)
        lb.pack(fill="x", ipady=12, pady=(0, 15))
        lb.bind("<Enter>", lambda e: lb.config(bg=self.accent_hover))
        lb.bind("<Leave>", lambda e: lb.config(bg=self.accent_color))

        rf = tk.Frame(login_frame, bg=self.panel_color)
        rf.pack()
        tk.Label(rf, text="Don't have an account? ", font=("Segoe UI", 9), bg=self.panel_color,
                 fg=self.muted_text).pack(side="left")
        rb = tk.Button(rf, text="Register", font=("Segoe UI", 9, "bold underline"), bg=self.panel_color,
                       fg=self.accent_color, activebackground=self.panel_color, activeforeground=self.accent_hover,
                       relief="flat", cursor="hand2", command=self.show_register_screen, borderwidth=0)
        rb.pack(side="left")

        self.password_entry.bind("<Return>", lambda e: self.login())

    def show_register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        mf = tk.Frame(self.root, bg=self.bg_color)
        mf.pack(fill="both", expand=True)
        rf = tk.Frame(mf, bg=self.panel_color, padx=50, pady=40)
        rf.place(relx=0.5, rely=0.5, anchor="center")

        self.create_brand_text(rf).pack(pady=(0, 30))

        tk.Label(rf, text="USERNAME", font=("Segoe UI", 9, "bold"), bg=self.panel_color, fg=self.muted_text).pack(
            anchor="w", pady=(0, 5))
        uc = tk.Frame(rf, bg=self.input_bg)
        uc.pack(fill="x", pady=(0, 15))
        tk.Label(uc, text="👤", font=("Segoe UI", 18), bg=self.input_bg).pack(side="left", padx=(10, 5))
        self.reg_username = tk.Entry(uc, font=("Segoe UI", 12), bg=self.input_bg, fg=self.text_color,
                                     insertbackground=self.text_color, border=0, relief="flat")
        self.reg_username.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

        tk.Label(rf, text="PASSWORD", font=("Segoe UI", 9, "bold"), bg=self.panel_color, fg=self.muted_text).pack(
            anchor="w", pady=(0, 5))
        pc = tk.Frame(rf, bg=self.input_bg)
        pc.pack(fill="x", pady=(0, 15))
        tk.Label(pc, text="🔒", font=("Segoe UI", 18), bg=self.input_bg).pack(side="left", padx=(10, 5))
        self.reg_password = tk.Entry(pc, font=("Segoe UI", 12), bg=self.input_bg, fg=self.text_color,
                                     insertbackground=self.text_color, show="●", border=0, relief="flat")
        self.reg_password.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

        tk.Label(rf, text="CONFIRM PASSWORD", font=("Segoe UI", 9, "bold"), bg=self.panel_color,
                 fg=self.muted_text).pack(anchor="w", pady=(0, 5))
        p2c = tk.Frame(rf, bg=self.input_bg)
        p2c.pack(fill="x", pady=(0, 25))
        tk.Label(p2c, text="🔒", font=("Segoe UI", 18), bg=self.input_bg).pack(side="left", padx=(10, 5))
        self.reg_password2 = tk.Entry(p2c, font=("Segoe UI", 12), bg=self.input_bg, fg=self.text_color,
                                      insertbackground=self.text_color, show="●", border=0, relief="flat")
        self.reg_password2.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

        rb = tk.Button(rf, text="CREATE ACCOUNT", font=("Segoe UI", 12, "bold"), bg=self.accent_color, fg="white",
                       activebackground=self.accent_hover, activeforeground="white", relief="flat", cursor="hand2",
                       command=self.register, borderwidth=0)
        rb.pack(fill="x", ipady=12, pady=(0, 15))
        rb.bind("<Enter>", lambda e: rb.config(bg=self.accent_hover))
        rb.bind("<Leave>", lambda e: rb.config(bg=self.accent_color))

        tk.Button(rf, text="← Back to Login", font=("Segoe UI", 9, "bold"), bg=self.panel_color, fg=self.accent_color,
                  activebackground=self.panel_color, activeforeground=self.accent_hover, relief="flat", cursor="hand2",
                  command=self.show_login_screen, borderwidth=0).pack()

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        user = self.data.get(username)
        if not user or user.get("password") != password:
            messagebox.showerror("Login Failed", "Invalid credentials")
            return

        self.current_user = username
        self.is_logged_in = True

        messagebox.showinfo("Success", "Login successful!")

        # Set fullscreen on login
        self.is_fullscreen = True
        self.root.state('zoomed')  # Maximized for Windows

        self.show_dashboard()
        self.toggle_sidebar()

    def register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        password2 = self.reg_password2.get().strip()

        if not username or not password or not password2:
            messagebox.showerror("Error", "All fields are required")
            return

        if username in self.data:
            messagebox.showerror("Error", "Username already exists")
            return

        if password != password2:
            messagebox.showerror("Error", "Passwords do not match")
            return

        self.data[username] = {
            "password": password,
            "profile": {},
            "workouts": [],
            "settings": {}
        }

        save_data(self.data)
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_screen()

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True)

        self.sidebar_visible = True
        self.create_sidebar(self.main_container)

        content_wrapper = tk.Frame(self.main_container, bg=self.bg_color)
        content_wrapper.pack(side="left", fill="both", expand=True)

        top_btn_frame = tk.Frame(content_wrapper, bg=self.bg_color)
        top_btn_frame.pack(anchor="nw", padx=10, pady=10)

        menu_btn = tk.Button(
            top_btn_frame,
            text="☰",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            activebackground=self.input_bg,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.toggle_sidebar,
            padx=15,
            pady=5
        )
        menu_btn.pack(side="left", padx=(0, 5))

        refresh_btn = tk.Button(
            top_btn_frame,
            text="🔄",
            font=("Segoe UI", 20),
            bg=self.bg_color,
            fg=self.text_color,
            activebackground=self.input_bg,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.refresh_content,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side="left")

        self.content_frame = tk.Frame(content_wrapper, bg=self.bg_color)
        self.content_frame.pack(fill="both", expand=True)

        self.show_dashboard_content()

    def create_sidebar(self, parent):
        self.sidebar = tk.Frame(parent, bg=self.sidebar_bg, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        logo_frame.pack(pady=30, padx=20)

        icon_label = tk.Label(
            logo_frame,
            text="💪",
            font=("Segoe UI", 64),
            bg=self.bg_color,
            fg="#FFD700"
        )
        icon_label.pack()

        title = tk.Label(
            logo_frame,
            text="Markyle Fitness",
            font=("Segoe UI", 16, "bold"),
            bg=self.sidebar_bg,
            fg=self.text_color
        )
        title.pack(pady=(10, 0))

        version_label = tk.Label(
            logo_frame,
            text="v1.0",
            font=("Segoe UI", 9),
            bg=self.sidebar_bg,
            fg=self.muted_text
        )
        version_label.pack()

        nav_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        nav_frame.pack(fill="x", padx=10)

        buttons = [
            ("🏠 Dashboard", self.show_dashboard_content),
            ("👤 Profile", self.show_profile_content),
            ("💪 Workouts", self.show_workouts_content),
            ("⚙️ Settings", self.show_settings_content)
        ]

        self.nav_buttons = []
        for text, command in buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("Segoe UI", 12),
                bg=self.sidebar_bg,
                fg=self.muted_text,
                activebackground=self.input_bg,
                activeforeground=self.text_color,
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=15,
                command=command
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons.append(btn)

            btn.bind("<Enter>", lambda e, b=btn: self.nav_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.nav_hover(b, False))

        tk.Frame(self.sidebar, bg=self.sidebar_bg).pack(expand=True)

        logout_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        logout_frame.pack(fill="x", padx=10, pady=20)

        logout_btn = tk.Button(
            logout_frame,
            text="🚪 Logout",
            font=("Segoe UI", 12),
            bg=self.sidebar_bg,
            fg="#ef4444",
            activebackground=self.input_bg,
            activeforeground="#ef4444",
            relief="flat",
            cursor="hand2",
            command=self.logout,
            anchor="w",
            padx=15
        )
        logout_btn.pack(fill="x")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            # Hide sidebar instantly
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            # Show sidebar instantly
            self.sidebar.pack(side="left", fill="y", before=self.main_container.winfo_children()[1])
            self.sidebar_visible = True

    def refresh_content(self):
        self.data = load_data()

        for i, btn in enumerate(self.nav_buttons):
            if btn.cget("bg") == self.accent_color:
                if i == 0:
                    self.show_dashboard_content()
                elif i == 1:
                    self.show_profile_content()
                elif i == 2:
                    self.show_workouts_content()
                elif i == 3:
                    self.show_settings_content()
                break

    def highlight_nav_button(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.config(bg=self.accent_color, fg="white")
            else:
                btn.config(bg=self.sidebar_bg, fg=self.muted_text)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def animate_fade_in(self, widget, alpha=0.0):
        pass

    def button_hover_effect(self, button, enter):
        if enter:
            button.config(relief="raised", bd=2)
        else:
            button.config(relief="flat", bd=0)

    def nav_hover(self, button, enter):
        if enter:
            if button.cget("bg") != self.accent_color:
                button.config(bg=self.input_bg)
                self.root.after(10, lambda: button.config(relief="flat"))
        else:
            if button.cget("bg") != self.accent_color:
                button.config(bg=self.sidebar_bg)
                self.root.after(10, lambda: button.config(relief="flat"))

    def show_dashboard_content(self):
        self.highlight_nav_button(0)
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        title_frame = tk.Frame(container, bg=self.bg_color)
        title_frame.pack(anchor="w", pady=(0, 20))

        tk.Label(
            title_frame,
            text="👋",
            font=("Segoe UI", 48),
            bg=self.bg_color,
            fg="#FFD700"
        ).pack(side="left", padx=(0, 15))

        title = tk.Label(
            title_frame,
            text=f"Welcome back, {self.current_user}!",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(side="left")

        stats_frame = tk.Frame(container, bg=self.bg_color)
        stats_frame.pack(fill="x", pady=20)

        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        import datetime as dt
        today = dt.date.today().isoformat()
        today_workouts = [w for w in workouts if w.get("date") == today]

        total_mins = sum(w.get("duration_min", 0) for w in today_workouts)
        total_cal = sum(w.get("calories", 0) for w in today_workouts)

        stats = [
            ("Total Workouts", str(len(today_workouts)), "#3b82f6", "🏃"),
            ("Total Minutes", str(total_mins), "#10b981", "⏱️"),
            ("Calories Burned", str(total_cal), "#f59e0b", "🔥")
        ]

        for title_text, value, color, icon in stats:
            card = tk.Frame(stats_frame, bg=self.panel_color, relief="flat", bd=0)
            card.pack(side="left", padx=(0, 20), ipadx=30, ipady=20)

            tk.Label(
                card,
                text=icon,
                font=("Segoe UI", 38),
                bg=self.panel_color,
                fg=color
            ).pack(pady=(0, 5))

            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 32, "bold"),
                bg=self.panel_color,
                fg=color
            ).pack()

            tk.Label(
                card,
                text=title_text,
                font=("Segoe UI", 11),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack(pady=(5, 0))

        recent_frame = tk.Frame(container, bg=self.panel_color, relief="flat")
        recent_frame.pack(fill="both", expand=True, pady=20)

        recent_header = tk.Frame(recent_frame, bg=self.panel_color)
        recent_header.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            recent_header,
            text="📋",
            font=("Segoe UI", 28),
            bg=self.panel_color,
            fg="#10b981"
        ).pack(side="left", padx=(0, 12))

        tk.Label(
            recent_header,
            text="Today's Activity",
            font=("Segoe UI", 18, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(side="left")

        # ADD SCROLLABLE CANVAS HERE
        canvas_frame = tk.Frame(recent_frame, bg=self.panel_color)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Create canvas and scrollbar
        canvas = tk.Canvas(canvas_frame, bg=self.panel_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.panel_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        if not today_workouts:
            empty_state = tk.Frame(scrollable_frame, bg=self.panel_color)
            empty_state.pack(fill="both", expand=True, pady=30)

            tk.Label(
                empty_state,
                text="💤",
                font=("Segoe UI", 64),
                bg=self.panel_color,
                fg="#9ca3af"
            ).pack(pady=(20, 10))

            tk.Label(
                empty_state,
                text="No workouts today",
                font=("Segoe UI", 14, "bold"),
                bg=self.panel_color,
                fg=self.text_color
            ).pack()

            tk.Label(
                empty_state,
                text="Add your first workout to get started!",
                font=("Segoe UI", 11),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack(pady=(5, 20))
        else:
            for workout in today_workouts:
                workout_card = tk.Frame(scrollable_frame, bg=self.input_bg)
                workout_card.pack(fill="x", pady=5)

                icon_map = {
                    "Running": "🏃",
                    "Cycling": "🚴",
                    "Swimming": "🏊",
                    "Weight Training": "🏋️",
                    "Yoga": "🧘",
                    "Pilates": "🤸",
                    "CrossFit": "💪",
                    "Boxing": "🥊",
                    "Dancing": "💃",
                    "Walking": "🚶",
                    "Hiking": "🥾",
                    "Rowing": "🚣",
                    "Jump Rope": "🪢",
                    "Elliptical": "🎯",
                    "Aerobics": "🤾",
                    "Sports (Basketball, Soccer, etc.)": "⚽",
                    "Stretching": "🤸",
                    "HIIT": "⚡",
                }
                workout_icon = icon_map.get(workout.get("type", ""), "🏃")

                icon_label = tk.Label(
                    workout_card,
                    text=workout_icon,
                    font=("Segoe UI", 36),
                    bg=self.input_bg
                )
                icon_label.pack(side="left", padx=15, pady=10)

                info_frame = tk.Frame(workout_card, bg=self.input_bg)
                info_frame.pack(side="left", padx=5, pady=10)

                tk.Label(
                    info_frame,
                    text=workout.get("type", "Workout"),
                    font=("Segoe UI", 14, "bold"),
                    bg=self.input_bg,
                    fg=self.text_color
                ).pack(anchor="w")

                tk.Label(
                    info_frame,
                    text=f"⏱️ {workout.get('duration_min', 0)} min • 🔥 {workout.get('calories', 0)} kcal",
                    font=("Segoe UI", 10),
                    bg=self.input_bg,
                    fg=self.muted_text
                ).pack(anchor="w")

    def show_profile_content(self):
        self.highlight_nav_button(1)
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        # Title with icon
        title_frame = tk.Frame(container, bg=self.bg_color)
        title_frame.pack(anchor="w", pady=(0, 20))

        tk.Label(
            title_frame,
            text="👤",
            font=("Segoe UI", 32),
            bg=self.bg_color,
            fg="#6366f1"
        ).pack(side="left", padx=(0, 10))

        title = tk.Label(
            title_frame,
            text="Profile Settings",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(side="left")

        # Profile card with visual enhancement
        card = tk.Frame(container, bg=self.panel_color, relief="flat")
        card.pack(fill="both", expand=True)

        # Profile avatar
        avatar_frame = tk.Frame(card, bg=self.panel_color)
        avatar_frame.pack(pady=(20, 10))

        tk.Label(
            avatar_frame,
            text="👤",
            font=("Segoe UI", 72),
            bg=self.panel_color,
            fg="#6366f1"
        ).pack()

        form_container = tk.Frame(card, bg=self.panel_color)
        form_container.pack(fill="both", expand=True, padx=30, pady=(10, 30))

        labels = ["Name", "Age", "Weight (kg)", "Height (cm)", "Daily Calorie Goal"]
        self.profile_entries = {}

        profile = self.data.get(self.current_user, {}).get("profile", {})

        for i, label in enumerate(labels):
            tk.Label(
                form_container,
                text=label,
                font=("Segoe UI", 11),
                bg=self.panel_color,
                fg=self.text_color
            ).grid(row=i, column=0, sticky="w", padx=10, pady=10)

            entry = tk.Entry(
                form_container,
                font=("Segoe UI", 11),
                bg=self.input_bg,
                fg=self.text_color,
                insertbackground=self.text_color,
                width=30,
                relief="flat"
            )
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            entry.insert(0, profile.get(label.lower().replace(" ", "_"), ""))
            self.profile_entries[label] = entry

        # Save button
        save_btn = tk.Button(
            card,
            text="Save Profile",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.save_profile,
            padx=30,
            pady=10
        )
        save_btn.pack(pady=20)

    def save_profile(self):
        if not self.current_user:
            return

        profile = {}
        for label, entry in self.profile_entries.items():
            key = label.lower().replace(" ", "_")
            profile[key] = entry.get().strip()

        self.data[self.current_user]["profile"] = profile
        save_data(self.data)
        messagebox.showinfo("Success", "Profile saved successfully!")

    def show_workouts_content(self):
        self.highlight_nav_button(2)
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        # Title with icon
        title_frame = tk.Frame(container, bg=self.bg_color)
        title_frame.pack(anchor="w", pady=(0, 20))

        tk.Label(
            title_frame,
            text="💪",
            font=("Segoe UI", 32),
            bg=self.bg_color,
            fg="#f59e0b"
        ).pack(side="left", padx=(0, 10))

        title = tk.Label(
            title_frame,
            text="Add New Workout",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(side="left")

        # Workout card
        card = tk.Frame(container, bg=self.panel_color, relief="flat")
        card.pack(fill="both", expand=True)

        form_container = tk.Frame(card, bg=self.panel_color)
        form_container.pack(fill="both", expand=True, padx=30, pady=30)

        # Date with calendar picker
        tk.Label(
            form_container,
            text="Date",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        date_frame = tk.Frame(form_container, bg=self.panel_color)
        date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.workout_date = tk.Entry(
            date_frame,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=25,
            relief="flat"
        )
        self.workout_date.pack(side="left", ipady=5)
        self.workout_date.insert(0, datetime.date.today().isoformat())

        # Calendar button
        cal_btn = tk.Button(
            date_frame,
            text="📅",
            font=("Segoe UI", 12),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.open_calendar(self.workout_date),  # ADD THIS LINE
            padx=10,
            pady=5
        )
        cal_btn.pack(side="left", padx=(5, 0))

        # Type
        tk.Label(
            form_container,
            text="Workout Type *",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

        workout_types = [
            "Running",
            "Cycling",
            "Swimming",
            "Weight Training",
            "Yoga",
            "Pilates",
            "CrossFit",
            "Boxing",
            "Dancing",
            "Walking",
            "Hiking",
            "Rowing",
            "Jump Rope",
            "Elliptical",
            "Aerobics",
            "Sports (Basketball, Soccer, etc.)",
            "Stretching",
            "HIIT",
            "Other"
        ]

        type_frame = tk.Frame(form_container, bg=self.panel_color)
        type_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.workout_type_var = tk.StringVar()
        self.workout_type = ttk.Combobox(
            type_frame,
            textvariable=self.workout_type_var,
            values=workout_types,
            font=("Segoe UI", 11),
            width=28,
            state="readonly"
        )
        self.workout_type.pack(side="left")
        self.workout_type.set("Select workout type")  # Default text

        # Duration
        tk.Label(
            form_container,
            text="Duration (minutes) *",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.workout_duration = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            relief="flat"
        )
        self.workout_duration.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Calories
        tk.Label(
            form_container,
            text="Calories *",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

        self.workout_calories = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            relief="flat"
        )
        self.workout_calories.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Notes
        tk.Label(
            form_container,
            text="Notes (optional)",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=4, column=0, sticky="w", padx=10, pady=10)

        self.workout_notes = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            relief="flat"
        )
        self.workout_notes.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Buttons
        btn_frame = tk.Frame(card, bg=self.panel_color)
        btn_frame.pack(pady=20)

        save_btn = tk.Button(
            btn_frame,
            text="Save Workout",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.save_workout,
            padx=20,
            pady=10
        )
        save_btn.pack(side="left", padx=5)

        view_btn = tk.Button(
            btn_frame,
            text="View History",
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            activebackground=self.muted_text,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.show_history,
            padx=20,
            pady=10
        )
        view_btn.pack(side="left", padx=5)

    def save_workout(self):
        try:
            date = self.workout_date.get().strip()
            workout_type = self.workout_type_var.get().strip()
            duration_str = self.workout_duration.get().strip()
            calories_str = self.workout_calories.get().strip()
            notes = self.workout_notes.get().strip()

            # Validation
            if not workout_type or workout_type == "Select workout type":
                messagebox.showerror("Error", "Please select a workout type")
                return

            if not duration_str:
                messagebox.showerror("Error", "Duration is required")
                return

            if not calories_str:
                messagebox.showerror("Error", "Calories is required")
                return

            try:
                duration = int(duration_str)
                calories = int(calories_str)
            except ValueError:
                messagebox.showerror("Error", "Duration and calories must be valid numbers")
                return

            if duration <= 0:
                messagebox.showerror("Error", "Duration must be greater than 0")
                return

            if calories < 0:
                messagebox.showerror("Error", "Calories cannot be negative")
                return

            workout = {
                "date": date,
                "type": workout_type,
                "duration_min": duration,
                "calories": calories,
                "notes": notes,
                "created_at": datetime.datetime.utcnow().isoformat()
            }

            self.data.setdefault(self.current_user, {
                "password": "",
                "profile": {},
                "workouts": [],
                "settings": {}
            })
            self.data[self.current_user].setdefault("workouts", []).append(workout)

            save_data(self.data)
            messagebox.showinfo("Success", "Workout saved successfully!")

            # Animate success feedback
            self.refresh_content()

            # Clear fields
            self.workout_type.set("Select workout type")
            self.workout_duration.delete(0, tk.END)
            self.workout_calories.delete(0, tk.END)
            self.workout_notes.delete(0, tk.END)
            self.workout_date.delete(0, tk.END)
            self.workout_date.insert(0, datetime.date.today().isoformat())

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workout: {str(e)}")

    def show_history(self):
        """Show workout history in a new window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Workout History")
        history_window.geometry("800x500")
        history_window.configure(bg=self.bg_color)

        title = tk.Label(
            history_window,
            text="Workout History",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=20)

        # Treeview
        tree_frame = tk.Frame(history_window, bg=self.bg_color)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tree = ttk.Treeview(
            tree_frame,
            columns=("date", "type", "duration", "calories", "notes"),
            show="headings",
            height=15
        )

        for col in ("date", "type", "duration", "calories", "notes"):
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=120)

        tree.pack(fill="both", expand=True)

        # Load workouts
        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        sorted_workouts = sorted(workouts, key=lambda x: x.get("date", ""), reverse=True)

        for workout in sorted_workouts:
            tree.insert("", "end", values=(
                workout.get("date", ""),
                workout.get("type", ""),
                f"{workout.get('duration_min', 0)} min",
                workout.get("calories", 0),
                workout.get("notes", "")
            ))

        # Export button
        btn_frame = tk.Frame(history_window, bg=self.bg_color)
        btn_frame.pack(pady=10)

        export_btn = tk.Button(
            btn_frame,
            text="Export to CSV",
            font=("Segoe UI", 11),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.export_csv(),
            padx=20,
            pady=8
        )
        export_btn.pack(side="left", padx=5)

        done_btn = tk.Button(
            btn_frame,
            text="Done",
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            activebackground=self.muted_text,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            command=history_window.destroy,
            padx=20,
            pady=8
        )
        done_btn.pack(side="left", padx=5)

    def show_settings_content(self):
        self.highlight_nav_button(3)
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        # Title with icon
        title_frame = tk.Frame(container, bg=self.bg_color)
        title_frame.pack(anchor="w", pady=(0, 20))

        tk.Label(
            title_frame,
            text="⚙️",
            font=("Segoe UI", 32),
            bg=self.bg_color,
            fg="#64748b"
        ).pack(side="left", padx=(0, 10))

        title = tk.Label(
            title_frame,
            text="Settings",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(side="left")

        # Settings card
        card = tk.Frame(container, bg=self.panel_color, relief="flat")
        card.pack(fill="both", expand=True)

        settings_container = tk.Frame(card, bg=self.panel_color)
        settings_container.pack(fill="both", expand=True, padx=30, pady=30)

        # Dark mode toggle
        tk.Label(
            settings_container,
            text="Appearance",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 10))

        dark_mode_var = tk.BooleanVar(value=self.dark_mode)
        dark_mode_check = tk.Checkbutton(
            settings_container,
            text="Dark Mode",
            variable=dark_mode_var,
            command=lambda: self.toggle_dark_mode(dark_mode_var.get()),
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color,
            selectcolor=self.input_bg,
            activebackground=self.panel_color,
            activeforeground=self.text_color
        )
        dark_mode_check.pack(anchor="w", pady=5)

        # Data management
        tk.Label(
            settings_container,
            text="Data Management",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(30, 10))

        export_btn = tk.Button(
            settings_container,
            text="Export CSV",
            font=("Segoe UI", 11),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.export_csv,
            padx=20,
            pady=8
        )
        export_btn.pack(anchor="w", pady=5)

        import_btn = tk.Button(
            settings_container,
            text="Import CSV",
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            activebackground=self.muted_text,
            activeforeground=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.import_csv,
            padx=20,
            pady=8
        )
        import_btn.pack(anchor="w", pady=5)

        # Charts button
        tk.Label(
            settings_container,
            text="Analytics",
            font=("Segoe UI", 16, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(30, 10))

        charts_btn = tk.Button(
            settings_container,
            text="View Charts",
            font=("Segoe UI", 11),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.show_charts,
            padx=20,
            pady=8
        )
        charts_btn.pack(anchor="w", pady=5)

    def toggle_dark_mode(self, value):
        self.dark_mode = value
        self.settings["dark_mode"] = value
        save_settings(self.settings)
        self.update_theme()
        messagebox.showinfo("Theme Changed", "Please restart the app to apply theme changes")

    def export_csv(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return

        workouts = self.data.get(self.current_user, {}).get("workouts", [])

        if not workouts:
            messagebox.showinfo("No Data", "No workouts to export")
            return

        default_filename = f"{self.current_user}_workouts_{datetime.date.today().isoformat()}.csv"
        path = filedialog.asksaveasfilename(
            title="Save workouts as CSV",
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                fieldnames = ["date", "type", "duration_min", "calories", "notes", "created_at"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(workouts)

            messagebox.showinfo("Success", f"Exported {len(workouts)} workouts to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def import_csv(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return

        path = filedialog.askopenfilename(
            title="Select CSV file to import",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not path:
            return

        try:
            imported = 0
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    workout = {
                        "date": row.get("date", ""),
                        "type": row.get("type", ""),
                        "duration_min": int(row.get("duration_min", 0)),
                        "calories": int(row.get("calories", 0)),
                        "notes": row.get("notes", ""),
                        "created_at": row.get("created_at", datetime.datetime.utcnow().isoformat())
                    }

                    self.data[self.current_user].setdefault("workouts", []).append(workout)
                    imported += 1

            save_data(self.data)
            messagebox.showinfo("Success", f"Imported {imported} workouts successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import: {str(e)}")

    def show_charts(self):
        """Show charts in a new window"""
        charts_window = tk.Toplevel(self.root)
        charts_window.title("Analytics")
        charts_window.geometry("900x600")
        charts_window.configure(bg=self.bg_color)

        title = tk.Label(
            charts_window,
            text="Workout Analytics",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=20)

        # Button frame
        btn_frame = tk.Frame(charts_window, bg=self.bg_color)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Weekly Calories",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.plot_weekly_calories(plot_area),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Duration Over Time",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.plot_duration(plot_area),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Done",
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=charts_window.destroy,
            padx=15,
            pady=5
        ).pack(side="left", padx=5)

        # Plot area
        plot_area = tk.Frame(charts_window, bg=self.bg_color)
        plot_area.pack(fill="both", expand=True, padx=20, pady=10)

        # Show weekly calories by default
        self.plot_weekly_calories(plot_area)

    def plot_weekly_calories(self, plot_area):
        # Clear plot area
        for widget in plot_area.winfo_children():
            widget.destroy()

        workouts = self.data.get(self.current_user, {}).get("workouts", [])

        if not workouts:
            tk.Label(
                plot_area,
                text="No data available",
                font=("Segoe UI", 12),
                bg=self.bg_color,
                fg=self.muted_text
            ).pack(pady=50)
            return

        today = datetime.date.today()
        days = [(today - datetime.timedelta(days=i)) for i in reversed(range(7))]
        labels = [d.strftime("%a") for d in days]
        totals = []

        for d in days:
            ds = d.isoformat()
            total = sum(w.get("calories", 0) for w in workouts if w.get("date") == ds)
            totals.append(total)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(labels, totals, color=self.accent_color)
        ax.set_title("Last 7 Days - Calories Burned", fontsize=14, fontweight="bold")
        ax.set_ylabel("Calories (kcal)")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_duration(self, plot_area):
        # Clear plot area
        for widget in plot_area.winfo_children():
            widget.destroy()

        workouts = self.data.get(self.current_user, {}).get("workouts", [])

        if not workouts:
            tk.Label(
                plot_area,
                text="No data available",
                font=("Segoe UI", 12),
                bg=self.bg_color,
                fg=self.muted_text
            ).pack(pady=50)
            return

        sorted_workouts = sorted(workouts, key=lambda x: x.get("date", ""))
        dates = [w.get("date", "") for w in sorted_workouts]
        durations = [w.get("duration_min", 0) for w in sorted_workouts]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(range(len(durations)), durations, marker="o", color=self.accent_color, linewidth=2)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha="right")
        ax.set_title("Workout Duration Over Time", fontsize=14, fontweight="bold")
        ax.set_ylabel("Duration (minutes)")
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def logout(self):
        self.current_user = None
        self.is_logged_in = False
        self.show_login_screen()

    def open_calendar(self, entry_widget):
        # Check if calendar window already exists
        if hasattr(self, 'cal_window') and self.cal_window.winfo_exists():
            self.cal_window.lift()  # Bring existing window to front
            return

        self.cal_window = tk.Toplevel(self.root)
        self.cal_window.title("Select Date")
        self.cal_window.geometry("350x400")
        self.cal_window.configure(bg=self.bg_color)
        self.cal_window.resizable(False, False)
        self.cal_window.grab_set()  # Make it modal

        # Get current date
        try:
            current_date = datetime.datetime.strptime(entry_widget.get(), "%Y-%m-%d").date()
        except:
            current_date = datetime.date.today()

        self.cal_selected_date = current_date
        self.cal_year = current_date.year
        self.cal_month = current_date.month

        # Header with month/year navigation
        header_frame = tk.Frame(self.cal_window, bg=self.panel_color)
        header_frame.pack(fill="x", padx=10, pady=10)

        prev_btn = tk.Button(
            header_frame,
            text="◀",
            font=("Segoe UI", 12),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.change_month(-1, self.cal_window, entry_widget),
            padx=10
        )
        prev_btn.pack(side="left")

        self.month_year_label = tk.Label(
            header_frame,
            text=f"{datetime.date(self.cal_year, self.cal_month, 1).strftime('%B %Y')}",
            font=("Segoe UI", 14, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        )
        self.month_year_label.pack(side="left", expand=True)

        next_btn = tk.Button(
            header_frame,
            text="▶",
            font=("Segoe UI", 12),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.change_month(1, self.cal_window, entry_widget),
            padx=10
        )
        next_btn.pack(side="right")

        # Calendar grid
        self.cal_frame = tk.Frame(self.cal_window, bg=self.panel_color)
        self.cal_frame.pack(padx=10, pady=5)

        self.draw_calendar(entry_widget)

        # Bottom buttons
        btn_frame = tk.Frame(self.cal_window, bg=self.bg_color)
        btn_frame.pack(pady=10)

        today_btn = tk.Button(
            btn_frame,
            text="Today",
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=lambda: self.select_today(entry_widget, self.cal_window),
            padx=15,
            pady=5
        )
        today_btn.pack(side="left", padx=5)

        done_btn = tk.Button(
            btn_frame,
            text="Done",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.cal_window.destroy,
            padx=15,
            pady=5
        )
        done_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            relief="flat",
            cursor="hand2",
            command=self.cal_window.destroy,
            padx=15,
            pady=5
        )
        cancel_btn.pack(side="left", padx=5)

    def draw_calendar(self, entry_widget):
        """Draw the calendar grid"""
        # Clear existing calendar
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(
                self.cal_frame,
                text=day,
                font=("Segoe UI", 9, "bold"),
                bg=self.panel_color,
                fg=self.muted_text,
                width=5
            ).grid(row=0, column=i, padx=2, pady=2)

        # Get calendar for month
        import calendar
        cal = calendar.monthcalendar(self.cal_year, self.cal_month)

        today = datetime.date.today()

        # Draw dates
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    tk.Label(
                        self.cal_frame,
                        text="",
                        bg=self.panel_color,
                        width=5
                    ).grid(row=week_num, column=day_num, padx=2, pady=2)
                else:
                    date_obj = datetime.date(self.cal_year, self.cal_month, day)
                    is_today = (date_obj == today)
                    is_selected = (date_obj == self.cal_selected_date)

                    # Determine button color
                    if is_selected:
                        bg_color = self.accent_color
                        fg_color = "white"
                        font_weight = "bold"
                    elif is_today:
                        bg_color = "#60a5fa"  # Lighter blue for today
                        fg_color = "white"
                        font_weight = "bold"
                    else:
                        bg_color = self.input_bg
                        fg_color = self.text_color
                        font_weight = "normal"

                    btn = tk.Button(
                        self.cal_frame,
                        text=str(day),
                        font=("Segoe UI", 9, font_weight),
                        bg=bg_color,
                        fg=fg_color,
                        relief="flat",
                        cursor="hand2",
                        command=lambda d=day: self.select_date(d, entry_widget),
                        width=5
                    )
                    btn.grid(row=week_num, column=day_num, padx=2, pady=2)

    def change_month(self, delta, cal_window, entry_widget):
        """Change the displayed month"""
        self.cal_month += delta
        if self.cal_month > 12:
            self.cal_month = 1
            self.cal_year += 1
        elif self.cal_month < 1:
            self.cal_month = 12
            self.cal_year -= 1

        self.month_year_label.config(
            text=f"{datetime.date(self.cal_year, self.cal_month, 1).strftime('%B %Y')}"
        )
        self.draw_calendar(entry_widget)

    def select_date(self, day, entry_widget):
        """Select a date from calendar"""
        self.cal_selected_date = datetime.date(self.cal_year, self.cal_month, day)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, self.cal_selected_date.isoformat())
        self.draw_calendar(entry_widget)

    def select_today(self, entry_widget, cal_window):
        """Select today's date and close calendar"""
        today = datetime.date.today()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, today.isoformat())
        cal_window.destroy()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.root.state('zoomed')
        else:
            self.root.state('normal')

    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        self.is_fullscreen = False
        self.root.state('normal')


if __name__ == "__main__":
    try:
        plt.switch_backend("TkAgg")
    except:
        pass

    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()