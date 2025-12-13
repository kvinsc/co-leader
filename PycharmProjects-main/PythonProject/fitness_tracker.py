import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, datetime, csv, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry


# ---------------------------
# Files & app constants
# ---------------------------
APP_NAME = "Markyle Fitness Tracker"
DATA_FILE = "users.json"
SETTINGS_FILE = "settings.json"

# ---------------------------
# Settings utilities
# ---------------------------
DEFAULT_SETTINGS = {
    "dark_mode": True,
    "sidebar_collapsed": False
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            s = json.load(f)
            # ensure defaults
            out = DEFAULT_SETTINGS.copy()
            out.update(s)
            return out
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2)

# ---------------------------
# Data utilities
# ---------------------------
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

# ---------------------------
# Window helper
# ---------------------------
def center_window(win, w=1000, h=650):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = max(0, (sw - w) // 2)
    y = max(0, (sh - h) // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

def format_duration(minutes):
    h = minutes // 60
    m = minutes % 60
    if h and m:
        return f"{h}h {m}m"
    if h:
        return f"{h}h"
    return f"{m}m"

# ---------------------------
# Theme definitions (light/dark)
# ---------------------------
LIGHT = {
    "bg": "#fff7fb",
    "panel": "#ffffff",
    "muted_panel": "#ffeef6",
    "text": "#111111",
    "accent": "#ff6fa3",
    "accent_alt": "#ff82b2",
    "muted_text": "#666666",
    "glass_border": "#e6e6e6",
    "sidebar_bg": "#ffd6e6",
    "sidebar_btn_bg": "#ff82b2",
    "canvas_bg": "#ffffff"
}

DARK = {
    "bg": "#1f1b21",
    "panel": "#2a262b",
    "muted_panel": "#352f34",
    "text": "#f3eef3",
    "accent": "#ff6fa3",
    "accent_alt": "#ff82b2",
    "muted_text": "#bbbbbb",
    "glass_border": "#3a333a",
    "sidebar_bg": "#2b1f24",
    "sidebar_btn_bg": "#4a2230",
    "canvas_bg": "#2a262b"
}

# ---------------------------
# Base page for convenience
# ---------------------------
class BasePage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

    def apply_theme_to_widget(self, widget):
        # implement in subclasses if needed
        pass

# ---------------------------
# Login / Register Pages
# ---------------------------
class LoginPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)

        self.bg = tk.Canvas(self, highlightthickness=0)
        self.bg.pack(fill="both", expand=True)
        self.bg.bind("<Configure>", self.draw_bg)

        self.card = tk.Frame(self.bg)

        tk.Label(self.card, text=APP_NAME, font=("Segoe UI", 22, "bold")).pack(pady=(16, 6))

        tk.Label(self.card, text="Username").pack(anchor="w", padx=24)
        self.ent_user = tk.Entry(self.card)
        self.ent_user.pack(fill="x", padx=24, pady=6)

        tk.Label(self.card, text="Password").pack(anchor="w", padx=24)
        self.ent_pass = tk.Entry(self.card, show="*")
        self.ent_pass.pack(fill="x", padx=24, pady=6)

        self.show_pw = tk.BooleanVar()
        tk.Checkbutton(
            self.card,
            text="Show password",
            variable=self.show_pw,
            command=self.toggle_pw
        ).pack(anchor="w", padx=24, pady=(0, 6))

        tk.Button(
            self.card,
            text="Login",
            width=20,
            command=self.do_login
        ).pack(pady=(8, 4))

        reg = tk.Label(
            self.card,
            text="Don’t have an account? Register",
            cursor="hand2",
            font=("Segoe UI", 9, "underline")
        )
        reg.pack(pady=(4, 12))
        reg.bind("<Button-1>", lambda e: self.app.show_frame("RegisterPage"))

    def toggle_pw(self):
        self.ent_pass.config(show="" if self.show_pw.get() else "*")

    def draw_bg(self, *_):
        t = self.app.theme
        w, h = self.winfo_width(), self.winfo_height()
        self.bg.delete("all")
        self.bg.create_rectangle(0, 0, w, h, fill=t["bg"], outline="")
        self.bg.create_rectangle(0, h * 0.3, w, h, fill=t["muted_panel"], outline="")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380)
        self.card.config(bg=t["panel"])

        for c in self.card.winfo_children():
            try:
                c.config(bg=t["panel"], fg=t["text"])
            except:
                pass

    def do_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Enter username and password")
            return

        user = self.app.data.get(username)
        if not user or user.get("password") != password:
            messagebox.showerror("Login failed", "Invalid credentials")
            return

        self.app.current_user = username
        self.app.show_sidebar()
        self.app.sidebar.update_user(username)
        self.app.show_frame("DashboardPage")


class RegisterPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)

        self.bg = tk.Canvas(self, highlightthickness=0)
        self.bg.pack(fill="both", expand=True)
        self.bg.bind("<Configure>", self.draw_bg)

        self.card = tk.Frame(self.bg)

        tk.Label(self.card, text="Create Account", font=("Segoe UI", 20, "bold")).pack(pady=(16, 6))

        for label, attr in [
            ("Username", "user"),
            ("Password", "pw"),
            ("Confirm Password", "pw2")
        ]:
            tk.Label(self.card, text=label).pack(anchor="w", padx=24)
            e = tk.Entry(self.card, show="*" if "Password" in label else "")
            e.pack(fill="x", padx=24, pady=6)
            setattr(self, f"e_{attr}", e)

        tk.Label(
            self.card,
            text="• 4–8 characters\n• At least 1 number & special character",
            font=("Segoe UI", 8),
            justify="left"
        ).pack(anchor="w", padx=24, pady=(2, 8))

        tk.Button(
            self.card,
            text="Create Account",
            width=20,
            command=self.create_account
        ).pack(pady=(6, 4))

        back = tk.Label(
            self.card,
            text="← Back to Login",
            cursor="hand2",
            font=("Segoe UI", 9, "underline")
        )
        back.pack(pady=(4, 12))
        back.bind("<Button-1>", lambda e: self.app.show_frame("LoginPage"))

    def draw_bg(self, *_):
        t = self.app.theme
        w, h = self.winfo_width(), self.winfo_height()
        self.bg.delete("all")
        self.bg.create_rectangle(0, 0, w, h, fill=t["bg"], outline="")
        self.bg.create_rectangle(0, h * 0.3, w, h, fill=t["muted_panel"], outline="")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=420)
        self.card.config(bg=t["panel"])

        for c in self.card.winfo_children():
            try:
                c.config(bg=t["panel"], fg=t["text"])
            except:
                pass

    def create_account(self):
        u = self.e_user.get().strip()
        p1 = self.e_pw.get().strip()
        p2 = self.e_pw2.get().strip()

        if not u or not p1 or not p2:
            messagebox.showerror("Error", "All fields required")
            return

        if u in self.app.data:
            messagebox.showerror("Error", "Username already exists")
            return

        if p1 != p2:
            messagebox.showerror("Error", "Passwords do not match")
            return

        self.app.data[u] = {
            "password": p1,
            "profile": {},
            "workouts": [],
            "settings": {}
        }

        save_data(self.app.data)
        messagebox.showinfo("Success", "Account created")
        self.app.show_frame("LoginPage")


