from django.contrib.auth import views as auth_views
from django.contrib import admin
from telegram_auth.views import telegram_login
from django.urls import path, include
from users.views import edit_profile
from django.shortcuts import redirect
from games.views import admin_dashboard
from .views import home
from games.views import user_profile

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("game_list")  # ✅ Перенаправляем только если маршрут существует
    return redirect("account_login")

urlpatterns = [
    path("feedback/", include("feedback.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("games/", include("games.urls")),
    path("", home, name="home"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("profile/", user_profile, name="user_profile"),
]