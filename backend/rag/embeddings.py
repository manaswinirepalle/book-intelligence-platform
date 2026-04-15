from functools import lru_cache
from sentence_transformers import SentenceTransformer
from django.conf import settings


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL_NAME)


def embed_texts(texts):
    return get_embedding_model().encode(texts, convert_to_numpy=True).tolist()

