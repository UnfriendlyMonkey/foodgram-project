from django import template
from recipes.models import Follow

register = template.Library()


@register.filter(name='followed_by')
def followed_by(user, request_user):
    return Follow.objects.filter(follower=request_user, following=user).exists()
