from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account_profile")
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "account/edit_profile.html", {"form": form})


from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user = request.user
    games = user.game_set.all() if hasattr(user, 'game_set') else []
    return render(request, 'users/profile.html', {'user': user, 'games': games})