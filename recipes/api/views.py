from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite


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
