import random
from re import search
from django import urls
from django.urls import path
from django.urls.conf import include

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("wiki/title/", views.random_page, name="random"),
    path("wiki/new/", views.new_page, name="new"),
    path("search/", views.search_entry, name="search"),
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.get_page, name="title"),
    path("wiki/<str:title>/edit/", views.edit_page, name="edit"),
    path("submit/", views.submit_edit, name="submit")

]