# ---------------------------
# Sidebar (collapsible)
# ---------------------------
class Sidebar(tk.Frame):
    def __init__(self, master, app, width=220):
        super().__init__(master, width=width)
        self.app = app
        self.place(x=0, y=0, relheight=1)
        self.pack_propagate(False)

        self.btns = {}

        items = [
            ("Dashboard", "DashboardPage"),
            ("Profile", "ProfilePage"),
            ("Workouts", "WorkoutPage"),
            ("Settings", "SettingsPage"),
        ]

        for text, page in items:
            b = tk.Button(
                self, text=text, anchor="w",
                command=lambda p=page: self.app.show_frame(p)
            )
            b.pack(fill="x", padx=10, pady=4)
            self.btns[text] = b

        # Refresh
        self.refresh_btn = tk.Button(
            self, text="↻ Refresh",
            command=self.refresh_dashboard
        )
        self.refresh_btn.pack(fill="x", padx=10, pady=10)

        # Spacer
        tk.Label(self).pack(expand=True)

        # Logout
        tk.Button(
            self, text="Logout",
            fg="red",
            command=self.logout
        ).pack(fill="x", padx=10, pady=10)

        self.apply_theme()

    def refresh_dashboard(self):
        if self.app.current_user:
            self.app.show_frame("DashboardPage", instant=True)

    def update_user(self, username):
        pass

    def apply_theme(self):
        t = self.app.theme
        self.config(bg=t["panel"])
        for b in self.btns.values():
            b.config(bg=t["panel"], fg=t["text"])
        self.refresh_btn.config(bg=t["panel"], fg=t["accent"])

    def logout(self):
        self.app.current_user = None
        self.app.hide_all_pages()
        self.destroy()
        self.app.sidebar = None
        self.app.show_frame("LoginPage", instant=True)


# ---------------------------
# Dashboard page
# ---------------------------
class DashboardPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)

        self.header = tk.Label(
            self, font=("Segoe UI", 18, "bold")
        )
        self.header.pack(anchor="w", padx=30, pady=20)

        self.today = tk.Label(
            self, font=("Segoe UI", 12), justify="left"
        )
        self.today.pack(anchor="w", padx=30)

        self.apply_theme()

    def on_show(self):
        u = self.app.current_user
        if not u:
            return

        self.header.config(text=f"Welcome {u}")

        workouts = self.app.data.get(u, {}).get("workouts", [])
        today = datetime.date.today().isoformat()
        t = [w for w in workouts if w.get("date") == today]

        mins = sum(w.get("duration_min", 0) for w in t)
        kcal = sum(w.get("calories", 0) for w in t)

        self.today.config(
            text=f"Today\nWorkouts: {len(t)}\nDuration: {mins} min\nCalories: {kcal}"
        )

    def apply_theme(self):
        t = self.app.theme
        self.config(bg=t["bg"])
        self.header.config(bg=t["bg"], fg=t["text"])
        self.today.config(bg=t["bg"], fg=t["text"])


# ---------------------------
# Profile Page
# ---------------------------
class ProfilePage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self)
        card.place(relx=0.05, rely=0.12, relwidth=0.9, relheight=0.7)
        tk.Label(card, text="Profile", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=10)
        form = tk.Frame(card); form.pack(padx=12, pady=6)
        labels = ["Name","Age","Weight (kg)","Height (cm)","Daily Calorie Goal","Activity Level"]
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(form, text=lab).grid(row=i, column=0, sticky="e", padx=6, pady=6)
            e = tk.Entry(form)
            e.grid(row=i, column=1, padx=6, pady=6)
            self.entries[lab] = e
        self.save_btn = tk.Button(card, text="Save Profile", command=self.save_profile)
        self.save_btn.pack(pady=10)
        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])
        for child in self.winfo_children():
            try:
                child.config(bg=theme["panel"])
            except:
                pass
        for lbl_e in self.entries.values():
            lbl_e.config(bg=theme["panel"], fg=theme["text"], insertbackground=theme["text"])
        self.save_btn.config(bg=theme["accent"], fg="white", bd=0)

    def on_show(self):
        uid = self.app.current_user
        if not uid: return
        p = self.app.data.get(uid, {}).get("profile", {})
        mapping = [("Name","name"),("Age","age"),("Weight (kg)","weight"),("Height (cm)","height"),("Daily Calorie Goal","goal"),("Activity Level","activity")]
        for label, key in mapping:
            self.entries[label].delete(0, tk.END)
            self.entries[label].insert(0, str(p.get(key, "")))

    def save_profile(self):
        uid = self.app.current_user
        if not uid: return
        mapping = [("Name","name"),("Age","age"),("Weight (kg)","weight"),("Height (cm)","height"),("Daily Calorie Goal","goal"),("Activity Level","activity")]
        for label, key in mapping:
            self.app.data[uid].setdefault("profile", {})[key] = self.entries[label].get().strip()
        save_data(self.app.data)
        messagebox.showinfo("Saved", "Profile saved!")

