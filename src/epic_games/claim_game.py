import requests
from pathlib import Path
import os

from patchright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.epic_games.notification import Notification

FREE_GAMES_API = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

SESSION_FILE = Path("Config/session.json")

COUNTRY = "US"
LOCALE = "en-US"


class ClaimGame:
    def __init__(self):
        self.main()
        self.free_now = []

    def fetch_current_games(self):
        params = {

            "locale": LOCALE,
            "country": COUNTRY,
            "allowCountries": COUNTRY,

        }
        data = requests.get(FREE_GAMES_API, params=params, timeout=30).json()
        games = data["data"]["Catalog"]["searchStore"]["elements"]

        self.free_now = []
        for game in games:
            price = game.get("price" or  {}).get("totalPrice") or {}
            if price.get("discountPrice") == 0 and price.get("originalPrice", 0) > 0:
                mapping = game.get("offerMappings") or game.get("catalogNs", {}).get("mappings", [])
                slug = mapping[0]["pageSlug"] if mapping else game.get("productSlug", "")
                if slug:
                    self.free_now.append({

                        "title": game["title"],
                        "url": f"https://store.epicgames.com/{LOCALE}/p/{slug}",

                    })
        return self.free_now

    def check_if_in_library(self, page):
        for text in ["IN LIBRARY", "In Library", "Owned"]:
            if page.locator(f"text={text}").first.is_visible():
                return True
        return False

    def click_first_visible(self, page, selectors):
        for selector in selectors:
            locator = page.locator(selector).first
            try:
                if locator.is_visible():
                    locator.click()
                    return True
            except PlaywrightTimeoutError:
                continue
        return False

    def click_first_visible_in_frame(self, frame, selectors):
        for selector in selectors:
            locator = frame.locator(selector).first
            try:
                if locator.is_visible():
                    locator.click()
                    return True
            except PlaywrightTimeoutError:
                continue
        return False

    def send_errors(self, game_title, error_message):
        Notification.send_error_msg(game_title, error_message)

    def claim_game(self, page, game):
        print(f"\nClaiming {game['title']}...")

        # 1. Go to game page
        page.goto(game["url"], wait_until="domcontentloaded")

        # 2. If already owned, skip
        if self.check_if_in_library(page):
            self.send_errors(game["title"], "Already In Library, Skipped")
            # print(f"{game['title']} - Already in library, skipping.")
            return

        # 3. Click "Get"
        if not self.click_first_visible(page, [

            "button:has-text('Get')",
            "button:has-text('GET')",

        ]):
            self.send_errors(game["title"], "Could not find Get/Add button.")
            return

        # 4. Wait for the claim popup to load
        page.wait_for_timeout(5000)

        # 5. Continue past the device support warning when it appears
        continue_clicked = False
        for frame in page.frames:
            if self.click_first_visible_in_frame(frame, [

                "button:has-text('Continue')",
                "button:has-text('CONTINUE')",

            ]):
                continue_clicked = True
                break

        if not continue_clicked:
            continue_clicked = self.click_first_visible(page, [

                "button:has-text('Continue')",
                "button:has-text('CONTINUE')",

            ])

        if continue_clicked:
            page.wait_for_timeout(2000)

        # 6. Click "Add to Library" in the popup
        final_clicked = False
        for frame in page.frames:
            if self.click_first_visible_in_frame(frame, [

                "button:has-text('Add to Library')",
                "button:has-text('ADD TO LIBRARY')",
                "button:has-text('Place Order')",
                "button:has-text('PLACE ORDER')",
                "button:has-text('Get')",
                "button:has-text('GET')",

            ]):
                final_clicked = True
                break

        if not final_clicked and self.click_first_visible(page, [

            "button:has-text('Add to Library')",
            "button:has-text('ADD TO LIBRARY')",
            "button:has-text('Place Order')",
            "button:has-text('PLACE ORDER')",
            "button:has-text('Get')",
            "button:has-text('GET')",

        ]):
            final_clicked = True

        if not final_clicked:
            self.send_errors(game["title"], "Could not find the final confirmation button.")
            return

				# 7. Wait for Checkout window
        page.wait_for_timeout(5000)

				# 8 Verfiy the order status
        page.goto(game["url"], wait_until="domcontentloaded")
        if self.check_if_in_library(page):
            print(f"Successfully claimed {game['title']}!")
            Notification.send_game_msg(game)
        else:
            self.send_errors(game["title"], "Order may have failed; game is not in the library.")

    def main(self):
        games = self.fetch_current_games()
        if not games:
            print("No free games found right now.")
            return

        print(f"Found {len(games)} free game(s):")
        for single_game in games:
            print(f"  - {single_game['title']}")

        if not SESSION_FILE.exists():
            self.send_errors("All games", "Session file not found. Please run the login script first.")
            return

        with sync_playwright() as p:
            print("DISPLAY inside script =", os.environ.get("DISPLAY"))
            browser = p.chromium.launch(headless=False, args=[

                "--ozone-platform=x11",
                "--disable-gpu",

            ])
            context = browser.new_context(storage_state=SESSION_FILE)
            page = context.new_page()
            for game in games:
                try:
                    self.claim_game(page, game)
                except Exception as e:
                    self.send_errors(game["title"], str(e))
            browser.close()


if __name__ == "__main__":
    ClaimGame()
