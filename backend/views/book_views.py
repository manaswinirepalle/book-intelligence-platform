from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Book, ChatHistory
from serializers.book_serializer import (
    AskRequestSerializer,
    BookSerializer,
    ChatHistorySerializer,
    UploadRequestSerializer,
)
from scraper.books_scraper import scrape_books
from rag.ai_features import classify_genre, generate_summary, sentiment_analysis


@api_view(["GET"])
def books_list(request):
    return Response(BookSerializer(Book.objects.all(), many=True).data)


@api_view(["GET"])
def book_detail(request, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    payload = BookSerializer(book).data
    payload["summary"] = generate_summary(book.description)
    payload["genre"] = classify_genre(book.description)
    payload["sentiment"] = sentiment_analysis(book.description)
    return Response(payload)


@api_view(["GET"])
def recommend_books(request, book_id: int):
    try:
        target = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    recs = Book.objects.filter(
        Q(rating__gte=max(target.rating - 1, 0)) & ~Q(id=target.id)
    ).order_by("-rating", "-reviews_count")[:5]
    return Response({"book_id": target.id, "recommendations": BookSerializer(recs, many=True).data})


@api_view(["POST"])
def upload_books(request):
    serializer = UploadRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    pages = serializer.validated_data["pages"]

    from rag.chunker import chunk_text
    from rag.embeddings import embed_texts
    from rag.vector_store import upsert_chunks

    scraped = scrape_books(settings.SCRAPER_BASE_URL, pages=pages)
    documents, embeddings, metadatas, ids = [], [], [], []
    created_count = 0

    for item in scraped:
        book, created = Book.objects.update_or_create(
            book_url=item.book_url,
            defaults={
                "title": item.title,
                "author": item.author,
                "description": item.description,
                "rating": item.rating,
                "reviews_count": item.reviews_count,
            },
        )
        created_count += int(created)
        chunks = chunk_text(book.description)
        if not chunks:
            continue
        vectors = embed_texts(chunks)
        for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
            documents.append(chunk)
            embeddings.append(vector)
            metadatas.append({"book_id": book.id, "title": book.title, "source": book.book_url})
            ids.append(f"book-{book.id}-chunk-{idx}")

    if documents:
        upsert_chunks(documents, embeddings, metadatas, ids)

    return Response(
        {
            "message": "Books scraped and indexed successfully",
            "pages": pages,
            "created_count": created_count,
            "indexed_chunks": len(documents),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def ask_question(request):
    from rag.embeddings import embed_texts
    from rag.llm_client import ask_lm_studio, build_fallback_answer
    from rag.vector_store import query_chunks

    serializer = AskRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    question = serializer.validated_data["question"]
    top_k = serializer.validated_data["top_k"]
    cache_key = f"ask::{question.lower().strip()}::{top_k}"

    cached = cache.get(cache_key)
    if cached:
        return Response({**cached, "cached": True})

    try:
        query_embedding = embed_texts([question])[0]
        results = query_chunks(query_embedding, top_k=top_k)
    except Exception:
        return Response(
            {
                "question": question,
                "answer": "The search index is not ready yet. Please upload/scrape books and try again.",
                "sources": [],
                "cached": False,
                "fallback": True,
            },
            status=status.HTTP_200_OK,
        )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    context = "\n\n".join(docs) if docs else "No matching chunks found."
    sources = [
        {"title": m.get("title"), "book_id": m.get("book_id"), "source": m.get("source")}
        for m in metas
    ]

    fallback = False
    try:
        answer = ask_lm_studio(question, context)
    except requests.RequestException:
        answer = build_fallback_answer(question, docs)
        fallback = True
    except (KeyError, IndexError, TypeError, ValueError):
        answer = build_fallback_answer(question, docs)
        fallback = True

    ChatHistory.objects.create(question=question, answer=answer, sources_json=sources)
    payload = {
        "question": question,
        "answer": answer,
        "sources": sources,
        "cached": False,
        "fallback": fallback,
    }
    cache.set(cache_key, payload, timeout=settings.CACHE_TTL_SECONDS)
    return Response(payload)


@api_view(["GET"])
def chat_history(request):
    data = ChatHistorySerializer(ChatHistory.objects.all()[:50], many=True).data
    return Response(data)