# ---------------------------
# Workout Page
# ---------------------------
class WorkoutPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self)
        card.place(relx=0.08, rely=0.08, relwidth=0.84, relheight=0.8)
        tk.Label(card, text="Add Workout", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=10)
        form = tk.Frame(card); form.pack(padx=12, pady=4)
        tk.Label(form, text="Date").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.ent_date = DateEntry(form, width=14, background='pink',
                                  foreground='white', date_pattern='yyyy-mm-dd')
        self.ent_date.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(form, text="Type").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.ent_type = tk.Entry(form); self.ent_type.grid(row=1, column=1, padx=6, pady=6)
        tk.Label(form, text="Hours").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        self.spin_h = tk.Spinbox(form, from_=0, to=99, width=6); self.spin_h.grid(row=2, column=1, sticky="w", padx=6, pady=6)
        tk.Label(form, text="Minutes").grid(row=2, column=1, sticky="e")
        self.spin_m = tk.Spinbox(form, from_=0, to=59, width=6); self.spin_m.grid(row=2, column=1, sticky="e", padx=(0,6), pady=6)
        tk.Label(form, text="Calories (optional)").grid(row=3, column=0, sticky="e", padx=6, pady=6)
        self.ent_cal = tk.Entry(form); self.ent_cal.grid(row=3, column=1, padx=6, pady=6)
        tk.Label(form, text="Notes (optional)").grid(row=4, column=0, sticky="e", padx=6, pady=6)
        self.ent_notes = tk.Entry(form); self.ent_notes.grid(row=4, column=1, padx=6, pady=6)
        btns = tk.Frame(card); btns.pack(pady=12)
        tk.Button(btns, text="Save Workout", command=self.save_workout).pack(side="left", padx=8)
        tk.Button(btns, text="Back", command=lambda: self.app.show_frame("DashboardPage")).pack(side="left", padx=8)

    def save_workout(self):
        uid = self.app.current_user
        if not uid:
            messagebox.showerror("Error", "Please login first"); return
        date_in = self.ent_date.get().strip()
        if date_in == "":
            date_s = datetime.date.today().isoformat()
        else:
            try:
                date_s = datetime.datetime.strptime(date_in, "%Y-%m-%d").date().isoformat()
            except:
                messagebox.showerror("Error", "Date must be YYYY-MM-DD"); return
        typ = self.ent_type.get().strip()
        if not typ:
            messagebox.showerror("Error", "Type required"); return
        try:
            h = int(self.spin_h.get()); m = int(self.spin_m.get())
            if h < 0 or m < 0 or m >= 60:
                raise ValueError
            mins = h*60 + m
        except:
            messagebox.showerror("Error", "Invalid duration"); return
        try:
            calories = int(self.ent_cal.get().strip()) if self.ent_cal.get().strip() else 0
        except:
            messagebox.showerror("Error", "Calories must be integer"); return
        notes = self.ent_notes.get().strip()
        created_at = datetime.datetime.utcnow().isoformat()
        self.app.data.setdefault(uid, {"password":"", "profile":{}, "workouts":[], "settings":{}})
        self.app.data[uid].setdefault("workouts", []).append({
            "date": date_s,
            "type": typ,
            "duration_min": mins,
            "calories": calories,
            "notes": notes,
            "created_at": created_at
        })
        save_data(self.app.data)
        messagebox.showinfo("Saved", "Workout saved")
        # clear fields
        self.ent_type.delete(0, tk.END)
        self.spin_h.delete(0, "end"); self.spin_h.insert(0, 0)
        self.spin_m.delete(0, "end"); self.spin_m.insert(0, 0)
        self.ent_cal.delete(0, tk.END); self.ent_notes.delete(0, tk.END)
        self.app.show_frame("DashboardPage")

