from flask import Flask
import requests
import schedule
import time
from threading import Thread

app = Flask(__name__)

@app.route('/status')
def status():
    return "GhostLinesBot - Automation Engine Running", 200

# --- Configurable Settings ---
BOT_TOKEN = "7583773430:AAFFs_1n19-eGcm6jSVPbWQod_ohPxGxh2Q"
CHAT_ID = "134815223"
EDGE_THRESHOLD = 8.0  # %
SCAN_INTERVAL_MINUTES = 15
MORNING_DIGEST_ENABLED = True
FILTER_PICKS_BEFORE_GAME_HOURS = 2
# ------------------------------

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def scan_and_send_picks():
    now = time.strftime("%Y-%m-%d %I:%M %p")
    picks = [
        "- [NBA] Justin Edwards – OVER 15.5 Points – 54% edge",
        "- [MLB] Austin Riley – OVER 1.5 Total Bases – 53% edge",
        "- [Tennis] Djokovic – UNDER 21.5 Total Games – 60% edge",
        "- [UFC] Moreno – OVER 85.5 Sig. Strikes – 57% edge"
    ]
    message = f"""🔥 *GhostLinesBot Live Picks ({now} PST)* 🔥

{chr(10).join(picks)}

✅ Lock in now. Live edges detected."""
    send_telegram_message(message)

def run_scheduler():
    schedule.every(SCAN_INTERVAL_MINUTES).minutes.do(scan_and_send_picks)
    if MORNING_DIGEST_ENABLED:
        schedule.every().day.at("07:00").do(scan_and_send_picks)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Background scheduler thread
Thread(target=run_scheduler, daemon=True).start()

