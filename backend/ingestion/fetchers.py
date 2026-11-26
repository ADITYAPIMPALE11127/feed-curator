import hashlib
import feedparser
import httpx
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from catalog.models import Item, Source

def generate_url_hash(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()

def fetch_rss(source):
    """Fetches items from an RSS feed and saves them."""
    feed = feedparser.parse(source.url)
    new_items_count = 0

    for entry in feed.entries:
        url = entry.get('link')
        if not url:
            continue

        url_hash = generate_url_hash(url)
        
        # Check for exact duplicates first
        if Item.objects.filter(url_hash=url_hash).exists():
            continue

        # Handle dates (fallback to now if missing)
        published_at = timezone.now()
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_at = datetime(*entry.published_parsed[:6], tzinfo=dt_timezone.utc)
            
        snippet = entry.get('summary', '')[:500] # Keep snippets short

        Item.objects.create(
            source=source,
            external_id=entry.get('id', url),
            title=entry.get('title', 'No Title')[:500],
            url=url,
            url_hash=url_hash,
            snippet=snippet,
            published_at=published_at,
        )
        new_items_count += 1

    source.last_fetched_at = timezone.now()
    source.save()
    return new_items_count

def fetch_hacker_news(source):
    """Fetches top stories from Hacker News API."""
    new_items_count = 0
    
    # Get top 20 story IDs
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()[:20] 

    for story_id in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_resp = httpx.get(item_url).json()
        
        if not story_resp or 'url' not in story_resp:
            continue
            
        url = story_resp['url']
        url_hash = generate_url_hash(url)
        
        if Item.objects.filter(url_hash=url_hash).exists():
            continue

        published_at = datetime.fromtimestamp(story_resp.get('time', timezone.now().timestamp()), tz=dt_timezone.utc)
        
        Item.objects.create(
            source=source,
            external_id=str(story_id),
            title=story_resp.get('title', 'No Title')[:500],
            url=url,
            url_hash=url_hash,
            snippet="", # HN API doesn't give snippets
            published_at=published_at,
        )
        new_items_count += 1

    source.last_fetched_at = timezone.now()
    source.save()
    return new_items_count

def fetch_all_active_sources():
    """Loops through all active sources and routes to the correct fetcher."""
    sources = Source.objects.filter(is_active=True)
    total_fetched = 0
    
    for source in sources:
        if source.kind == 'rss':
            total_fetched += fetch_rss(source)
        elif source.kind == 'hn':
            total_fetched += fetch_hacker_news(source)
            
    return total_fetched