from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, default="Unknown")
    description = models.TextField(blank=True, default="")
    rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)
    book_url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "books"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author}"


class ChatHistory(models.Model):
    question = models.TextField()
    answer = models.TextField()
    sources_json = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_history"
        ordering = ["-created_at"]

