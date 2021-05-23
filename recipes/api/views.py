from rest_framework import status, mixins, viewsets, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.api.serializers import IngredientSerializer
from recipes.models import Favorite, Follow, Ingredient, ShoppingCart as Cart


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


class ShoppingCart(APIView):
    """Add recipes to shopping card of authorized User and remove them"""

    def post(self, request):
        recipe_id = request.data.get('id')
        if request.user.is_authenticated:
            Cart.objects.get_or_create(
                user=request.user,
                recipe_id=recipe_id,
            )
            return Response({'success': True}, status=status.HTTP_200_OK)

        if 'cart' not in request.session.keys():
            request.session['cart'] = [recipe_id]
        else:
            if recipe_id in request.session['cart']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                request.session['cart'].append(recipe_id)
                request.session.modified = True
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user, recipe_id=pk).delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        print(request.session['cart'])
        print(pk)
        request.session['cart'].remove(str(pk))
        request.session.modified = True
        return Response({'success': True}, status=status.HTTP_200_OK)


class IngredientsViewSet(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """
        Returns queryset filtered by first letters of query.
        """
        query = self.request.query_params.get('query')
        print(query)
        if query:
            ingredients = Ingredient.objects.filter(name__contains=query)[:25]
            print(ingredients)
            return ingredients
        return Ingredient.objects.all()
