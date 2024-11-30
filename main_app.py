import os
import json
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS  # For PyInstaller builds
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

LOCAL_VERSION_FILE = os.path.join(BASE_PATH, "version.json")
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/marcinknara/auto-update-python/main/version.json"
UPDATER_SCRIPT = os.path.join(BASE_PATH, "update_manager.py")

def check_for_updates():
    try:
        response = requests.get(GITHUB_VERSION_URL)
        response.raise_for_status()
        remote_version = response.json()["version"]

        with open(LOCAL_VERSION_FILE, "r") as file:
            local_version = json.load(file)["version"]

        if remote_version > local_version:
            if messagebox.askyesno("Update Available", "A new version is available. Update now?"):
                subprocess.Popen(["python", UPDATER_SCRIPT, remote_version])
                root.destroy()
        else:
            messagebox.showinfo("Up-to-date", "You are already running the latest version.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to check for updates: {e}")

root = tk.Tk()
root.title("Minimal Updater App")

menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Check for Updates", command=check_for_updates)
menubar.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menubar)

tk.Label(root, text="Welcome to the Minimal Updater App!").pack(pady=20)
root.geometry("400x200")
root.mainloop()