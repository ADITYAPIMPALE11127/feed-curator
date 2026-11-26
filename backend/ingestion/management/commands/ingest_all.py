from django.core.management.base import BaseCommand
from ingestion.fetchers import fetch_all_active_sources

class Command(BaseCommand):
    help = 'Fetch, normalize, and dedupe items from all active sources'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting ingestion...")
        count = fetch_all_active_sources()
        self.stdout.write(self.style.SUCCESS(f"Successfully fetched {count} new items."))