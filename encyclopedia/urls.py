from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/results/", views.results, name="results"),
    path("new/", views.newPage, name="new"),
    path("wiki/random/", views.randomEntry, name="random"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>/", views.entry, name = "entry")
]
