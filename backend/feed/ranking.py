from catalog.models import Item

def get_ranked_feed(user, category_slug=None):
    # 1. Get the base queryset (active items, newest first)
    queryset = Item.objects.select_related('source', 'category').order_by('-published_at')
    
    # Filter by category if requested
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    # Grab the top 100 latest items to rank
    items = list(queryset[:100])

    # 2. Apply diversity (max 2 items per category in a row)
    ranked_items = []
    category_counts = {}
    
    for item in items:
        cat_id = item.category_id or 'none'
        
        # If we have already shown 2 items from this category, push it down
        if category_counts.get(cat_id, 0) >= 2:
            continue
            
        ranked_items.append(item)
        category_counts[cat_id] = category_counts.get(cat_id, 0) + 1
        
        # Stop once we have 50 items
        if len(ranked_items) >= 50:
            break

    return ranked_items