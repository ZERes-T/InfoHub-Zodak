from django.shortcuts import render, redirect
from django import forms
from .models import Game, Rating


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "title", "description", "cover", "rating", "total_votes",
            "favorites", "category", "direct_link", "torrent_file", "video_url"
        ]