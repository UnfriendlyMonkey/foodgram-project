from django import template
from recipes.models import Follow

register = template.Library()


@register.filter(name='followed_by')
def followed_by(user, request_user):
    return Follow.objects.filter(follower=request_user, following=user).exists()


@register.filter(name='get_tags')
def get_tags(qs):
    return qs.getlist('active_tags')


@register.filter(name='construct_tag_link')
def construct_tag_link(request, tag):
    new_request = request.GET.copy()
    tags = new_request.getlist('active_tags')

    if tag.slug in tags:
        tags.remove(tag.slug)
    else:
        tags.append(tag.slug)

    if new_request.__contains__('page'):
        new_request.pop('page')

    new_request.setlist('active_tags', tags)
    return new_request.urlencode()


@register.filter(name='construct_page_link')
def construct_page_link(request, page: int):
    new_request = request.GET.copy()
    # page_list = []
    # page_list.append(page)
    new_request.setlist('page', [str(page)])
    return new_request.urlencode()
