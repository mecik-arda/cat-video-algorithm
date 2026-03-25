import webbrowser
import requests
import random
import io
from PIL import Image, ImageTk

API_KEY = "API_Key"

def fetch_popular_cat_video():
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": 50,
        "q": "#cat", 
        "order": "viewCount",
        "type": "video",
        "key": API_KEY
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        if "items" in data:
            video = random.choice(data["items"])
            return {"id": video["id"]["videoId"]}
        return None
    except:
        return None

def fetch_cat_image():
    try:
        url = "https://api.thecatapi.com/v1/images/search?limit=1"
        response = requests.get(url, timeout=10)
        data = response.json()
        img_url = data[0]['url']
        img_data = requests.get(img_url, timeout=10).content
        img = Image.open(io.BytesIO(img_data))
        img.thumbnail((450, 450), Image.Resampling.LANCZOS)
        return img
    except:
        return None

def open_video_in_browser(video_id):
    webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")
