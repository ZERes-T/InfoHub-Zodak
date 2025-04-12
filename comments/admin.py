from django.contrib import admin
from .models import Comment  # замени Comment на свою модель, если имя другое

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'created_at')  # отобрази нужные поля
    search_fields = ('user__username', 'game__title')         # для поиска
