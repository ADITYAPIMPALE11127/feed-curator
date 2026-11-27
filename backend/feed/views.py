from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ItemSerializer
from .ranking import get_ranked_feed
from feedback.models import UserCategoryWeight
from rest_framework.permissions import IsAuthenticated
from ai.models import UserModel
class FeedView(APIView):
    permission_classes = [AllowAny] # Open for now, we'll add user auth later

    def get(self, request):
        category = request.query_params.get('category', None)
        mode = request.query_params.get('mode', 'personalized') # mode=newest for baseline

        items = get_ranked_feed(request.user, category_slug=category)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
class WeightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        weights = UserCategoryWeight.objects.filter(user=request.user).select_related('category')
        data = [
            {"category": w.category.name, "weight": w.weight}
            for w in weights
        ]
        return Response(data)

class ModelStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            model = UserModel.objects.get(user=request.user)
            return Response({
                "samples": model.n_samples,
                "auc": model.val_auc,
                "trained_at": model.trained_at
            })
        except UserModel.DoesNotExist:
            # Return empty stats if the model hasn't trained yet
            return Response({
                "samples": 0,
                "auc": None,
                "trained_at": None
            })