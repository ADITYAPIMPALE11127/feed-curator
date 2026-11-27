import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from feedback.models import Interaction, UserTasteVector
from catalog.models import ItemEmbedding

def update_taste_vector(user):
    """Calculates the average vector of a user's liked items."""
    # Get embeddings for items the user liked
    liked_interactions = Interaction.objects.filter(user=user, action='like').select_related('item')
    
    liked_vectors = []
    for interaction in liked_interactions:
        try:
            liked_vectors.append(interaction.item.embedding.vector)
        except ItemEmbedding.DoesNotExist:
            continue

    taste_vector_obj, _ = UserTasteVector.objects.get_or_create(user=user)
    
    if not liked_vectors:
        taste_vector_obj.vector = None
        taste_vector_obj.liked_count = 0
        taste_vector_obj.save()
        return
    
    # Calculate the mean vector across all liked items
    mean_vector = np.mean(liked_vectors, axis=0)
    
    taste_vector_obj.vector = mean_vector.tolist()
    taste_vector_obj.liked_count = len(liked_vectors)
    taste_vector_obj.save()

def calculate_similarity_score(user, item):
    """Returns a similarity score (0 to 1) between the user's taste and the item."""
    try:
        taste_vector_obj = UserTasteVector.objects.get(user=user)
        if not taste_vector_obj.vector:
            return 0.0 # No taste vector yet
        taste_vec = np.array(taste_vector_obj.vector).reshape(1, -1)
    except UserTasteVector.DoesNotExist:
        return 0.0

    try:
        item_vector = np.array(item.embedding.vector).reshape(1, -1)
    except ItemEmbedding.DoesNotExist:
        return 0.0

    # Cosine similarity returns a value between -1 and 1
    sim = cosine_similarity(taste_vec, item_vector)[0][0]
    return float(sim)