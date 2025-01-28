import requests
import os

# Get Telegram credentials from GitHub Secrets
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Fetch trending repos from GitHub
url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"
response = requests.get(url)
repos = response.json()["items"][:5]  # Get top 5 trending repos

# Format message
message = "🔥 Trending GitHub Repos Today:\n\n"
for repo in repos:
    message += f"🔹 {repo['name']} - ⭐ {repo['stargazers_count']}\n{repo['html_url']}\n\n"

# Send message via Telegram bot
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": message})

print("Message sent successfully!")
