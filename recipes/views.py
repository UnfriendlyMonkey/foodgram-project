from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from recipes.models import Recipe, User


class IsFavoriteMixin:
    """Add annotation with favorite mark to the View."""

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('author')
            .with_is_favorite(user_id=self.request.user.id)
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
        qs = qs.filter(favorites__user=self.request.user)

        return qs


class ProfileView(BaseRecipeListView):
    """User's page with its name and list of authored Recipes."""
    template_name = 'recipes/author_recipes_list.html'

    def get(self, request, *args, **kwargs):
        """Store `user` parameter for data filtration purposes."""
        self.user = get_object_or_404(User, username=kwargs.get('username'))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = qs.filter(author=self.user)

        return qs

    def _get_page_title(self):
        """Get page title."""
        return self.user.get_full_name()


class RecipeDetailView(IsFavoriteMixin, DetailView):
    """Page with Recipe details."""
    queryset = Recipe.objects.all()
    template_name = 'recipes/recipe_detail.html'

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs
            .prefetch_related('recipe_ingredients__ingredient')
            .with_is_favorite(user_id=self.request.user.id)
        )

        return qs
