import traceback
import os
import requests
import json
# Remove 'get_spytips_cool_signals' if it doesn't exist, only keep what's truly there
from strategies.spytips_cool import spy_tips_cool # Ensure this is the correct function name in spytips_cool.py
from strategies.nvidia import get_nvidia_signals # Assuming this is correct for nvidia.py

def saveText(subject, subject2=None, text=None):
    if not subject and not subject2 and not text:
        return
    d = open('message.txt', 'w')
    if subject:
        d.write(subject + "\n\n")
    if subject2:
        d.write(subject2 + "\n\n")
    if text:
        d.write(text)
    d.close()

# Define the send_discord_message function (make sure this is complete from previous instructions)
def send_discord_message(webhook_url, title, subtitle, text):
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL not set.")
        return

    payload = {
        "embeds": [
            {
                "title": title,
                "description": subtitle,
                "fields": [
                    {
                        "name": "Details",
                        "value": text,
                        "inline": False
                    }
                ],
                "color": 3447003
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"Message sent to Discord successfully for {title}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sending Discord message: {e}")


def main():
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    # --- SPYTIPS Signal Check ---
    # Use spy_tips_cool directly for the signals
    spytips_title, spytips_subtitle, spytips_text = spy_tips_cool()
    if spytips_title: # If spy_tips_cool returns something, send it
        send_discord_message(discord_webhook_url, spytips_title, spytips_subtitle, spytips_text)
    else:
        print("No SPYTIPS signal change to report.")

    # --- NVDA Signal Check ---
    nvda_title, nvda_subtitle, nvda_text = get_nvidia_signals()
    if nvda_title:
        send_discord_message(discord_webhook_url, nvda_title, nvda_subtitle, nvda_text)
    else:
        print("No NVDA signal change to report.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_message = repr(traceback.format_exc())
        print(f"An unhandled error occurred in main: {error_message}")
        saveText("Unhandled Bot Error", error_message)
