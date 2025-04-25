import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover = models.ImageField(upload_to='game_covers/', blank=True, null=True)
    rating = models.FloatField(default=0)
    total_votes = models.IntegerField(default=0)

    favorites = models.ManyToManyField(User, through='GameFavorites', related_name='favorite_games', blank=True)

    category = models.CharField(
        max_length=100,
        choices=[
            ("Action", "Action"),
            ("RPG", "RPG"),
            ("Strategy", "Strategy")
        ]
    )
    direct_link = models.URLField(blank=True, null=True)
    torrent_file = models.FileField(upload_to='torrents/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_games")

    def __str__(self):
        return self.title

    def delete_old_file(self):
        if not self.pk:
            return
        try:
            old_game = Game.objects.get(pk=self.pk)
        except Game.DoesNotExist:
            return

        if old_game.cover and old_game.cover != self.cover:
            old_path = os.path.join(settings.MEDIA_ROOT, old_game.cover.name)
            if os.path.exists(old_path):
                os.remove(old_path)

    def save(self, *args, **kwargs):
        self.delete_old_file()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.cover:
            cover_path = os.path.join(settings.MEDIA_ROOT, self.cover.name)
            if os.path.exists(cover_path):
                os.remove(cover_path)

        if self.torrent_file:
            torrent_path = os.path.join(settings.MEDIA_ROOT, self.torrent_file.name)
            if os.path.exists(torrent_path):
                os.remove(torrent_path)

        super().delete(*args, **kwargs)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rated_games")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="ratings")
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'game')

class GameFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "game")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.user} к {self.game}'