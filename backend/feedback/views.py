from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from catalog.models import Item
from .models import Interaction, UserCategoryWeight
from django.shortcuts import get_object_or_404
from ai.personalization import update_taste_vector
class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        action = request.data.get('action')

        if action not in ['like', 'dislike', 'save', 'hide']:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Log the interaction
        Interaction.objects.create(user=request.user, item=item, action=action)

        # 2. Update category weights (Learning Logic)
        if item.category and action in ['like', 'dislike']:
            weight_obj, _ = UserCategoryWeight.objects.get_or_create(
                user=request.user, 
                category=item.category,
                defaults={'weight': 1.0}
            )
            
            if action == 'like':
                weight_obj.weight = min(3.0, weight_obj.weight + 0.2)
            elif action == 'dislike':
                weight_obj.weight = max(0.05, weight_obj.weight - 0.2)
                
            weight_obj.save()
                    # Recalculate the taste vector after every like/dislike
        if action in ['like', 'dislike']:
            update_taste_vector(request.user)

        return Response({"status": "success", "action": action})