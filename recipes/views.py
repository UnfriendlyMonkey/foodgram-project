import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Subquery, Prefetch, OuterRef, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from rest_framework import status

from recipes.forms import RecipeForm
from recipes.models import (
    Recipe,
    User,
    Follow,
    Ingredient,
    Tag,
    RecipeIngredient,
    ShoppingCart
)
from django.conf import settings


class BaseRecipeListView(ListView):
    """Base view for Recipe list."""
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = settings.PAGINATED_BY
    page_title = None

    def get_context_data(self, **kwargs):
        """Add page title to the context."""
        tags = Tag.objects.all()
        kwargs.update({'page_title': self._get_page_title(), 'tag_list': tags})

        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        """Get page title."""
        return self.page_title

    def get_queryset(self):
        """Get selected tag filters from query
        and filtrate queryset according to them"""
        qs = super().get_queryset()
        tags = self.request.GET.getlist('active_tags')

        if tags:
            qs = qs.filter(tag__slug__in=tags).distinct()

        return qs


class IndexView(BaseRecipeListView):
    """Main page that displays list of Recipes."""
    page_title = 'Рецепты'
    template_name = 'recipes/recipes_list.html'


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    """List of current user's favorite Recipes."""
    page_title = 'Избранное'
    template_name = 'recipes/recipes_list.html'

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = qs.filter(favorites__user=self.request.user)

        return qs


class ProfileView(BaseRecipeListView):
    """User's page with its name and list of authored Recipes."""
    template_name = 'recipes/author_recipes_list.html'

    def get(self, request, *args, **kwargs):
        """Store `user`s parameter for data filtration purposes."""
        self.user = get_object_or_404(User, username=kwargs.get('username'))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({'author': self.user})
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = qs.filter(user=self.user)

        return qs

    def _get_page_title(self):
        return self.user.get_full_name()


class RecipeDetailView(DetailView):
    """Page with Recipe details."""
    queryset = Recipe.objects.all()
    template_name = 'recipes/single_page.html'

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs
            .prefetch_related('recipe_ingredients__ingredient')
        )

        return qs

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            followed_by = Follow.objects.filter(
                following=self.object.user,
                follower=self.request.user
            ).exists()
            kwargs.update({'followed_by': followed_by})
        return super().get_context_data(**kwargs)


class SubscriptionsView(LoginRequiredMixin, ListView):
    """List of current user's subscriptions."""
    page_title = 'Мои подписки'
    context_object_name = 'subscriptions_list'
    paginate_by = settings.PAGINATED_BY
    template_name = 'recipes/subscriptions.html'
    queryset = User.objects.all()

    def get_queryset(self):
        """Display subscriptions with their recipes."""
        qs = super().get_queryset()
        users = User.objects.filter(following__follower=self.request.user)

        subscriptions_recipes_view = Subquery(
            Recipe.objects.filter(
                user_id=OuterRef('user_id')).values_list('id', flat=True)[:3]
        )
        prefetch = Prefetch(
            'recipes',
            queryset=Recipe.objects.filter(id__in=subscriptions_recipes_view)
        )
        qs = (users
              .prefetch_related(prefetch)
              .annotate(count=Count('recipes'))
              .order_by('-count'))

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({'page_title': 'Мои подписки'})
        context = super().get_context_data(**kwargs)

        return context


class CartListView(ListView):
    template_name = 'recipes/shopping_cart.html'
    queryset = Recipe.objects.all()
    context_object_name = 'shopping_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Recipe.objects.filter(in_cart__user=self.request.user)
        else:
            queryset = Recipe.objects.filter(
                id__in=self.request.session.get('cart')
            )

        return queryset


def parse_recipe(data, recipe):
    tags = []
    ingredients = {}
    for key, value in data.items():
        if value == 'on':
            tags.append(key)

        if key.startswith('nameIngredient_'):
            index = key.split('_')[1]
            ingredients[value] = data.get(f'valueIngredient_{index}')

    for slug in tags:
        tag = get_object_or_404(Tag, slug=slug)
        recipe.tag.add(tag)

    ingreds = []
    for name, value in ingredients.items():
        ingredient = get_object_or_404(Ingredient, name=name)
        combination = RecipeIngredient(
            ingredient=ingredient, recipe=recipe, quantity=value
        )
        ingreds.append(combination)
    RecipeIngredient.objects.bulk_create(ingreds)


@login_required
def new_recipe(request):
    tags = Tag.objects.all()
    if request.method != 'POST':
        form = RecipeForm()
        return render(
            request, 'recipes/new_recipe.html', {'form': form, 'tags': tags}
        )
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if not form.is_valid():
        return render(
            request,
            'recipes/new_recipe.html',
            {'form': form, 'tags': tags}
        )
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.user = request.user
        recipe.save()

        parse_recipe(request.POST, recipe)

    return redirect('detail', pk=recipe.id)


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    author = recipe.user
    if request.user != author:
        return redirect('detail', pk)

    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    tags = Tag.objects.all()

    if not form.is_valid():
        return render(
            request,
            'recipes/edit_recipe.html',
            {'form': form, 'recipe': recipe, 'tags': tags, 'edit_mode': True}
        )
    with transaction.atomic():
        form.save()
        RecipeIngredient.objects.filter(recipe=recipe).delete()

        parse_recipe(request.POST, recipe)

    return redirect('detail', pk=recipe.id)


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    author = recipe.user
    if request.user != author:
        return redirect('detail', pk)

    recipe.delete()
    return redirect('index')


def shopping_cart_download(request):
    if request.user.is_authenticated:
        cart = ShoppingCart.objects.filter(user=request.user)
        recipes = Recipe.objects.filter(in_cart__in=cart)
    else:
        recipes = Recipe.objects.filter(id__in=request.session['cart'])
    ingredients_list = RecipeIngredient.objects.filter(recipe__in=recipes)
    ingredients = {}
    for item in ingredients_list:
        name = item.ingredient.name
        if name in ingredients:
            ingredients[name]['quantity'] += item.quantity
        else:
            ingredients[name] = {
                'quantity': item.quantity,
                'unit': item.ingredient.unit
            }

    response = HttpResponse(
        content_type='text/csv,charset=utf8',
        headers={'Content-Disposition': 'attachment; filename="shopping_cart.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['СПИСОК ПОКУПОК:'])
    writer.writerow(['Ингредиент', 'количество', 'ед. измерения'])
    for item, value in ingredients.items():
        writer.writerow([f'{item}:', value["quantity"], value["unit"]])

    return response


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=status.HTTP_404_NOT_FOUND
    )


def server_error(request):
    return render(
        request,
        'misc/500.html',
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
