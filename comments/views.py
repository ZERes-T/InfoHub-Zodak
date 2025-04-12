from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment  # ✅ Убедись, что импортируется именно `Comment`
from .forms import CommentForm
from games.models import Game

@login_required
def add_comment(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.game = game
            comment.save()
    return redirect("game_detail", game_id=game.id)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_staff:  # Только автор или админ могут удалить
        comment.delete()
    return redirect("game_list")
