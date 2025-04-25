from django.urls import path
from .views import (
    game_list, upload_game, rate_game,
    admin_dashboard, edit_game, delete_game,
    GameDetailView, ajax_search  # 👈 добавили proxy_youtube
)

urlpatterns = [
    path("game/<int:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("upload/", upload_game, name="upload_game"),
    path("game/<int:game_id>/rate/", rate_game, name="rate_game"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("edit-game/<int:game_id>/", edit_game, name="edit_game"),
    path("delete-game/<int:game_id>/", delete_game, name="delete_game"),
    path('ajax/search/', ajax_search, name='ajax_search'),

]