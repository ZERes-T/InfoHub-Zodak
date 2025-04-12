from django.urls import path, include

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("accounts/", include("allauth.urls")),
]
