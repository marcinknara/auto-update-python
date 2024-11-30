import os
import json
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys

# Determine the base path of the application
if getattr(sys, 'frozen', False):
    # If running from a macOS .app bundle
    if sys.platform == "darwin" and ".app" in os.path.abspath(sys.executable):
        BASE_PATH = os.path.abspath(os.path.join(sys.executable, "../../../.."))
    else:
        # If running from the one-folder mode
        BASE_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # If running directly as a Python script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Paths for local version file and updater executable
LOCAL_VERSION_FILE = os.path.join(BASE_PATH, "version.json")

# Path to the updater folder
UPDATER_EXECUTABLE = os.path.join(BASE_PATH, "update_manager", "update_manager")
if sys.platform == "win32":
    UPDATER_EXECUTABLE += ".exe"

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/marcinknara/auto-update-python/main/version.json"

def check_for_updates():
    try:
        # Fetch the latest version from GitHub
        response = requests.get(GITHUB_VERSION_URL)
        response.raise_for_status()
        remote_version = response.json()["version"]

        # Read the local version
        with open(LOCAL_VERSION_FILE, "r") as file:
            local_version = json.load(file)["version"]

        # Compare versions and trigger the updater if needed
        if remote_version > local_version:
            if messagebox.askyesno("Update Available", "A new version is available. Update now?"):
                # Launch the updater executable
                subprocess.Popen([UPDATER_EXECUTABLE])
                root.destroy()  # Close the main application
        else:
            messagebox.showinfo("Up-to-date", "You are already running the latest version.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to check for updates: {e}")

# Main application GUI
root = tk.Tk()
root.title("Minimal Updater App")

menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Check for Updates", command=check_for_updates)
menubar.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menubar)

tk.Label(root, text="Welcome to the Minimal Updater App! v1.0.4").pack(pady=20)
root.geometry("400x200")
root.mainloop()