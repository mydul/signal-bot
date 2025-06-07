import traceback
import os
import requests
import json
from strategies.spytips_cool import get_spytips_cool_signals
from strategies.nvidia import get_nvidia_signals # Corrected import to match function name
from strategies.spytips_cool import spy_tips_cool # Keep if spy_tips_cool() is used elsewhere

def saveText(subject, subject2=None, text=None):
    if not subject and not subject2 and not text: # Added text check for clarity
        return
    # This part seems to be for saving to a local file, which is separate from Discord
    # If you only want Discord messages, this function might not be needed for the bot's primary operation
    d = open('message.txt', 'w')
    if subject:
        d.write(subject + "\n\n")
    if subject2:
        d.write(subject2 + "\n\n")
    if text:
        d.write(text)
    d.close()

# IMPORTANT: Define the send_discord_message function correctly
# This function was missing its implementation in your provided snippet.
# Here's a standard way to implement it:
def send_discord_message(webhook_url, title, subtitle, text):
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL not set.")
        return

    # Discord webhook payload structure
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
                "color": 3447003 # A common color (blue) for embeds
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        print(f"Message sent to Discord successfully for {title}")
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else {err}")
    except Exception as e:
        print(f"An unexpected error occurred while sending Discord message: {e}")


# This is the single, correct main function
def main():
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    # --- SPYTIPS Signal Check ---
    # Call the original spytips_cool() if it's meant to trigger the saveText or similar.
    # If the intention is to use get_spytips_cool_signals for Discord, then use that.
    # Based on the original text, get_spytips_cool_signals() is for Discord.
    spytips_title, spytips_subtitle, spytips_text = get_spytips_cool_signals()
    if spytips_title: # Only send if there's a message to send (title is not None)
        send_discord_message(discord_webhook_url, spytips_title, spytips_subtitle, spytips_text)
    else:
        print("No SPYTIPS signal change to report.")

    # --- Add NVDA Signal Check ---
    # Ensure your strategies/nvidia.py has a function named get_nvidia_signals
    # that returns (title, subtitle, text) or (None, None, None)
    nvda_title, nvda_subtitle, nvda_text = get_nvidia_signals()
    if nvda_title: # Only send if there's a message to send (title is not None)
        send_discord_message(discord_webhook_url, nvda_title, nvda_subtitle, nvda_text)
    else:
        print("No NVDA signal change to report.")

# This ensures main() is called when the script runs
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_message = repr(traceback.format_exc()) # Use format_exc() for full traceback
        print(f"An unhandled error occurred in main: {error_message}")
        # You could also send this error to Discord if you want
        # send_discord_message(os.getenv("DISCORD_WEBHOOK_URL"), "Bot Error", "Unhandled Exception", error_message)
        saveText("Unhandled Bot Error", error_message) # If you want to log to file
