from django.db import models
from django.conf import settings
from catalog.models import Category, Item

class UserCategoryWeight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='category_weights')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    weight = models.FloatField(default=1.0) # 0.05 to 3.0
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.email} - {self.category.name}: {self.weight}"

class UserTasteVector(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taste_vector')
    vector = models.JSONField(null=True, blank=True)
    liked_count = models.IntegerField(default=0)
    disliked_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

class Interaction(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('save', 'Save'),
        ('hide', 'Hide'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interactions')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'item']),
        ]

class FeedImpression(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='impressions')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    position = models.IntegerField()
    score = models.FloatField()
    features = models.JSONField(default=dict)
    shown_at = models.DateTimeField(auto_now_add=True)