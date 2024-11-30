import os
import sys
import requests
import zipfile
import shutil
import subprocess

# Constants
GITHUB_RELEASE_URL = "https://github.com/marcinknara/auto-update-python/releases/latest/download/app.zip"
APP_DIR = os.path.dirname(os.path.abspath(__file__))  # Current app directory
TEMP_DIR = os.path.join(APP_DIR, "temp")  # Temporary directory for downloads
BACKUP_DIR = os.path.join(APP_DIR, "backup")  # Backup directory for rollback
APP_ZIP_PATH = os.path.join(TEMP_DIR, "app.zip")

def backup_existing_app():
    """Backup current application files."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for item in os.listdir(APP_DIR):
        if item not in ["backup", "temp", os.path.basename(__file__)]:
            shutil.move(os.path.join(APP_DIR, item), BACKUP_DIR)

def download_new_version():
    """Download the latest version from GitHub."""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    with open(APP_ZIP_PATH, "wb") as file:
        response = requests.get(GITHUB_RELEASE_URL, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def install_new_version():
    """Extract and install the new version."""
    with zipfile.ZipFile(APP_ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(APP_DIR)
    shutil.rmtree(TEMP_DIR)  # Clean up temp files

def restart_main_app():
    """Restart the main application."""
    main_app_path = os.path.join(APP_DIR, "main_app.py")
    subprocess.Popen(["python", main_app_path])
    sys.exit()

def main():
    try:
        print("Backing up existing application...")
        backup_existing_app()

        print("Downloading new version...")
        download_new_version()

        print("Installing new version...")
        install_new_version()

        print("Restarting application...")
        restart_main_app()

    except Exception as e:
        print(f"Update failed: {e}")
        print("Restoring from backup...")
        for item in os.listdir(BACKUP_DIR):
            shutil.move(os.path.join(BACKUP_DIR, item), APP_DIR)
    finally:
        sys.exit()

if __name__ == "__main__":
    main()