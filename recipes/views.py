from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from recipes.forms import RecipeForm
from recipes.models import Recipe, User, Follow


class IsFavoriteMixin:
    """Add annotation with favorite mark to the View."""

    def get_queryset(self):
        """Annotate with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('user')
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
            .with_is_favorite(user_id=self.request.user.id)
        )

        return qs


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

        qs = User.objects.filter(following__follower=self.request.user).order_by('username').prefetch_related('recipes')

        print(qs)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Мои подписки'

        return context


@login_required
def new_recipe(request):
    if request.method != 'POST':
        form = RecipeForm()
        return render(request, 'new_recipe.html', {'form': form})
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.user = request.user
        recipe.save()
        return redirect('index')
    return render(
        request,
        'new_recipe.html',
        {'form': form}
    )


# @login_required
# def follow_index(request):
#     post_list = Post.objects.filter(author__following__user=request.user)
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#
#     return render(
#         request,
#         "follow.html",
#         {"page": page, "paginator": paginator}
#     )


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
