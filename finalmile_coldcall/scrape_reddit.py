import re
from typing import List, Tuple

import requests

from constants import (
    AIRPORT_MAP,
    KNOWN_CITIES,
    LOCATION_PATTERNS,
    REQUEST_HEADERS,
    STATE_FULL_MAP,
    STATE_MAP,
)


def parse_location_from_title(title: str) -> str:
    """
    Extract city and state from a Reddit title using common patterns.

    Args:
        title: Post title.

    Returns:
        Location string in the form 'City, State' or best-effort extraction.
    """
    # Normalize separators to a common form for easier parsing
    normalized = re.sub(r"[|/]", " ", title)
    # Remove content inside parentheses for initial parsing
    stripped = re.sub(r"\([^)]*\)", "", normalized)

    # 1) Try explicit patterns with state abbreviations
    for pat in LOCATION_PATTERNS:
        match = re.search(pat, stripped, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            state = match.group(2).strip()
            city = re.sub(r"\b(Area|County|Metro)\b", "", city, flags=re.IGNORECASE).strip()
            # Ensure state is 2-letter abbreviation; if not, try to abbreviate
            if len(state) != 2:
                state = STATE_MAP.get(state, state)
            return f"{city}, {state}"

    # 2) Special case: airport codes like RNO, DFW preceded/followed by text
    airport_match = re.search(r"([A-Za-z\s]{3,15})\s+([A-Z]{3})\b", stripped)
    if airport_match:
        city_part = airport_match.group(1).strip()
        code = airport_match.group(2)
        if code in AIRPORT_MAP:
            return AIRPORT_MAP[code]
        return f"{city_part} {code}"

    # 2b) Airport code alone before price/number (e.g., "RNO 564k")
    airport_alone = re.search(r"\b(" + "|".join(AIRPORT_MAP.keys()) + r")\b\s+[$]?\d", stripped)
    if airport_alone:
        code = airport_alone.group(1)
        return AIRPORT_MAP.get(code, code)

    # 3) Standalone state abbreviations (e.g., "CO $560k")
    state_only = re.search(r"\b([A-Z]{2})\b", stripped)
    if state_only:
        state = state_only.group(1)
        return STATE_FULL_MAP.get(state, state)

    # 4) Known city names before price or number (fallback)
    city_before_price = re.search(r"\b(" + "|".join(KNOWN_CITIES) + r")\b", stripped, re.IGNORECASE)
    if city_before_price:
        return city_before_price.group(0)

    # 5) Fallback: any phrase before a price, but exclude generic phrases
    fallback = re.search(r"(.+?)\s+[$]\d", stripped)
    if fallback:
        loc = fallback.group(1).strip()
        loc_clean = re.sub(r"\b(Metro|Area|County)\b", "", loc, flags=re.IGNORECASE).strip()
        # Exclude generic phrases that commonly appear before prices
        generic_prefixes = {
            "i did it",
            "i did, it",
            "we did it",
            "we did, it",
            "finally did it",
            "finally did, it",
            "finally did",
            "got the keys",
            "got keys",
            "got the",
            "we got the",
            "we finally",
            "i opted",
            "first home",
            "dream come",
            "saving paid",
            "first month",
            "we did",
            "i did",
        }
        # If the cleaned location starts with a generic phrase, try to extract a known city after it
        matched_generic = None
        for word in generic_prefixes:
            if loc_clean.lower().startswith(word):
                matched_generic = word
                remaining = loc_clean[len(word):].strip(", ").strip()
                # Check if the remaining text is a known city
                if remaining.lower() in (c.lower() for c in KNOWN_CITIES):
                    return remaining
                # Also check if the remaining text contains a known city (e.g., extra words)
                for city in KNOWN_CITIES:
                    if city.lower() in remaining.lower():
                        return city
                break
        # If no generic prefix matched, return the cleaned location
        if not matched_generic:
            return loc_clean
        return "Unknown"

    # 6) Special case: check for known cities anywhere in the title
    for city in KNOWN_CITIES:
        if city.lower() in stripped.lower():
            return city

    return "Unknown"


def get_recent_posts_with_user(
    subreddit_name: str,
    target_flair: str = "GOT THE KEY",
    max_posts: int = 50,
    sort: str = "new",
) -> List[Tuple[str, str]]:
    """
    Fetch recent posts from a subreddit and return (title, username) for posts that have the target flair
    or contain the target text in the title or body.

    Args:
        subreddit_name: Name of the subreddit (without 'r/').
        target_flair: Exact flair text to match (case-insensitive).
        max_posts: Maximum number of matching posts to return.
        sort: Sorting order ('new', 'hot', 'top', etc.).

    Returns:
        List of (title, username) tuples matching the criteria.
    """
    base_url = f"https://www.reddit.com/r/{subreddit_name}/{sort}.json"
    matching_results: List[Tuple[str, str]] = []
    after = None

    while len(matching_results) < max_posts:
        url = base_url
        params = {}
        if after:
            params["after"] = after

        try:
            response = requests.get(url, headers=REQUEST_HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            posts = data["data"]["children"]
            if not posts:
                break  # No more posts

            for post in posts:
                post_data = post["data"]
                title = post_data.get("title", "")
                selftext = post_data.get("selftext", "")
                flair = post_data.get("link_flair_text", "")
                author = post_data.get("author", "[deleted]")

                # Check flair or title/body contains target text (case-insensitive)
                if flair and target_flair.lower() in flair.lower():
                    matching_results.append((title, author))
                elif target_flair.lower() in title.lower() or target_flair.lower() in selftext.lower():
                    matching_results.append((title, author))

                if len(matching_results) >= max_posts:
                    break

            # Pagination token for next page
            after = data["data"].get("after")
            if not after:
                break

        except Exception as e:
            print(f"Error fetching posts for r/{subreddit_name}: {e}")
            break

    return matching_results[:max_posts]


def get_recent_posts_with_user_and_location(
    subreddit_name: str,
    target_flair: str = "GOT THE KEY",
    max_posts: int = 50,
    sort: str = "new",
) -> List[Tuple[str, str, str]]:
    """
    Fetch recent posts from a subreddit and return (title, location, username) for posts that have the target flair
    or contain the target text in the title or body.

    Args:
        subreddit_name: Name of the subreddit (without 'r/').
        target_flair: Exact flair text to match (case-insensitive).
        max_posts: Maximum number of matching posts to return.
        sort: Sorting order ('new', 'hot', 'top', etc.).

    Returns:
        List of (title, location, username) tuples matching the criteria.
    """
    base_url = f"https://www.reddit.com/r/{subreddit_name}/{sort}.json"
    matching_results: List[Tuple[str, str, str]] = []
    after = None

    while len(matching_results) < max_posts:
        url = base_url
        params = {}
        if after:
            params["after"] = after

        try:
            response = requests.get(url, headers=REQUEST_HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            posts = data["data"]["children"]
            if not posts:
                break  # No more posts

            for post in posts:
                post_data = post["data"]
                title = post_data.get("title", "")
                selftext = post_data.get("selftext", "")
                flair = post_data.get("link_flair_text", "")
                author = post_data.get("author", "[deleted]")

                # Check flair or title/body contains target text (case-insensitive)
                if flair and target_flair.lower() in flair.lower():
                    location = parse_location_from_title(title)
                    matching_results.append((title, location, author))
                elif target_flair.lower() in title.lower() or target_flair.lower() in selftext.lower():
                    location = parse_location_from_title(title)
                    matching_results.append((title, location, author))

                if len(matching_results) >= max_posts:
                    break

            # Pagination token for next page
            after = data["data"].get("after")
            if not after:
                break

        except Exception as e:
            print(f"Error fetching posts for r/{subreddit_name}: {e}")
            break

    return matching_results[:max_posts]


if __name__ == "__main__":
    subreddit = "FirstTimeHomeBuyer"
    
    # Example 1: Get posts with location parsing
    print("=== WITH LOCATION PARSING ===")
    results = get_recent_posts_with_user_and_location(subreddit, target_flair="GOT THE KEY", max_posts=15)
    if results:
        print(f"Found {len(results)} posts with flair or 'GOT THE KEY' in title/body (with location):")
        for i, (title, location, author) in enumerate(results, 1):
            print(f"{i}. {location} — u/{author}")
            print(f"   Title: {title}\n")
    else:
        print("No posts found matching the criteria.")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Get posts without location parsing (simpler)
    print("=== WITHOUT LOCATION PARSING ===")
    simple_results = get_recent_posts_with_user(subreddit, target_flair="GOT THE KEY", max_posts=15)
    if simple_results:
        print(f"Found {len(simple_results)} posts with flair or 'GOT THE KEY' in title/body (title and username only):")
        for i, (title, author) in enumerate(simple_results, 1):
            print(f"{i}. u/{author}")
            print(f"   Title: {title}\n")
    else:
        print("No posts found matching the criteria.")
