import json
from datetime import datetime, timezone
import requests

# AniList official GraphQL API (never blocked on GitHub Actions)
API_URL = "https://graphql.anilist.co"

QUERY = """
query {
  Page(page: 1, perPage: 12) {
    media(status: RELEASING, type: ANIME, sort: POPULARITY_DESC) {
      id
      title {
        english
        romaji
      }
      averageScore
      episodes
      coverImage {
        large
      }
      siteUrl
      description(asHtml: false)
    }
  }
}
"""

def fetch_and_save():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "AnimeRadar/1.0"
    }

    response = requests.post(API_URL, json={"query": QUERY}, headers=headers, timeout=20)
    response.raise_for_status()
    raw = response.json()

    media_list = raw.get("data", {}).get("Page", {}).get("media", [])
    
    items = []
    for entry in media_list:
        score = entry.get("averageScore")
        items.append({
            "title": entry.get("title", {}).get("english") or entry.get("title", {}).get("romaji") or "Unknown Title",
            "score": f"{score / 10:.1f}" if score else "N/A",
            "episodes": entry.get("episodes") or "Ongoing",
            "image": entry.get("coverImage", {}).get("large", ""),
            "url": entry.get("siteUrl", "#"),
            "synopsis": (entry.get("description") or "No synopsis available.").replace("\n", " ")[:130] + "..."
        })

    output = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "items": items
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Successfully fetched {len(items)} anime titles and wrote data.json!")

if __name__ == "__main__":
    fetch_and_save()
    
