from functools import lru_cache
import chromadb
from chromadb.config import Settings
from django.conf import settings


@lru_cache(maxsize=1)
def get_collection():
    client = chromadb.PersistentClient(
        path=settings.CHROMA_PERSIST_DIR,
        settings=Settings(anonymized_telemetry=False),
    )
    return client.get_or_create_collection(name="book_chunks")


def upsert_chunks(documents, embeddings, metadatas, ids):
    get_collection().upsert(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )


def query_chunks(query_embedding, top_k=4):
    return get_collection().query(query_embeddings=[query_embedding], n_results=top_k)

