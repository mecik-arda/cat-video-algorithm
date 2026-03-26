import requests
import webbrowser
import random
import io
from PIL import Image

def fetch_popular_cat_video(api_key, query="#cat", algo="Popular"):
    try:
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "maxResults": 25,
            "type": "video",
            "relevanceLanguage": "en",
            "order": "viewCount" if algo == "Popular" else "date",
            "key": api_key
        }
        r = requests.get(search_url, params=params, timeout=5)
        if r.status_code == 200:
            items = r.json().get("items", [])
            if items:
                video = random.choice(items)
                return {
                    "id": video["id"]["videoId"],
                    "title": video["snippet"]["title"]
                }
        elif r.status_code == 403:
            return {"id": "dQw4w9WgXcQ", "title": "Quota Exceeded"}
    except:
        pass
    return {"id": "dQw4w9WgXcQ", "title": "Default Video"}

def fetch_cat_image():
    try:
        r = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5)
        if r.status_code == 200:
            img_url = r.json()[0]['url']
            img_res = requests.get(img_url, timeout=5)
            return Image.open(io.BytesIO(img_res.content))
    except:
        pass
    return None

def open_video_in_browser(video_id):
    webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")