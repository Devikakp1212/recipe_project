

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

from django.db.models import Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):

    query = request.GET.get('q')

    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
    else:
        recipes = Recipe.objects.all().order_by('-id')

    return render(request,
                  'home.html',
                  {
                      'recipes': recipes
                  })
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,
                            username=username,
                            password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('home')
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    return render(request, 'register.html', {'form': form})
@login_required
def add_recipe(request):
    form = RecipeForm()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('home')

    return render(request, 'add_recipe.html', {'form': form})



@login_required
def like_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.user in recipe.likes.all():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)

    return redirect('recipe_detail', id=id)


@login_required
def favorite_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    Favorite.objects.get_or_create(user=request.user, recipe=recipe)

    return redirect('recipe_detail', id=id)
def recipe_detail(request, id):

    recipe = get_object_or_404(Recipe, id=id)

    comments = Comment.objects.filter(recipe=recipe)

    avg_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'))

    comment_form = CommentForm()

    rating_form = RatingForm()

    if request.method == 'POST':

        if 'comment_submit' in request.POST:

            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():

                comment = comment_form.save(commit=False)

                comment.recipe = recipe
                comment.user = request.user

                comment.save()

        elif 'rating_submit' in request.POST:

            rating_form = RatingForm(request.POST)

            if rating_form.is_valid():

                Rating.objects.update_or_create(
                    user=request.user,
                    recipe=recipe,
                    defaults={
                        'rating': rating_form.cleaned_data['rating']
                    }
                )

    return render(request,
                  'recipe_detail.html',
                  {
                      'recipe': recipe,
                      'comments': comments,
                      'comment_form': comment_form,
                      'rating_form': rating_form,
                      'avg_rating': avg_rating
                  })
@login_required
def profile(request):

    recipes = Recipe.objects.filter(user=request.user)

    favorites = Favorite.objects.filter(user=request.user)

    total_recipes = recipes.count()

    total_favorites = favorites.count()

    return render(request,
                  'profile.html',
                  {
                      'recipes': recipes,

                      'favorites': favorites,

                      'total_recipes': total_recipes,

                      'total_favorites': total_favorites,
                  })