from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from feed.views import FeedView
from feed.views import FeedView, WeightsView, ModelStatsView
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
        path('api/me/weights/', WeightsView.as_view(), name='weights'),
    path('api/me/model/', ModelStatsView.as_view(), name='model-stats'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/feed/', FeedView.as_view(), name='feed'),
            path('api/items/<int:item_id>/feedback/', FeedbackView.as_view(), name='feedback'),
]