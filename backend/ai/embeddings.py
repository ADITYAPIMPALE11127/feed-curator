from fastembed import TextEmbedding
import numpy as np
from catalog.models import Item, ItemEmbedding

# Load the model once when the script runs
# BAAI/bge-small-en-v1.5 is tiny (133MB) and very fast on CPU
MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=MODEL_NAME)

def generate_embeddings_for_new_items():
    """Finds items without embeddings, generates them, and saves to DB."""
    items = Item.objects.filter(embedding__isnull=True)
    if not items.exists():
        return 0

    texts = [f"{item.title}. {item.snippet}" for item in items]
    
    # Generate vectors
    embeddings = list(embedding_model.embed(texts))
    
    new_embeddings = []
    for item, vector in zip(items, embeddings):
        # Convert numpy array to list for JSON serialization
        new_embeddings.append(
            ItemEmbedding(
                item=item,
                vector=vector.tolist(),
                model_name=MODEL_NAME
            )
        )
    
    ItemEmbedding.objects.bulk_create(new_embeddings)
    return len(new_embeddings)

from sklearn.metrics.pairwise import cosine_similarity

def cluster_items():
    """Groups items into clusters if their embeddings are very similar."""
    # Get all items that have embeddings
    embeddings_qs = ItemEmbedding.objects.select_related('item').all()
    if len(embeddings_qs) == 0:
        return 0

    items = [e.item for e in embeddings_qs]
    vectors = np.array([e.vector for e in embeddings_qs])

    # Compute similarity matrix
    sim_matrix = cosine_similarity(vectors)

    # A simple clustering approach: 
    # If two items have > 0.85 similarity, they are the same cluster
    cluster_id_counter = 1
    cluster_assignments = {}

    for i in range(len(items)):
        if items[i].id in cluster_assignments:
            continue
            
        # Start a new cluster
        cluster_assignments[items[i].id] = cluster_id_counter
        
        # Find matches
        for j in range(i + 1, len(items)):
            if sim_matrix[i][j] > 0.85:
                cluster_assignments[items[j].id] = cluster_id_counter
                
        cluster_id_counter += 1

    # Save to DB
    updated_count = 0
    for item_id, cid in cluster_assignments.items():
        item = Item.objects.get(id=item_id)
        if item.cluster_id != cid:
            item.cluster_id = cid
            item.save()
            updated_count += 1

    return updated_count