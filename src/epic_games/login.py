from typing import Any

from patchright.sync_api import sync_playwright

from src.config import load_config, save_config

LOGIN_URL = "https://www.epicgames.com/id/login"


class Login:
  def __init__(self):
    self.epic_login()

  def epic_login(self):
    with sync_playwright() as login_browser:
      browser = login_browser.chromium.launch(headless=False)
      window = browser.new_context()
      new_tab = window.new_page()
      new_tab.goto(LOGIN_URL)
      input("Login Into Browser Manually, Then Press ENTER Here.")
      session: Any = window.storage_state()
      browser.close()

    config = load_config()
    config["Session"] = session
    save_config(config)
    print("Session Saved Successfully")
