from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from feed.views import FeedView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from feedback.views import FeedbackView

def healthz(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz', healthz),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/feed/', FeedView.as_view(), name='feed'),
            path('api/items/<int:item_id>/feedback/', FeedbackView.as_view(), name='feedback'),
]