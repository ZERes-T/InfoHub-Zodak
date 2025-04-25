from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet

router = DefaultRouter()
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
from django.urls import path
from .views import add_comment, delete_comment

urlpatterns = [
    path("game/<int:game_id>/comment/", add_comment, name="add_comment"),
    path("delete/<int:comment_id>/", delete_comment, name="delete_comment"),
    path("logout/", auth_views.LogoutView.as_view(template_name="account/logout.html"), name="logout")
]


from django.urls import path
from .views import register

urlpatterns += [
    path('register/', register, name='register'),
]


from django.views.generic import TemplateView

urlpatterns += [
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('activation-sent/', TemplateView.as_view(template_name='registration/activation_sent.html'), name='activation_sent'),
]
