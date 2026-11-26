from django.db import models

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Source(models.Model):
    KIND_CHOICES = [
        ('rss', 'RSS'),
        ('hn', 'Hacker News'),
        ('arxiv', 'arXiv'),
        ('guardian', 'The Guardian'),
        ('devto', 'Dev.to'),
    ]
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    url = models.URLField()
    default_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    quality_score = models.FloatField(default=1.0)
    fetch_interval_minutes = models.IntegerField(default=60)
    last_fetched_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='items')
    external_id = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=1000)
    url_hash = models.CharField(max_length=64, unique=True)
    snippet = models.TextField(blank=True)
    published_at = models.DateTimeField(db_index=True)
    fetched_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    category_confidence = models.FloatField(null=True, blank=True)
    cluster_id = models.IntegerField(null=True, blank=True, db_index=True)
    summary = models.TextField(blank=True)

    class Meta:
        unique_together = ('source', 'external_id')
        indexes = [
            models.Index(fields=['category', 'published_at']),
        ]

    def __str__(self):
        return self.title

class ItemEmbedding(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='embedding')
    vector = models.JSONField()
    model_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class ItemStats(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='stats')
    impressions_48h = models.IntegerField(default=0)
    likes_48h = models.IntegerField(default=0)
    dislikes_48h = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)