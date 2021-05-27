from rest_framework import status, mixins, viewsets, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import IngredientSerializer
from recipes.models import Favorite, Follow, Ingredient, ShoppingCart as Cart


class AddToFavorites(APIView):
    """Add a Recipe to Favorites of a User"""

    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data.get('id'),
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):
    """Remove a Recipe from User's Favorites"""

    def delete(self, request, pk, format=None):
        object_to_del = generics.get_object_or_404(
            Favorite, recipe_id=pk, user=request.user
        )
        object_to_del.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddSubscription(APIView):
    """Follow the User"""

    def post(self, request, format=None):
        Follow.objects.get_or_create(
            follower=request.user,
            following_id=request.data.get('id'),
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveSubscription(APIView):
    """Unfollow the User"""

    def delete(self, request, pk, format=None):
        object_to_del = generics.get_object_or_404(
            Follow, following_id=pk, follower=request.user
        )
        object_to_del.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddPurchase(APIView):
    """Add recipes to shopping cart"""

    def post(self, request):
        recipe_id = request.data.get('id')
        if request.user.is_authenticated:
            Cart.objects.get_or_create(
                user=request.user,
                recipe_id=recipe_id,
            )
            return Response({'success': True}, status=status.HTTP_200_OK)

        if 'cart' not in request.session:
            request.session['cart'] = [recipe_id]
        if recipe_id in request.session['cart']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.session['cart'].append(recipe_id)
        request.session.modified = True
        return Response({'success': True}, status=status.HTTP_200_OK)


class DeletePurchase(APIView):
    """Remove recipes from shopping cart"""

    def delete(self, request, pk):
        if request.user.is_authenticated:
            object_to_del = generics.get_object_or_404(
                Cart, user=request.user, recipe_id=pk
            )
            object_to_del.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        request.session['cart'].remove(str(pk))
        request.session.modified = True
        return Response({'success': True}, status=status.HTTP_200_OK)


class IngredientsViewSet(generics.ListAPIView):
    """Get list of ingredients in new or edit recipe form"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """Returns queryset filtered by first letters of query"""
        query = self.request.query_params.get('query')
        if not query:
            return Ingredient.objects.all()
        ingredients = Ingredient.objects.filter(name__contains=query)
        return ingredients
