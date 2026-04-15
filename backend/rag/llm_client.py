import requests
from django.conf import settings


def ask_lm_studio(question: str, context: str):
    prompt = (
        "You are a helpful assistant for book intelligence. "
        "Answer from context only.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    payload = {
        "model": settings.LM_STUDIO_MODEL,
        "messages": [
            {"role": "system", "content": "Cite sources from retrieved chunks."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 300,
    }
    response = requests.post(settings.LM_STUDIO_URL, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def build_fallback_answer(question: str, docs):
    """
    Return a user-friendly local fallback when LM Studio is unavailable.
    """
    if not docs:
        return (
            "I could not find enough indexed book content to answer this yet. "
            "Please scrape or upload books first, then try again."
        )

    snippets = []
    for idx, doc in enumerate(docs[:3], start=1):
        clean = " ".join(doc.split())
        snippets.append(f"{idx}. {clean[:220]}{'...' if len(clean) > 220 else ''}")

    return (
        "The local AI model is currently unavailable, so here is a context-based summary from retrieved book data:\n"
        + "\n".join(snippets)
        + f"\n\nYour question: {question}"
    )