# ---------------------------
# EditWorkoutDialog
# ---------------------------
class EditWorkoutDialog(tk.Toplevel):
    def __init__(self, parent, workout, on_saved=None):
        super().__init__(parent)
        self.workout = workout
        self.on_saved = on_saved
        self.title("Edit Workout")
        center_window(self, 420, 340)
        self.resizable(False, False)
        frame = tk.Frame(self, bd=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=280)
        tk.Label(frame, text="Edit Workout", font=("Segoe UI", 14, "bold")).pack(pady=8)
        inner = tk.Frame(frame); inner.pack(pady=6)
        tk.Label(inner, text="Date").grid(row=0, column=0, padx=6, pady=4)
        self.e_date = tk.Entry(inner); self.e_date.grid(row=0, column=1, padx=6, pady=4); self.e_date.insert(0, workout.get("date",""))
        tk.Label(inner, text="Type").grid(row=1, column=0, padx=6, pady=4)
        self.e_type = tk.Entry(inner); self.e_type.grid(row=1, column=1, padx=6, pady=4); self.e_type.insert(0, workout.get("type",""))
        mins = workout.get("duration_min",0); h = mins//60; m = mins%60
        tk.Label(inner, text="Hours").grid(row=2, column=0, padx=6, pady=4)
        self.e_h = tk.Spinbox(inner, from_=0, to=99, width=6); self.e_h.grid(row=2, column=1, sticky="w"); self.e_h.delete(0,"end"); self.e_h.insert(0,h)
        tk.Label(inner, text="Minutes").grid(row=3, column=0, padx=6, pady=4)
        self.e_m = tk.Spinbox(inner, from_=0, to=59, width=6); self.e_m.grid(row=3, column=1, sticky="w"); self.e_m.delete(0,"end"); self.e_m.insert(0,m)
        tk.Label(inner, text="Calories").grid(row=4, column=0, padx=6, pady=4)
        self.e_cal = tk.Entry(inner); self.e_cal.grid(row=4, column=1, padx=6, pady=4); self.e_cal.insert(0, str(workout.get("calories",0)))
        tk.Label(inner, text="Notes").grid(row=5, column=0, padx=6, pady=4)
        self.e_notes = tk.Entry(inner); self.e_notes.grid(row=5, column=1, padx=6, pady=4); self.e_notes.insert(0, workout.get("notes",""))
        tk.Button(frame, text="Save", command=self.save).pack(pady=8)


    def save(self):
        try:
            date_s = datetime.datetime.strptime(self.e_date.get().strip(), "%Y-%m-%d").date().isoformat()
        except:
            messagebox.showerror("Error", "Date must be YYYY-MM-DD"); return
        typ = self.e_type.get().strip()
        try:
            h = int(self.e_h.get()); m = int(self.e_m.get())
            if h < 0 or m < 0 or m >= 60:
                raise ValueError
            mins = h*60 + m
        except:
            messagebox.showerror("Error", "Invalid duration"); return
        try:
            cal = int(self.e_cal.get().strip()) if self.e_cal.get().strip() else 0
        except:
            messagebox.showerror("Error", "Calories must be integer"); return
        notes = self.e_notes.get().strip()
        app = self.master.master
        uid = app.current_user
        if not uid:
            self.destroy(); return
        for w in app.data[uid].get("workouts", []):
            if w.get("created_at") == self.workout.get("created_at"):
                w["date"] = date_s; w["type"] = typ; w["duration_min"] = mins; w["calories"] = cal; w["notes"] = notes
                break
        save_data(app.data)
        if self.on_saved: self.on_saved()
        self.destroy()

