import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_web(query: str) -> str:
    """Return only the top snippet from SerpAPI for a medical question."""
    if not SERPAPI_KEY:
        return "SerpAPI key not configured."
    
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 5,
        "gl": "us",
        "hl": "en",
        "device": "desktop",
        "no_cache": True
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    organic = results.get("organic_results", [])
    if not organic:
        return "No results found."
    
    first_result = organic[0]
    snippet = first_result.get("snippet") or first_result.get("title")
    return snippet
