import requests
from telegram import Bot

# Telegram Credentials
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def get_trending_repos():
    # GitHub Trending API (unofficial, but works)
    url = "https://gh-trending-api.herokuapp.com/repositories"
    response = requests.get(url)
    repos = response.json()
    
    message = "📈 Today's Trending GitHub Repos:\n\n"
    for repo in repos[:10]:  # Top 10 repos
        message += f"{repo['name']}: {repo['url']}\n\n"
    return message

def send_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=get_trending_repos())

if __name__ == "__main__":
    send_message()
