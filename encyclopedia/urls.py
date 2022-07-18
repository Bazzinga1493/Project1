from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="title"),
    path("add_page", views.add, name="add_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name="random_page"),
]
