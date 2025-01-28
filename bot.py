import requests
from telegram import Bot

# Telegram Credentials
TELEGRAM_TOKEN = "8070383408:AAEUzxeDPfLC2KytDHAlCc0rSZWlSmydMFg"
CHAT_ID = "sxurxbh"

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
