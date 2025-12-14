import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import datetime
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------
# App Constants
# ---------------------------
APP_NAME = "Markyle Fitness Tracker"
DATA_FILE = "users.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "dark_mode": True,
    "sidebar_collapsed": False
}


# ---------------------------
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


def format_duration(minutes):
    h = minutes // 60
    m = minutes % 60
    if h and m:
        return f"{h}h {m}m"
    if h:
        return f"{h}h"
    return f"{m}m"


# ---------------------------
# Main App
# ---------------------------
class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1200x700")

        # Load data
        self.data = load_data()
        self.settings = load_settings()
        self.current_user = None
        self.is_logged_in = False
        self.dark_mode = self.settings.get("dark_mode", True)

        # Apply theme colors
        self.update_theme()

        # Show login screen
        self.show_login_screen()

    def update_theme(self):
        """Update theme colors based on dark_mode setting"""
        if self.dark_mode:
            self.bg_color = "#1a1a1a"
            self.panel_color = "#2d2d2d"
            self.text_color = "white"
            self.muted_text = "#cccccc"
            self.accent_color = "#3b82f6"
            self.accent_hover = "#2563eb"
            self.input_bg = "#404040"
            self.sidebar_bg = "#2d2d2d"
        else:
            self.bg_color = "#f5f5f5"
            self.panel_color = "#ffffff"
            self.text_color = "#1a1a1a"
            self.muted_text = "#666666"
            self.accent_color = "#3b82f6"
            self.accent_hover = "#2563eb"
            self.input_bg = "#e5e5e5"
            self.sidebar_bg = "#ffffff"

        self.root.configure(bg=self.bg_color)

    def show_login_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        # Login card centered
        login_frame = tk.Frame(main_frame, bg=self.panel_color, padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = tk.Label(
            login_frame,
            text="⚡ Markyle Fitness Tracker",
            font=("Segoe UI", 24, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        )
        title.pack(pady=(0, 30))

        # Username
        username_label = tk.Label(
            login_frame,
            text="Username",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        )
        username_label.pack(anchor="w", pady=(0, 5))

        self.username_entry = tk.Entry(
            login_frame,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            relief="flat"
        )
        self.username_entry.pack(pady=(0, 15), ipady=8)

        # Password
        password_label = tk.Label(
            login_frame,
            text="Password",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        )
        password_label.pack(anchor="w", pady=(0, 5))

        self.password_entry = tk.Entry(
            login_frame,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            show="*",
            relief="flat"
        )
        self.password_entry.pack(pady=(0, 10), ipady=8)

        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_cb = tk.Checkbutton(
            login_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            font=("Segoe UI", 9),
            bg=self.panel_color,
            fg=self.muted_text,
            selectcolor=self.input_bg,
            activebackground=self.panel_color,
            activeforeground=self.text_color
        )
        show_password_cb.pack(anchor="w", pady=(0, 20))

        # Login button
        login_btn = tk.Button(
            login_frame,
            text="Login",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.login
        )
        login_btn.pack(fill="x", ipady=10, pady=(0, 15))

        # Register link
        register_btn = tk.Button(
            login_frame,
            text="Don't have an account? Register",
            font=("Segoe UI", 9, "underline"),
            bg=self.panel_color,
            fg="#60a5fa",
            activebackground=self.panel_color,
            activeforeground="#93c5fd",
            relief="flat",
            cursor="hand2",
            command=self.show_register_screen
        )
        register_btn.pack()

        # Bind enter key to login
        self.password_entry.bind("<Return>", lambda e: self.login())

    def show_register_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        # Register card centered
        register_frame = tk.Frame(main_frame, bg=self.panel_color, padx=40, pady=40)
        register_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = tk.Label(
            register_frame,
            text="Create Account",
            font=("Segoe UI", 22, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        )
        title.pack(pady=(0, 30))

        # Username
        tk.Label(
            register_frame,
            text="Username",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))

        self.reg_username = tk.Entry(
            register_frame,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            relief="flat"
        )
        self.reg_username.pack(pady=(0, 15), ipady=8)

        # Password
        tk.Label(
            register_frame,
            text="Password",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))

        self.reg_password = tk.Entry(
            register_frame,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            show="*",
            relief="flat"
        )
        self.reg_password.pack(pady=(0, 15), ipady=8)

        # Confirm Password
        tk.Label(
            register_frame,
            text="Confirm Password",
            font=("Segoe UI", 10),
            bg=self.panel_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(0, 5))

        self.reg_password2 = tk.Entry(
            register_frame,
            font=("Segoe UI", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            show="*",
            relief="flat"
        )
        self.reg_password2.pack(pady=(0, 20), ipady=8)

        # Register button
        register_btn = tk.Button(
            register_frame,
            text="Create Account",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground=self.accent_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.register
        )
        register_btn.pack(fill="x", ipady=10, pady=(0, 15))

        # Back to login link
        back_btn = tk.Button(
            register_frame,
            text="← Back to Login",
            font=("Segoe UI", 9, "underline"),
            bg=self.panel_color,
            fg="#60a5fa",
            activebackground=self.panel_color,
            activeforeground="#93c5fd",
            relief="flat",
            cursor="hand2",
            command=self.show_login_screen
        )
        back_btn.pack()

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

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
        self.show_dashboard()

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
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True)

        # Sidebar
        self.create_sidebar(main_container)

        # Content area
        self.content_frame = tk.Frame(main_container, bg=self.bg_color)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Show dashboard by default
        self.show_dashboard_content()

    def create_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.sidebar_bg, width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo and title
        logo_frame = tk.Frame(sidebar, bg=self.sidebar_bg)
        logo_frame.pack(pady=30, padx=20)

        title = tk.Label(
            logo_frame,
            text="⚡ Markyle Fitness",
            font=("Segoe UI", 16, "bold"),
            bg=self.sidebar_bg,
            fg=self.text_color
        )
        title.pack()

        # Navigation buttons
        nav_frame = tk.Frame(sidebar, bg=self.sidebar_bg)
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
                font=("Segoe UI", 11),
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

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.input_bg))
            btn.bind("<Leave>",
                     lambda e, b=btn: b.config(bg=self.sidebar_bg) if b.cget("bg") != self.accent_color else None)

        # Spacer
        tk.Frame(sidebar, bg=self.sidebar_bg).pack(expand=True)

        # Logout button
        logout_btn = tk.Button(
            sidebar,
            text="Logout",
            font=("Segoe UI", 11),
            bg=self.sidebar_bg,
            fg="#ef4444",
            activebackground=self.input_bg,
            activeforeground="#ef4444",
            relief="flat",
            cursor="hand2",
            command=self.logout
        )
        logout_btn.pack(fill="x", padx=10, pady=20)

    def highlight_nav_button(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.config(bg=self.accent_color, fg="white")
            else:
                btn.config(bg=self.sidebar_bg, fg=self.muted_text)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard_content(self):
        self.highlight_nav_button(0)
        self.clear_content()

        # Container with padding
        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        # Title
        title = tk.Label(
            container,
            text=f"Welcome, {self.current_user}!",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(anchor="w", pady=(0, 20))

        # Stats cards
        stats_frame = tk.Frame(container, bg=self.bg_color)
        stats_frame.pack(fill="x", pady=20)

        workouts = self.data.get(self.current_user, {}).get("workouts", [])
        today = datetime.date.today().isoformat()
        today_workouts = [w for w in workouts if w.get("date") == today]

        total_mins = sum(w.get("duration_min", 0) for w in today_workouts)
        total_cal = sum(w.get("calories", 0) for w in today_workouts)

        stats = [
            ("Total Workouts", str(len(today_workouts)), "#3b82f6"),
            ("Total Minutes", str(total_mins), "#10b981"),
            ("Calories Burned", str(total_cal), "#f59e0b")
        ]

        for title_text, value, color in stats:
            card = tk.Frame(stats_frame, bg=self.panel_color, relief="flat", bd=0)
            card.pack(side="left", padx=(0, 20), ipadx=30, ipady=20)

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
                font=("Segoe UI", 10),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack()

        # Recent activity
        recent_frame = tk.Frame(container, bg=self.panel_color, relief="flat")
        recent_frame.pack(fill="both", expand=True, pady=20)

        tk.Label(
            recent_frame,
            text="Today's Activity",
            font=("Segoe UI", 18, "bold"),
            bg=self.panel_color,
            fg=self.text_color
        ).pack(anchor="w", padx=20, pady=(15, 10))

        if not today_workouts:
            tk.Label(
                recent_frame,
                text="No workouts today. Add your first workout!",
                font=("Segoe UI", 12),
                bg=self.panel_color,
                fg=self.muted_text
            ).pack(anchor="w", padx=20, pady=(0, 15))
        else:
            for workout in today_workouts:
                workout_card = tk.Frame(recent_frame, bg=self.input_bg)
                workout_card.pack(fill="x", padx=20, pady=5)

                info_frame = tk.Frame(workout_card, bg=self.input_bg)
                info_frame.pack(side="left", padx=15, pady=10)

                tk.Label(
                    info_frame,
                    text=workout.get("type", "Workout"),
                    font=("Segoe UI", 14, "bold"),
                    bg=self.input_bg,
                    fg=self.text_color
                ).pack(anchor="w")

                tk.Label(
                    info_frame,
                    text=f"{workout.get('duration_min', 0)} min • {workout.get('calories', 0)} kcal",
                    font=("Segoe UI", 10),
                    bg=self.input_bg,
                    fg=self.muted_text
                ).pack(anchor="w")

    def show_profile_content(self):
        self.highlight_nav_button(1)
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        title = tk.Label(
            container,
            text="Profile Settings",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(anchor="w", pady=(0, 20))

        # Profile card
        card = tk.Frame(container, bg=self.panel_color, relief="flat")
        card.pack(fill="both", expand=True)

        form_container = tk.Frame(card, bg=self.panel_color)
        form_container.pack(fill="both", expand=True, padx=30, pady=30)

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

        title = tk.Label(
            container,
            text="Add New Workout",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(anchor="w", pady=(0, 20))

        # Workout card
        card = tk.Frame(container, bg=self.panel_color, relief="flat")
        card.pack(fill="both", expand=True)

        form_container = tk.Frame(card, bg=self.panel_color)
        form_container.pack(fill="both", expand=True, padx=30, pady=30)

        # Date
        tk.Label(
            form_container,
            text="Date (YYYY-MM-DD)",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.workout_date = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            relief="flat"
        )
        self.workout_date.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.workout_date.insert(0, datetime.date.today().isoformat())

        # Type
        tk.Label(
            form_container,
            text="Workout Type",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg=self.text_color
        ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.workout_type = tk.Entry(
            form_container,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            width=30,
            relief="flat"
        )
        self.workout_type.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Duration
        tk.Label(
            form_container,
            text="Duration (minutes)",
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
            text="Calories (optional)",
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
            workout_type = self.workout_type.get().strip()
            duration = int(self.workout_duration.get().strip())
            calories = int(self.workout_calories.get().strip()) if self.workout_calories.get().strip() else 0
            notes = self.workout_notes.get().strip()

            if not workout_type:
                messagebox.showerror("Error", "Workout type is required")
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

            # Clear fields
            self.workout_type.delete(0, tk.END)
            self.workout_duration.delete(0, tk.END)
            self.workout_calories.delete(0, tk.END)
            self.workout_notes.delete(0, tk.END)
            self.workout_date.delete(0, tk.END)
            self.workout_date.insert(0, datetime.date.today().isoformat())

        except ValueError:
            messagebox.showerror("Error", "Invalid duration or calories value")

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
        export_btn = tk.Button(
            history_window,
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
        export_btn.pack(pady=10)

    def show_settings_content(self):
        self.highlight_nav_button(3)
        self.clear_content()

        container = tk.Frame(self.content_frame, bg=self.bg_color)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        title = tk.Label(
            container,
            text="Settings",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(anchor="w", pady=(0, 20))

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


if __name__ == "__main__":
    try:
        plt.switch_backend("TkAgg")
    except:
        pass

    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()