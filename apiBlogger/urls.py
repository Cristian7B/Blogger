from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.ReadmeView.as_view(), name="post-list"),
    path("posts/<int:pk>/", views.ReadmeView.as_view(), name="post-detail"),
    path("", views.index, name="index"),
]