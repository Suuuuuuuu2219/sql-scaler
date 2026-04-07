import sqlparse
import re

def normalize(query: str) -> str:
    """Normalize a SQL query using sqlparse."""
    # 1. Strip comments
    parsed = sqlparse.format(query, strip_comments=True)
    # 2. Uppercase keywords
    parsed = sqlparse.format(parsed, keyword_case='upper')
    # 3. Clean whitespace
    parsed = " ".join(parsed.split())
    return parsed.strip()

def is_equivalent(q1: str, q2: str) -> bool:
    """Check if two queries are normalized equivalent."""
    return normalize(q1) == normalize(q2)

def optimization_score(original: str, optimized: str) -> float:
    """Apply optimization rules to compute a score additive components."""
    score = 0.0
    
    # 1. No SELECT * (+0.3)
    if "SELECT *" not in original.upper() or "SELECT *" not in optimized.upper():
        if "SELECT *" not in optimized.upper() and "SELECT *" in original.upper():
            score += 0.3
            
    # 2. Uses JOIN (+0.3)
    # If the original used a comma-join or a subquery, and optimized uses JOIN.
    if "JOIN" in optimized.upper() and "JOIN" not in original.upper():
        score += 0.3
    elif "JOIN" in optimized.upper() and "JOIN" in original.upper():
        # If it already had a join, check if it's "better" (e.g. using aliases)
        # This is simplified for the grader.
        pass

    # 3. Shorter query (+0.2)
    if len(optimized) < len(original):
        score += 0.2
        
    return score

def grade(original: str, predicted: str, optimal: str) -> float:
    """Compute final reward between 0.0 and 1.0."""
    # 1. Exact match with optimal (+1.0)
    if is_equivalent(predicted, optimal):
        return 1.0
        
    # 2. Logic Check
    # Simplified: if the predicted query is not equivalent to optimal, 
    # it might be functionally wrong. But in a real environment, 
    # we'd execute it. Here we use the specified rules.
    
    score = optimization_score(original, predicted)
    
    # Cap between 0.0 and 1.0
    # Note: The prompt says "Partial optimization -> 0.5 to 1.0".
    # I'll base it on the rules.
    if score > 0:
        return min(1.0, 0.5 + score)
        
    return 0.0
