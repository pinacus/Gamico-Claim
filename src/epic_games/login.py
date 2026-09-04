import json
from pathlib import Path
from patchright.sync_api import sync_playwright


LOGIN_URL = "https://www.epicgames.com/id/login"
SESSION_FILE = Path("Config/session.json")


class Login:
  def __init__(self):
    self.epic_login()

  def epic_login(self):
    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as login_browser:
      browser = login_browser.chromium.launch(headless=False)
      window = browser.new_context()
      new_tab = window.new_page()
      new_tab.goto(LOGIN_URL)
      input("Login Into Browser Manually, Then Press ENTER Here.")
      window.storage_state(path=SESSION_FILE)
      browser.close()

    if SESSION_FILE.is_file():
      with open(SESSION_FILE, "r", encoding="utf-8") as file:
        raw_session = json.load(file)

      with open(SESSION_FILE, "w", encoding="utf-8") as file:
        json.dump(raw_session, file, indent=2, ensure_ascii=False)
        print("Session Saved Successfully")
