from django.urls import include, path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import AddToFavorites, RemoveFromFavorites, AddSubscription,\
    RemoveSubscription, IngredientsViewSet, AddPurchase, DeletePurchase

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
    path('', include(format_suffix_patterns(api_patterns)))
]
