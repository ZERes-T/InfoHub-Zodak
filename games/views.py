from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Game, Rating
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model  # Импортируем модель пользователя
from games.models import Game

User = get_user_model()  # Получаем кастомную модель пользователя

# Функция для проверки, является ли пользователь админом
def is_admin(user):
    return user.is_staff or user.is_superuser

# Страница админ-панели
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Админ-панель: просмотр, добавление и удаление игр"""
    latest_games = Game.objects.order_by('-upload_date')[:5]
    games = Game.objects.all()

    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = GameForm()

    context = {
        'latest_games': latest_games,
        'games': games,
        'form': form
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def edit_game(request, game_id):
    """Редактирование информации об игре"""
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = GameForm(instance=game)

    return render(request, 'edit_game.html', {'form': form, 'game': game})


@login_required
def delete_game(request, game_id):
    """Удаление игры"""
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    return redirect('admin_dashboard')@login_required

@login_required
def upload_game(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.added_by = request.user
            game.save()
            return redirect("game_list")
    else:
        form = GameForm()
    return render(request, "games/upload_game.html", {"form": form})

def rate_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == "POST":
        value = int(request.POST.get("rating", 0))
        if 1 <= value <= 5:
            rating, created = Rating.objects.get_or_create(user=request.user, game=game)
            rating.value = value
            rating.save()
            game.calculate_rating()
            return JsonResponse({"success": True, "new_rating": game.rating})
    return JsonResponse({"success": False})

def game_list(request):
    query = request.GET.get("q", "")
    games = Game.objects.filter(title__icontains=query) if query else Game.objects.all()
    return render(request, "games/game_list.html", {"games": games, "query": query})
    category = request.GET.get("category", "all")

    if category == "games":
        games = Game.objects.filter(category="game")
    elif category == "apps":
        games = Game.objects.filter(category="app")
    else:
        games = Game.objects.all()

    return render(request, "games/game_list.html", {"games": games, "category": category})
from .forms import GameForm  # Убедись, что импорт формы есть

def home(request):
    games = Game.objects.all()[:8]  # Выводим 8 последних игр
    return render(request, "infohub/home.html", {"games": games})

@login_required
def upload_game(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.added_by = request.user  # Указываем, кто загрузил игру
            game.save()
            return redirect("game_list")
    else:
        form = GameForm()
    return render(request, "games/upload_game.html", {"form": form})

@login_required
def user_profile(request):
    user_games = Game.objects.filter(added_by=request.user)  # Выбираем игры текущего пользователя
    return render(request, "account/profile.html", {"user_games": user_games})


from .forms import GameForm

@login_required
def upload_game(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("game_list")  # Переход после загрузки
    else:
        form = GameForm()
    return render(request, "games/upload_game.html", {"form": form})
