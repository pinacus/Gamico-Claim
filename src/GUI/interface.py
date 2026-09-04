from pathlib import Path
from PIL import Image
import customtkinter
import json
from CTkMessagebox import CTkMessagebox

from src.epic_games.login import Login

customtkinter.set_appearance_mode("dark")

IMG_PATH = Path("assets")
USER_CONFIG_DATA = Path("Config/discord.json")
CHECK_SESSION_FILE = Path("Config/session.json")

class GUI(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    self.title("Gamico Claim")
    self.geometry("620x620")
    self.resizable(False, False)
    self.interface()

  def login_popup(self, event=None):
    Login()
    self.update_account_status()

  def open_webhook_dialog(self):
    dialog = customtkinter.CTkInputDialog(

        text="Enter your Discord WEBhook URL",
        title="Discord Webhook"

    )

    webhook_url = dialog.get_input()
    if webhook_url:
      data_format = {

          "Discord WEBHOOK URL": webhook_url.strip()

        }

      with open(USER_CONFIG_DATA, "w", encoding="utf-8") as file:
        json.dump(data_format, file, indent=4)

      CTkMessagebox(

            title="Success",
            message="Saved Successfully",
            icon="check"

      )
      self.update_account_status()

    if not webhook_url:
      CTkMessagebox(

            title="Error",
            message="Kindly Fill The Detail",
            icon="warning"

      )

  def interface(self):
    container = customtkinter.CTkFrame(self, corner_radius=20, fg_color="#CF4173")
    container.pack(fill="both", expand=True, padx=20, pady=20)

    logo = Image.open(f"{IMG_PATH}/logo.png")
    self.logo_image = customtkinter.CTkImage(

            light_image=logo,
            dark_image=logo,
            size=(175, 175),

    )

    logo_label = customtkinter.CTkLabel(container, text="", image=self.logo_image, cursor="hand2")
    logo_label.pack(pady=(50,0), padx=(0, 30))
    logo_label.bind("<Button-1>", self.login_popup)

    self.account_label = customtkinter.CTkLabel(container, text="")
    self.account_label.pack(pady=(20, 0), padx=(10, 0))
    self.update_account_status()

    top_space = customtkinter.CTkLabel(container, text="")
    top_space.pack(pady=(0,0))

    self.option_var = customtkinter.StringVar(value="Select an option",)
    self.discord_button = customtkinter.CTkButton(

      container,
      text="Discord",
      width=125,
      height=30,
      corner_radius=50,
      fg_color="#F6D8BD",
      text_color="black",
      hover_color="#F39399",
      command=self.open_webhook_dialog

    )

    self.discord_button.pack(pady=(10, 20))

  def update_account_status(self):
    session_status = "active.png" if (

        CHECK_SESSION_FILE.is_file() and USER_CONFIG_DATA.is_file()

    ) else "inactive.png"

    session_img = Image.open(f"{IMG_PATH}/{session_status}")
    self.current_session_img = customtkinter.CTkImage(

        dark_image=session_img,
        size=(30, 30)
        
    )
    self.account_label.configure(image=self.current_session_img)
