import requests
import os
from bs4 import BeautifulSoup

# Set your Telegram Bot Token and Chat ID
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# GitHub Trending URLs for Overall and Python-specific repos
timeframes = {
    "Today": "daily",
    "Weekly": "weekly",
    "Monthly": "monthly",
}

base_url = "https://github.com/trending"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_trending_repos(url):
    """Fetch top 10 trending repositories from GitHub Trending page with descriptions."""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    repos = soup.find_all("article", class_="Box-row")[:10]  # Reduced to top 10 repos
    repo_list = []
    
    for repo in repos:
        # Extract repository name and link
        title = repo.find("h2").text.strip().replace("\n", "").replace(" ", "")
        repo_link = "https://github.com" + repo.find("a")["href"]
        
        # Extract stars count
        stars = repo.find("a", {"href": lambda x: x and x.endswith("/stargazers")})
        stars_count = stars.text.strip() if stars else "N/A"
        
        # Extract description
        description_tag = repo.find("p", class_=lambda x: x and "col-9" in x)
        description = description_tag.text.strip() if description_tag else "No description available"
        
        repo_list.append(f"🔹 [{title}]({repo_link}) - ⭐ {stars_count}\n`{description}`")

    return repo_list

def build_message(timeframe_dict, language_filter=""):
    """Build message for either all languages or Python only."""
    message = ""
    for timeframe, param in timeframe_dict.items():
        url = f"{base_url}/{language_filter}?since={param}" if language_filter else f"{base_url}?since={param}"
        repos = fetch_trending_repos(url)
        message += f"📅 **{timeframe}**\n"
        message += "\n".join(repos) + "\n\n"
    return message

# Build messages
all_langs_message = "🔥 **Trending GitHub Repositories - All Languages**\n\n"
all_langs_message += build_message(timeframes)

python_message = "🐍 **Trending GitHub Repositories - Python Only**\n\n"
python_message += build_message(timeframes, "python")

# Send messages via Telegram bot
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Send All Languages message
response_all = requests.post(telegram_url, data={
    "chat_id": CHAT_ID,
    "text": all_langs_message,
    "parse_mode": "Markdown"
})

# Send Python message
response_python = requests.post(telegram_url, data={
    "chat_id": CHAT_ID,
    "text": python_message,
    "parse_mode": "Markdown"
})

print("All Languages Response:", response_all.json())
print("Python Response:", response_python.json())
print("✅ Both messages sent successfully!")
