import os
import requests
from rich.console import Console

console = Console()

def get_tavily_api_key():
    import os
    return os.getenv("TAVILY_API_KEY")


TAVILY_SEARCH_URL = "https://api.tavily.com/api/v1/search"

def search_tavily(topic, max_results=8):
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") 
    if not TAVILY_API_KEY:
        console.print("[red]Tavily API key not found.[/red]")
                          

def search_duckduckgo(topic, max_results=8):
    # kinda shitty API honestly but decent for a fallback. SERPAPI has rate limits of 150 req/day I think.
    try:
        resp = requests.get("https://api.duckduckgo.com/",
                            params={"q": topic, "format": "json", "no_redirect": 1, "skip_disambig": 1}, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        abstract = data.get("AbstractText", "")
        url = data.get("AbstractURL", "")
        if abstract:
            return [{"title": topic, "snippet": abstract, "url": url}]
        else:
            return []
    except Exception as e:
        console.print(f"[red]DuckDuckGo search failed: {e}[/red]")
        return []


def search_serpapi(query, max_results=8):
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    if not SERPAPI_API_KEY:
        console.print("[red]SerpAPI key not found in environment variables.[/red]")
        return None

    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "engine": "google",
        "num": max_results,
        "api_key": SERPAPI_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        results = []
        organic_results = data.get("organic_results", [])

        for item in organic_results[:max_results]:
            title = item.get("title", "")
            snippet = item.get("snippet", "") or item.get("description", "")
            link = item.get("link", "")
            if title and snippet:
                results.append({"title": title, "snippet": snippet, "url": link})
        return results
    except Exception as e:
        console.print(f"[red]SerpAPI search failed: {e}[/red]")
        return None

def search_web(topic):
    results = search_serpapi(topic)
    if results:
        return results
    console.print("[yellow]Falling back to DuckDuckGo search...[/yellow]")
    return search_duckduckgo(topic)
