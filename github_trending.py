import requests
import os
from bs4 import BeautifulSoup

# Set your Telegram Bot Token and Chat ID here
BOT_TOKEN = "your_telegram_bot_token"
CHAT_ID = "your_chat_id"

# Fetch trending repositories (unofficial GitHub Trending API)
url = "https://github.com/trending?since=daily"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Parse HTML to extract trending repo details
soup = BeautifulSoup(response.text, "html.parser")
repos = soup.find_all("article", class_="Box-row")[:5]  # Get top 5 trending

# Format message
message = "🔥 Trending GitHub Repos (Today):\n\n"
for repo in repos:
    title = repo.find("h2").text.strip().replace("\n", "").replace(" ", "")
    repo_link = "https://github.com" + repo.find("a")["href"]
    stars = repo.find("a", {"href": lambda x: x and x.endswith("/stargazers")})
    stars_count = stars.text.strip() if stars else "N/A"
    
    message += f"🔹 {title} - ⭐ {stars_count}\n{repo_link}\n\n"

# Send message via Telegram bot
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response = requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": message})
print(response.json())  # Print Telegram API response

print("✅ Message sent successfully!")
