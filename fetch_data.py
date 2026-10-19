import urllib.request
import json
from datetime import datetime, timezone

API_URL = "https://api.jikan.moe/v4/top/anime?filter=airing&limit=12"

def fetch_and_save():
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        raw_data = json.loads(response.read().decode('utf-8'))
    
    items = []
    for entry in raw_data.get('data', []):
        items.append({
            "title": entry.get("title_english") or entry.get("title"),
            "score": entry.get("score") or "N/A",
            "episodes": entry.get("episodes") or "Ongoing",
            "image": entry["images"]["jpg"]["large_image_url"],
            "url": entry.get("url"),
            "synopsis": (entry.get("synopsis") or "No description available.")[:120] + "..."
        })
    
    output = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items": items
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fetch_and_save()
