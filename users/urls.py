from django.urls import path, include
from . import views
from .views import confirm_email
from .views import CustomLoginView, CustomSignupView

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("accounts/", include("allauth.urls")),
    path('confirm-email/', views.confirm_email, name='confirm_email'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
