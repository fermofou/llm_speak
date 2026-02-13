import requests


def search_wikipedia(query: str, sentences: int = 3) -> dict:
    """
    Search Wikipedia for information about a topic.
    
    Args:
        query: Search query
        sentences: Number of sentences to return
        
    Returns:
        Dictionary with search results
    """
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": query,
            "prop": "extracts",
            "explaintext": True,
            "exsentences": sentences,
            "redirects": 1
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        if pages:
            page = list(pages.values())[0]
            if "extract" in page:
                return {
                    "success": True,
                    "title": page.get("title"),
                    "extract": page.get("extract"),
                    "source": "Wikipedia"
                }
        
        return {
            "success": False,
            "error": f"No Wikipedia article found for '{query}'"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_wikipedia_summary(page_title: str) -> dict:
    """Get a summary of a Wikipedia page."""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "extracts",
            "explaintext": True,
            "exintro": True,
            "redirects": 1
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        if pages:
            page = list(pages.values())[0]
            return {
                "success": True,
                "title": page.get("title"),
                "summary": page.get("extract"),
                "source": "Wikipedia"
            }
        
        return {
            "success": False,
            "error": f"No Wikipedia article found for '{page_title}'"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