# ---------------------------
# History Page
# ---------------------------
class HistoryPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self); card.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.8)
        tk.Label(card, text="History", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=8)
        self.tree = ttk.Treeview(card, columns=("date","type","duration","calories","notes"), show="headings", height=14)
        for col in ("date","type","duration","calories","notes"):
            self.tree.heading(col, text=col.capitalize()); self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, padx=12, pady=8)
        ctrl = tk.Frame(card); ctrl.pack(pady=6)
        tk.Button(ctrl, text="Refresh", command=self.load).pack(side="left", padx=6)
        tk.Button(ctrl, text="Edit Selected", command=self.edit_selected).pack(side="left", padx=6)
        tk.Button(ctrl, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=6)
        tk.Button(ctrl, text="Export CSV", command=self.export_csv).pack(side="left", padx=6)
        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])
        for child in self.winfo_children():
            try:
                child.config(bg=theme["panel"])
            except:
                pass

    def on_show(self):
        self.load()

    def load(self):
        self.tree.delete(*self.tree.get_children())
        uid = self.app.current_user
        if not uid: return
        rows = sorted(self.app.data.get(uid, {}).get("workouts", []), key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        for w in rows:
            self.tree.insert("", "end", values=(w.get("date"), w.get("type"), format_duration(w.get("duration_min",0)), w.get("calories",0), w.get("notes","")))

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error", "Select a row"); return
        idx = self.tree.index(sel[0])
        uid = self.app.current_user
        rows = sorted(self.app.data.get(uid, {}).get("workouts", []), key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        workout = rows[idx]
        EditWorkoutDialog(self, workout, on_saved=self.load)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error","Select row"); return
        idx = self.tree.index(sel[0])
        uid = self.app.current_user
        rows = sorted(self.app.data.get(uid, {}).get("workouts", []), key=lambda x: (x.get("date",""), x.get("created_at","")), reverse=True)
        workout = rows[idx]
        allw = self.app.data[uid]["workouts"]
        for i,w in enumerate(allw):
            if w.get("created_at") == workout.get("created_at"):
                del allw[i]; save_data(self.app.data); break
        self.load()

    def export_csv(self):
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        rows = self.app.data[uid].get("workouts", [])
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["date","type","duration_min","calories","notes","created_at"])
            for r in rows:
                w.writerow([r.get("date"), r.get("type"), r.get("duration_min"), r.get("calories"), r.get("notes"), r.get("created_at")])
        messagebox.showinfo("Exported", f"Saved to {path}")

# ---------------------------
# Charts Page
# ---------------------------
class ChartPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)
        card = tk.Frame(self); card.place(relx=0.05, rely=0.08, relwidth=0.9, relheight=0.84)
        tk.Label(card, text="Charts & Progress", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=8)
        btns = tk.Frame(card); btns.pack(pady=6)
        tk.Button(btns, text="Weekly Calories (last 7 days)", command=self.weekly_calories).pack(side="left", padx=6)
        tk.Button(btns, text="Calories per Workout", command=self.calories_per_workout).pack(side="left", padx=6)
        tk.Button(btns, text="Duration over Time", command=self.duration_over_time).pack(side="left", padx=6)
        self.plot_area = tk.Frame(card); self.plot_area.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas = None
        self.apply_theme()

    def apply_theme(self):
        theme = self.app.theme
        self.config(bg=theme["bg"])

    def _clear_plot(self):
        if self.canvas:
            try:
                self.canvas.get_tk_widget().destroy()
            except:
                pass
            self.canvas = None

    def weekly_calories(self):
        self._clear_plot()
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        now = datetime.date.today()
        days = [(now - datetime.timedelta(days=i)) for i in reversed(range(7))]
        labels = [d.strftime("%a") for d in days]
        totals = []
        for d in days:
            ds = d.isoformat()
            t = sum(w.get("calories",0) for w in self.app.data[uid].get("workouts", []) if w.get("date") == ds)
            totals.append(t)
        fig, ax = plt.subplots(figsize=(9,4))
        ax.bar(labels, totals, color=self.app.theme["accent"])
        ax.set_title("Last 7 days — Calories")
        ax.set_ylabel("kcal")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_area); self.canvas.draw(); self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def calories_per_workout(self):
        self._clear_plot()
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        rows = sorted(self.app.data[uid].get("workouts", []), key=lambda x: x.get("date",""))
        if not rows:
            messagebox.showinfo("No Data","No workouts yet"); return
        labels = [w.get("date") for w in rows]; vals = [w.get("calories",0) for w in rows]
        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(range(len(vals)), vals, marker="o", color=self.app.theme["accent"])
        ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_title("Calories per workout"); ax.set_ylabel("kcal")
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_area); self.canvas.draw(); self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def duration_over_time(self):
        self._clear_plot()
        uid = self.app.current_user
        if not uid: messagebox.showerror("Error","Login required"); return
        rows = sorted(self.app.data[uid].get("workouts", []), key=lambda x: x.get("date",""))
        if not rows:
            messagebox.showinfo("No Data","No workouts yet"); return
        labels = [w.get("date") for w in rows]; vals = [w.get("duration_min",0) for w in rows]
        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(range(len(vals)), vals, marker="o", color=self.app.theme["accent_alt"])
        ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_title("Duration over time (minutes)"); ax.set_ylabel("minutes")
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_area); self.canvas.draw(); self.canvas.get_tk_widget().pack(fill="both", expand=True)

