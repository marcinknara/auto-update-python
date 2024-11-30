import os
import sys
import requests
import zipfile
import subprocess

# Constants for your GitHub repository
GITHUB_RELEASE_URL = "https://github.com/marcinknara/auto-update-python/releases/latest/download/app.zip"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ZIP_PATH = os.path.join(APP_DIR, "app.zip")

def download_new_version():
    with open(APP_ZIP_PATH, "wb") as file:
        response = requests.get(GITHUB_RELEASE_URL, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def install_new_version():
    with zipfile.ZipFile(APP_ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(APP_DIR)
    os.remove(APP_ZIP_PATH)

def restart_main_app():
    subprocess.Popen(["python", os.path.join(APP_DIR, "main_app.py")])

def main():
    try:
        print("Downloading new version...")
        download_new_version()

        print("Installing new version...")
        install_new_version()

        print("Restarting application...")
        restart_main_app()

    except Exception as e:
        print(f"Update failed: {e}")
    finally:
        sys.exit()

if __name__ == "__main__":
    main()