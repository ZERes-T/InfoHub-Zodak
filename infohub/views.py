from django.shortcuts import render
from games.models import Game  # ✅ импорт Game из приложения games

def home(request):
    games = Game.objects.all()
    return render(request, "infohub/home.html", {"games": games})