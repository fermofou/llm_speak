from app.services.wikipedia_service import search_wikipedia, get_wikipedia_summary


def search_wiki(query: str, sentences: int = 3) -> dict:
    """Search Wikipedia for information."""
    return search_wikipedia(query, sentences)


def get_wiki_summary(page_title: str) -> dict:
    """Get a summary of a Wikipedia page."""
    return get_wikipedia_summary(page_title)
