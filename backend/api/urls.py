from django.urls import path
from views.book_views import (
    ask_question,
    book_detail,
    books_list,
    chat_history,
    recommend_books,
    upload_books,
)

urlpatterns = [
    path("books/", books_list),
    path("books/<int:book_id>/", book_detail),
    path("recommend/<int:book_id>/", recommend_books),
    path("upload/", upload_books),
    path("ask/", ask_question),
    path("history/", chat_history),
]