# ---------------------------
# Settings Page
# ---------------------------
def import_from_csv(app):
    pass


def export_to_csv(app):
    pass


class SettingsPage(BasePage):
    def __init__(self, master, app):
        super().__init__(master, app)

        # ===== TITLE =====
        self.title = tk.Label(
            self, text="Settings",
            font=("Segoe UI", 18, "bold")
        )
        self.title.pack(anchor="w", padx=30, pady=(20, 10))

        # ===== BUTTON BAR =====
        self.btn_bar = tk.Frame(self)
        self.btn_bar.pack(anchor="w", padx=30, pady=10)

        self.btn_history = tk.Button(
            self.btn_bar, text="History",
            width=12, command=self.show_history
        )
        self.btn_history.pack(side="left", padx=4)

        self.btn_charts = tk.Button(
            self.btn_bar, text="Charts",
            width=12, command=self.show_charts
        )
        self.btn_charts.pack(side="left", padx=4)

        # ===== CONTENT AREA =====
        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True, padx=30, pady=10)

        # ===== SYSTEM SETTINGS (PERSISTENT) =====
        self.sys_frame = tk.Frame(self)
        self.sys_frame.pack(fill="x", padx=30, pady=(10, 0))

        self.dark_var = tk.BooleanVar(
            value=self.app.settings.get("dark_mode", True)
        )

        self.dark_toggle = tk.Checkbutton(
            self.sys_frame,
            text="Dark Mode",
            variable=self.dark_var,
            command=self.toggle_dark
        )
        self.dark_toggle.pack(anchor="w", pady=4)

        self.btn_export = tk.Button(
            self.sys_frame,
            text="Export CSV",
            command=self.export_csv
        )
        self.btn_export.pack(anchor="w", pady=4)

        self.btn_import = tk.Button(
            self.sys_frame,
            text="Import CSV",
            command=self.import_csv
        )
        self.btn_import.pack(anchor="w", pady=4)

        # ===== BACK BUTTON =====
        self.back_btn = tk.Button(
            self, text="Back to Dashboard",
            command=lambda: self.app.show_frame("DashboardPage")
        )
        self.back_btn.pack(pady=20)

        self.canvas = None
        self.apply_theme()

    # -------------------------
    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    # -------------------------
    def show_history(self):
        self.clear_content()

        u = self.app.current_user
        if not u:
            return

        tk.Label(
            self.content,
            text="Workout History",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=10)

        workouts = self.app.data[u].get("workouts", [])
        if not workouts:
            tk.Label(self.content, text="No history available").pack(anchor="w")
            return

        for w in reversed(workouts):
            tk.Label(
                self.content,
                text=f"{w.get('date')} | {w.get('duration_min')} min | {w.get('calories')} kcal",
                anchor="w"
            ).pack(anchor="w", pady=2)

    # -------------------------
    def show_charts(self):
        self.clear_content()

        u = self.app.current_user
        if not u:
            return

        tk.Label(
            self.content,
            text="Weekly Calories",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=10)

        today = datetime.date.today()
        days = []
        values = []

        for i in range(7):
            d = today - datetime.timedelta(days=6 - i)
            days.append(d.strftime("%a"))
            values.append(
                sum(
                    w.get("calories", 0)
                    for w in self.app.data[u]["workouts"]
                    if w.get("date") == d.isoformat()
                )
            )

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(days, values, marker="o")
        ax.set_ylim(bottom=0)
        ax.set_title("Calories Burned")

        self.canvas = FigureCanvasTkAgg(fig, self.content)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # -------------------------
    def toggle_dark(self):
        self.app.settings["dark_mode"] = self.dark_var.get()
        self.app.apply_theme_all()

    # -------------------------
    def export_csv(self):
        export_to_csv(self.app)

    def import_csv(self):
        import_from_csv(self.app)

    # -------------------------
    def apply_theme(self):
        t = self.app.theme
        self.config(bg=t["bg"])
        self.btn_bar.config(bg=t["bg"])
        self.content.config(bg=t["bg"])
        self.sys_frame.config(bg=t["bg"])

        for w in (
            self.title, self.back_btn,
            self.dark_toggle, self.btn_export, self.btn_import
        ):
            w.config(bg=t["bg"], fg=t["text"])



