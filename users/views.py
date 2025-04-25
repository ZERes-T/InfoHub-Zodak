from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # или "user_profile", в зависимости от urls.py
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})