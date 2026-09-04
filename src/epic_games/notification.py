import json
import os

import requests
from pathlib import Path
from datetime import datetime, timezone

RAWG_API_KEY = os.getenv("RAWG_API_KEY", "")
DISCORD_WEBHOOK = Path("Config/discord.json")


class Notification:
	@staticmethod
	def send_game_msg(game_info_item, show_status=True):
		with open(DISCORD_WEBHOOK, "r", encoding="utf-8") as file:
			data = json.load(file)

		discord_webhook = data.get("Discord WEBHOOK URL")
		game_name = game_info_item["title"]
		game_url = game_info_item["url"]

		search_url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={game_name}"
		response = requests.get(search_url).json()

		if not response.get("results"):
			print(f"Game '{game_name}' not found.")
			return

		game = response["results"][0]
		title = game.get("name")
		image_url = game.get("background_image")
		rating = game.get("rating", "N/A")
		released = game.get("released", "N/A")
		genres = ", ".join(g["name"] for g in game.get("genres", [])) or "N/A"

		fields = [

			{"name": "⭐ Rating", "value": f"{rating}/5", "inline": True},
			{"name": "📅 Released", "value": str(released), "inline": True},
			{"name": "🏷️ Genres", "value": genres, "inline": False},

		]

		if show_status:
			fields.append({

				"name": "Status",
				"value": f"Claimed, [Checkout]({game_url})",
				"inline": False

			})

		payload = {

			"embeds": [{

				"title": title,
				"color": 13582707,
				"fields": fields,
				"image": {"url": image_url},
				"timestamp": datetime.now(timezone.utc).isoformat(),

			}]

		}

		result = requests.post(discord_webhook, json=payload)
		if result.status_code == 204:
			print(f"Successfully sent claim alert for '{title}'!")
		else:
			print(f"Failed to send claim notification: {result.status_code} - {result.text}")

	@staticmethod
	def send_error_msg(game_title, error_message):
		with open(DISCORD_WEBHOOK, "r", encoding="utf-8") as file:
			data = json.load(file)

		discord_webhook = data.get("Discord WEBHOOK URL")
		payload = {

			"embeds": [
				{

					"title": "Game Claim Error",
					"color": 13582707,
					"fields": [

						{"name": "Game", "value": game_title, "inline": False},
						{"name": "Error", "value": error_message, "inline": False},

					],
					"timestamp": datetime.now(timezone.utc).isoformat(),

				}
			]
   
		}

		requests.post(discord_webhook, json=payload)
