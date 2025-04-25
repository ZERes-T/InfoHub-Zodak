from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from users.views import edit_profile
from django.shortcuts import redirect
from games.views import admin_dashboard, user_profile
from .views import home

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("game_list")
    return redirect("account_login")

urlpatterns = [
    path("feedback/", include("feedback.urls")),
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path("games/", include("games.urls")),
    path("", home, name="home"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", user_profile, name="user_profile"),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)