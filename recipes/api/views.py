from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Follow


class AddToFavorites(APIView):
    """Add a Recipe to Favorites of a User."""

    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):
    """Remove a Recipe from User's Favorites."""

    def delete(self, request, pk, format=None):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddSubscription(APIView):
    """Follow the User."""

    def post(self, request, format=None):
        print(request.data, request.user)
        Follow.objects.get_or_create(
            follower=request.user,
            following_id=request.data['id'],
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveSubscription(APIView):
    """Unfollow the User."""

    def delete(self, request, pk, format=None):
        print(pk, request.data)
        Follow.objects.filter(following_id=pk, follower=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


# аналогичные функции из старого проекта yatube
# @login_required
# def profile_follow(request, username):
#     author = get_object_or_404(User, username=username)
#     if author != request.user:
#         follow_link = Follow.objects.get_or_create(user=request.user, author=author)
#     return redirect('profile', username)
#
#
# @login_required
# def profile_unfollow(request, username):
#     author = get_object_or_404(User, username=username)
#     follow_link = Follow.objects.get(user=request.user, author=author)
#     if follow_link:
#         follow_link.delete()
#     return redirect('profile', username)