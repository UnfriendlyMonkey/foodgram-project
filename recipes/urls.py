from django.urls import include, path

from rest_framework.urlpatterns import format_suffix_patterns

from recipes import views
from .api.views import AddToFavorites, RemoveFromFavorites, AddSubscription,\
    RemoveSubscription, IngredientsViewSet, AddPurchase, DeletePurchase

views_patterns = [
    path('',
        views.IndexView.as_view(), name='index'),
    path('favorites/',
        views.FavoriteView.as_view(), name='favorites'),
    path('profiles/<str:username>/',
        views.ProfileView.as_view(), name='profile'),
    path('profiles/',
        views.ProfileView.as_view(), name='profile'),
    path('subscriptions/',
        views.SubscriptionsView.as_view(), name='subscriptions'),
    path('recipes/<int:pk>/',
        views.RecipeDetailView.as_view(), name='detail'),
    path('recipes/<int:pk>/edit/',
        views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:pk>/delete/',
        views.delete_recipe, name='delete_recipe'),
    path('recipes/new/',
        views.new_recipe, name='new_recipe'),
    path('purchases/download/',
        views.shopping_cart_download, name='download'),
    path('purchases/',
        views.CartListView.as_view(), name='cart_view')
]

api_patterns = [
    path('ingredients', IngredientsViewSet.as_view()),
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:pk>/', RemoveFromFavorites.as_view()),
    path('subscriptions/', AddSubscription.as_view()),
    path('subscriptions/<int:pk>/', RemoveSubscription.as_view()),
    path('purchases/', AddPurchase.as_view(), name='cart_add'),
    path('purchases/<int:pk>/', DeletePurchase.as_view(), name='cart_delete'),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns)))
]
