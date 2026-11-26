from django.core.management.base import BaseCommand
from catalog.models import Category, Source

class Command(BaseCommand):
    help = 'Seed initial categories and sources'

    def handle(self, *args, **kwargs):
        # 1. Create Categories
        tech, _ = Category.objects.get_or_create(slug='tech', name='Technology')
        prog, _ = Category.objects.get_or_create(slug='programming', name='Programming')

        # 2. Create Sources
        Source.objects.get_or_create(
            name='Hacker News',
            defaults={'kind': 'hn', 'url': 'https://news.ycombinator.com', 'default_category': tech}
        )
        Source.objects.get_or_create(
            name='Real Python',
            defaults={'kind': 'rss', 'url': 'https://realpython.com/atom.xml', 'default_category': prog}
        )
        
        self.stdout.write(self.style.SUCCESS("Successfully seeded categories and sources."))