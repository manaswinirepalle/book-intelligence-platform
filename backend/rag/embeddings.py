from functools import lru_cache
from django.conf import settings
import hashlib


EMBEDDING_DIM = 128


@lru_cache(maxsize=1)
def get_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
    except Exception:
        # Keep backend bootable even when transformer dependencies are unavailable.
        return None


def _fallback_embedding(text: str):
    vector = [0.0] * EMBEDDING_DIM
    tokens = text.lower().split()
    if not tokens:
        return vector
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        for idx in range(EMBEDDING_DIM):
            vector[idx] += digest[idx % len(digest)] / 255.0
    scale = float(len(tokens))
    return [value / scale for value in vector]


def embed_texts(texts):
    model = get_embedding_model()
    if model is None:
        return [_fallback_embedding(text) for text in texts]
    return model.encode(texts, convert_to_numpy=True).tolist()

