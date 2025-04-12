from django.db import models
from django.contrib.auth import get_user_model
from games.models import Game

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")  # 🔥 УНИКАЛЬНЫЙ related_name
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="comments_game")  # 🔥 УНИКАЛЬНЫЙ related_name
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_ratings")  # 🔥 УНИКАЛЬНЫЙ related_name
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="comments_ratings")  # 🔥 УНИКАЛЬНЫЙ related_name
    value = models.IntegerField()

class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover = models.ImageField(upload_to="game_covers/", blank=True, null=True)
    rating = models.FloatField(default=0)
    total_votes = models.IntegerField(default=0)
    favorites = models.ManyToManyField(User, related_name="comments_favorite_games", blank=True)

    # ✅ Добавляем недостающие поля
    torrent_file = models.FileField(upload_to="torrents/", blank=True, null=True)
    direct_link = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=[("Action", "Action"), ("RPG", "RPG"), ("Strategy", "Strategy")])

    def calculate_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.rating = sum(r.value for r in ratings) / ratings.count()
            self.total_votes = ratings.count()
            self.save()

    def __str__(self):
        return self.title