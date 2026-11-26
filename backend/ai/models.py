from django.db import models
from django.conf import settings
import hashlib
import json
class UserModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_model')
    coefficients = models.JSONField(default=dict)
    intercept = models.FloatField(default=0.0)
    n_samples = models.IntegerField(default=0)
    val_auc = models.FloatField(null=True, blank=True)
    trained_at = models.DateTimeField(null=True, blank=True)

class AICache(models.Model):
    key = models.CharField(max_length=64, unique=True)
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
def generate_cache_key(prompt, model_name, text):
    raw_string = f"{prompt}_{model_name}_{text}"
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()