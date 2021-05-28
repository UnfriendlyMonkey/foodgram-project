from django import template
from recipes.models import Favorite, Follow, ShoppingCart

register = template.Library()


@register.filter(name='is_followed_by')
def is_followed_by(user, request_user):
    return Follow.objects.filter(follower=request_user, following=user).exists()


@register.filter(name='get_tags')
def get_tags(qs):
    """Gets active tags to mark tags selectors as checked """
    return qs.getlist('active_tags')


@register.filter(name='construct_tag_link')
def construct_tag_link(request, tag):
    """Adds checked tags to url to make a filtration"""
    new_request = request.GET.copy()
    tags = new_request.getlist('active_tags')

    if tag.slug in tags:
        tags.remove(tag.slug)
    else:
        tags.append(tag.slug)

    if new_request.__contains__('page'):
        new_request.pop('page')

    new_request.setlist('active_tags', tags)
    new_request.setlist('tag', tags)
    return new_request.urlencode()


@register.filter(name='construct_page_link')
def construct_page_link(request, page: int):
    """Adds page number to url without deleting active tags from it"""
    new_request = request.GET.copy()
    new_request.setlist('page', [str(page)])
    return new_request.urlencode()


@register.filter
def is_favorite(recipe, user):
    """Checks if recipe is in favorites for current user"""
    return Favorite.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def is_in_cart(recipe, request):
    """Cheks if recipe is in cart for current user
    depending upon its authentication status"""
    if request.user.is_authenticated:
        return ShoppingCart.objects.filter(recipe=recipe, user=request.user).exists()
    if 'cart' not in request.session:
        request.session['cart'] = []
    return (str(recipe.id) in request.session['cart'])
