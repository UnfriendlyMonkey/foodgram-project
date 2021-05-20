import io

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Subquery, Prefetch, OuterRef, Count
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
import pdfkit

from recipes.forms import RecipeForm
from recipes.models import Recipe, User, Follow, Ingredient, Tag, RecipeIngredient, ShoppingCart


class IsFavoriteMixin:
    """Add annotation with favorite mark to the View."""

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('user')
            .with_favorite_and_cart(user_id=self.request.user.id)
        )

        return qs


class BaseRecipeListView(IsFavoriteMixin, ListView):
    """Base view for Recipe list."""
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = 6
    page_title = None

    def get_context_data(self, **kwargs):
        """Add page title to the context."""
        kwargs.update({'page_title': self._get_page_title()})

        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        """Get page title."""
        assert self.page_title, f"Attribute 'page_title' not set for {self.__class__.__name__}"

        return self.page_title


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
        # TO DO - уточнить название фильтра
        qs = qs.filter(favorites__user=self.request.user)

        return qs


class ProfileView(BaseRecipeListView):
    """User's page with its name and list of authored Recipes."""
    template_name = 'recipes/author_recipes_list.html'

    def get(self, request, *args, **kwargs):
        """Store `user` parameter for data filtration purposes."""
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
        """Get page title."""
        return self.user.get_full_name()


class RecipeDetailView(IsFavoriteMixin, DetailView):
    """Page with Recipe details."""
    queryset = Recipe.objects.all()
    template_name = 'recipes/single_page.html'

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs
            .prefetch_related('recipe_ingredients__ingredient')
            .with_favorite_and_cart(user_id=self.request.user.id)
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
    paginate_by = 6
    template_name = 'recipes/subscriptions.html'
    queryset = User.objects.all()

    def get_queryset(self):
        """Display subscriptions with their recipes."""
        qs = super().get_queryset()
        users = User.objects\
            .filter(following__follower=self.request.user)

        subscriptions_recipes_view = Subquery(Recipe.objects
                                              .filter(user_id=OuterRef('user_id'))
                                              .values_list('id', flat=True)[:3])
        prefetch = Prefetch('recipes',
                            queryset=Recipe.objects
                            .filter(id__in=subscriptions_recipes_view))
        # TODO: как ограничить поля только нужными? values() не работает с Prefetch
        qs = (users
              .prefetch_related(prefetch)
              .annotate(count=Count('recipes'))
              .order_by('-count'))

        # qs = User.objects.filter(following__follower=self.request.user).order_by('username').prefetch_related('recipes')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({'page_title': "Мои подписки"})
        context = super().get_context_data(**kwargs)

        return context


class CartListView(ListView):
    template_name = 'recipes/shopping_cart.html'
    queryset = Recipe.objects.all()
    context_object_name = 'shopping_list'

    def get_queryset(self):
        queryset = Recipe.objects.filter(in_cart__user=self.request.user)

        return queryset


def parse_recipe(data):
    tags = []
    ingredients = {}
    for key, value in data.items():
        print(key, value)
        if value == 'on':
            tags.append(key)
        if key.startswith('nameIngredient'):
            index = key.split('_')[1]
            ingredients[value] = data.get(f'valueIngredient_{index}')
    return tags, ingredients


@login_required
def new_recipe(request):
    if request.method != 'POST':
        form = RecipeForm()
        tags = Tag.objects.all()
        return render(request, 'recipes/new_recipe.html', {'form': form, 'tags': tags})
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    print(form.data)
    print(form.is_valid())
    print(form.errors)
    tags, ingredients = parse_recipe(request.POST)

    if form.is_valid():
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            for slug in tags:
                tag = get_object_or_404(Tag, slug=slug)
                print(tag)
                recipe.tag.add(tag)
            recipe.save()

            ingreds = []
            for name, value in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=name)
                combination = RecipeIngredient(ingredient=ingredient, recipe=recipe, quantity=value)
                ingreds.append(combination)
            RecipeIngredient.objects.bulk_create(ingreds)
            form.save_m2m()  # TODO - check if it's necessary here
        return redirect('detail', pk=recipe.id)
    return render(
        request,
        'recipes/new_recipe.html',
        {'form': form}
    )


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
        if name in ingredients.keys():
            ingredients[name]['quantity'] += item.quantity
        else:
            ingredients[name] = {
                'quantity': item.quantity,
                'unit': item.ingredient.unit
            }
    to_string = render_to_string(
        'recipes/cart_to_load.html', {'ingredients': ingredients}
    )
    to_pdf = pdfkit.from_string(to_string, False)
    buffer = io.BytesIO(to_pdf)
    return FileResponse(buffer, as_attachment=True, filename='shopping_cart.pdf')


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        "misc/500.html",
        status=500
    )
