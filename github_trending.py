import requests
import os
from bs4 import BeautifulSoup

# Set your Telegram Bot Token and Chat ID
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# GitHub Trending URLs for different timeframes
timeframes = {
    "Today": "https://github.com/trending?since=daily",
    "Weekly": "https://github.com/trending?since=weekly",
    "Monthly": "https://github.com/trending?since=monthly",
}

# User-Agent to avoid request blocking
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_trending_repos(url):
    """Fetch trending repositories from GitHub Trending page."""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    repos = soup.find_all("article", class_="Box-row")[:20]  # Get top 20 trending repos
    repo_list = []
    
    for repo in repos:
        title = repo.find("h2").text.strip().replace("\n", "").replace(" ", "")
        repo_link = "https://github.com" + repo.find("a")["href"]
        stars = repo.find("a", {"href": lambda x: x and x.endswith("/stargazers")})
        stars_count = stars.text.strip() if stars else "N/A"
        
        repo_list.append(f"🔹 [{title}]({repo_link}) - ⭐ {stars_count}")

    return repo_list

# Build the final message
message = "🔥 **Trending GitHub Repositories**\n\n"
for timeframe, url in timeframes.items():
    message += f"📅 **{timeframe}**\n"
    trending_repos = fetch_trending_repos(url)
    message += "\n".join(trending_repos) + "\n\n"

# Send message via Telegram bot
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
response = requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

print(response.json())  # Print Telegram API response
print("✅ Trending GitHub repos sent successfully!")
