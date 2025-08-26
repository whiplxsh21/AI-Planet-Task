import requests
import os

# some sort of niche images or references are not possible to get, unsplash isnt really good at that, but for this use-case, its decent.
def search_unsplash_image(query: str) -> str | None:
    api_key = os.getenv("UNSPLASH_API_KEY")
    if not api_key:
        return None
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {"query": query, "orientation": "landscape", "per_page": 1}
    resp = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("results"):
            img_url = data["results"][0]["urls"]["regular"]
            return img_url
    return None

def download_image(url: str, save_path: str) -> str | None:
    try:
        resp = requests.get(url, stream=True)
        if resp.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            return save_path
    except Exception:
        pass
    return None
