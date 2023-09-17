from django.urls import path
from django import forms
from . import views
from django.urls import path
from . import views

app_name = "kvadro"
urlpatterns = [
    path("", views.homepage, name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
#   path("<int:pk>/", views.RecipeView.as_view(), name="recipe"),
    path("calculate/<int:pk>/", views.calculate, name="calculateform"),
    path("owner/<int:pk>/", views.OwnerRecipesView.as_view(), name="owner"),
    path("recipe/<int:pk>/", views.RecipeProductsView.as_view(), name="recipe"),
    path("group_recipes/<int:pk>/", views.GroupRecipesView.as_view(), name="group_recipes"),
#   path("groups/<int:pk>/", views.GroupsList.as_view(), name="groups"),
]