from django.contrib import admin
from .models import Game, Comment, Rating

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']  # оставим только реальные поля
    list_filter = []  # убираем 'os'
    search_fields = ['title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'game', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'game', 'user']  # 🛠 'score' удалён
    list_filter = []  # 🛠 'score' удалён