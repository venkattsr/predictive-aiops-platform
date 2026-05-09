import requests

BOT_TOKEN = "8653014573:AAHa1YvC3Aih9KRbYPtU5Hvq8mN9Y1h0Ljk"

CHAT_ID = "7480683115"

def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    print(response.text)

# --------------------------------
# TEST ALERT
# --------------------------------

if __name__ == "__main__":

    send_telegram_alert(
        "🚀 AIOps Telegram Alert Working!"
    )