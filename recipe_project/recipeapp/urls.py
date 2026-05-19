from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
 
    path('home/', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),

    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),

    path('like/<int:id>/', views.like_recipe, name='like_recipe'),

    path('favorite/<int:id>/', views.favorite_recipe, name='favorite_recipe'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'), 
]