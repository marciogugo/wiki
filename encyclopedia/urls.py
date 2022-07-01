from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/Search", views.search_view),
    path("wiki/New", views.new_entry_view),
    path("wiki/Random", views.random_view),
    path("wiki/Edit/<str:entry>", views.edit_entry_view),
    path('wiki/<str:entry>', views.get_entry_view, name="get-entry"),
]

