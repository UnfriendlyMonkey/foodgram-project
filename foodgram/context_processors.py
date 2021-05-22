from recipes.models import ShoppingCart


def cart_count(request):
    """
    A context processor making 'cart_count' variable available in templates
    """
    if request.user.is_authenticated:
        return {
            'cart_count': ShoppingCart.objects.filter(user=request.user).count()
        }
    return {'cart_count': len(request.session['cart'])}