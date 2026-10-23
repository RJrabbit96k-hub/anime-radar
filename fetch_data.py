import json
import time
from datetime import datetime, timezone
import requests

API_URL = "https://api.jikan.moe/v4/top/anime?filter=airing&limit=12"

def fetch_and_save():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Retry mechanism in case of public API rate-limits or network blips
    data = None
    for attempt in range(3):
        try:
            response = requests.get(API_URL, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                break
            time.sleep(3)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(3)
            
    if not data or 'data' not in data:
        raise RuntimeError("Failed to fetch data from API after 3 attempts.")

    items = []
    for entry in data.get('data', []):
        items.append({
            "title": entry.get("title_english") or entry.get("title"),
            "score": entry.get("score") or "N/A",
            "episodes": entry.get("episodes") or "Ongoing",
            "image": entry.get("images", {}).get("jpg", {}).get("large_image_url", ""),
            "url": entry.get("url", "#"),
            "synopsis": (entry.get("synopsis") or "No description available.")[:120] + "..."
        })
    
    output = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items": items
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("data.json successfully generated!")

if __name__ == "__main__":
    fetch_and_save()
    