# ---------------------------
# Main App (handles animated transitions & theme)
# ---------------------------
class MKApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)

        self.data = load_data()
        self.settings = load_settings()
        self.current_user = None
        self.theme = DARK if self.settings.get("dark_mode", True) else LIGHT

        center_window(self, 1000, 650)

        # MAIN AREA
        self.main_area = tk.Frame(self)
        self.main_area.place(x=0, y=0, relwidth=1, relheight=1)

        # SIDEBAR (HIDDEN UNTIL LOGIN)
        self.sidebar = None

        # PAGES
        self.pages = {}
        page_classes = {
            "LoginPage": LoginPage,
            "RegisterPage": RegisterPage,
            "DashboardPage": DashboardPage,
            "ProfilePage": ProfilePage,
            "WorkoutPage": WorkoutPage,
            "SettingsPage": SettingsPage
        }

        for name, cls in page_classes.items():
            p = cls(self.main_area, self)
            p.place(x=1200, y=0, width=1000, relheight=1)
            self.pages[name] = p

        protected = {
            "DashboardPage", "ProfilePage", "WorkoutPage",
            "HistoryPage", "ChartPage", "SettingsPage"
        }

        if name in protected and not self.current_user:
            name = "LoginPage"

        # SHOW LOGIN ONLY
        self.show_frame("LoginPage", instant=True)

    # --------------------
    # SIDEBAR CONTROL
    # --------------------
    def show_sidebar(self):
        if self.sidebar is None:
            self.sidebar = Sidebar(self, self, width=220)
            self.sidebar.is_collapsed = self.settings.get("sidebar_collapsed", False)
            self.sidebar.apply_theme()

    def hide_sidebar(self):
        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None

    def hide_all_pages(self):
        for p in self.pages.values():
            p.place_forget()
    # --------------------
    # THEME
    # --------------------
    def apply_theme_all(self):
        self.theme = DARK if self.settings.get("dark_mode", True) else LIGHT
        if self.sidebar:
            self.sidebar.apply_theme()
        for p in self.pages.values():
            if hasattr(p, "apply_theme"):
                try:
                    p.apply_theme()
                except:
                    pass
        save_settings(self.settings)

    # --------------------
    # PAGE NAVIGATION
    # --------------------
    def show_frame(self, name, instant=False):
        # 🔒 PROTECT PAGES
        protected = {
            "DashboardPage", "ProfilePage", "WorkoutPage",
            "HistoryPage", "ChartPage", "SettingsPage"
        }

        if name in protected and not self.current_user:
            name = "LoginPage"

        page = self.pages[name]

        if hasattr(page, "on_show"):
            try:
                page.on_show()
            except:
                pass

        sidebar_w = self.sidebar.winfo_width() if self.sidebar else 0
        total_w = self.winfo_width() or 1000
        page_w = total_w - sidebar_w

        start_x = -page_w
        target_x = sidebar_w

        page.place_configure(x=start_x, y=0, width=page_w, relheight=1)
        page.lift()

        if instant:
            page.place_configure(x=target_x)
            return

        steps = 25
        dx = (target_x - start_x) / steps
        cur = start_x

        def slide():
            nonlocal cur
            cur += dx
            if cur >= target_x:
                page.place_configure(x=target_x)
                return
            page.place_configure(x=int(cur))
            self.after(10, slide)

        slide()


if __name__ == "__main__":
    try:
        plt.switch_backend("TkAgg")
    except:
        pass

    app = MKApp()
    app.apply_theme_all()
    app.mainloop()
