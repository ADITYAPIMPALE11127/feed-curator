from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ItemSerializer
from .ranking import get_ranked_feed

class FeedView(APIView):
    permission_classes = [AllowAny] # Open for now, we'll add user auth later

    def get(self, request):
        category = request.query_params.get('category', None)
        mode = request.query_params.get('mode', 'personalized') # mode=newest for baseline

        items = get_ranked_feed(request.user, category_slug=category)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)