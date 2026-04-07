def clean_query(query: str) -> str:
    """Helper to clean whitespace from a query."""
    return " ".join(query.split()).strip()
