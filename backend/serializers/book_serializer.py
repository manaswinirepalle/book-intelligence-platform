from rest_framework import serializers
from api.models import Book, ChatHistory


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "description",
            "rating",
            "reviews_count",
            "book_url",
            "created_at",
        ]


class AskRequestSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    top_k = serializers.IntegerField(default=4, min_value=1, max_value=10)


class UploadRequestSerializer(serializers.Serializer):
    pages = serializers.IntegerField(default=1, min_value=1, max_value=50)


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ["id", "question", "answer", "sources_json", "created_at"]

