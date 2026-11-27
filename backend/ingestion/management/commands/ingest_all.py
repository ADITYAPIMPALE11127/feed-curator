from django.core.management.base import BaseCommand
from ingestion.fetchers import fetch_all_active_sources
from catalog.models import Item, Category
from ai.llm_client import classify_item
from ai.embeddings import generate_embeddings_for_new_items, cluster_items
class Command(BaseCommand):
    help = 'Fetch, normalize, and dedupe items from all active sources'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting ingestion...")
        
        # Step 1: Fetch new items
        count = fetch_all_active_sources()
        self.stdout.write(self.style.SUCCESS(f"Successfully fetched {count} new items."))
        
        # Step 2: Classify uncategorized items
        self.stdout.write("Classifying items via LLM...")
        uncategorized_items = Item.objects.filter(category__isnull=True)
        
        # Map our slugs to Category objects (create if missing)
        valid_slugs = ['tech', 'programming', 'science', 'business', 'world']
        categories = {}
        for slug in valid_slugs:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': slug.capitalize()})
            categories[slug] = cat
            
        classified_count = 0
        for item in uncategorized_items:
            category_slug = classify_item(item.title, item.snippet)
            
            # Assign the category
            if category_slug in categories:
                item.category = categories[category_slug]
            else:
                item.category = categories['tech'] # fallback
                
            item.save()
            classified_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully classified {classified_count} items."))
        
        # Step 3: Generate Embeddings
        self.stdout.write("Generating embeddings...")
        embedded_count = generate_embeddings_for_new_items()
        self.stdout.write(self.style.SUCCESS(f"Generated embeddings for {embedded_count} items."))

        # Step 4: Cluster similar items
        self.stdout.write("Clustering similar items...")
        clustered_count = cluster_items()
        self.stdout.write(self.style.SUCCESS(f"Updated cluster IDs for {clustered_count} items."))