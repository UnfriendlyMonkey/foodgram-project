from django.urls import include, path

from rest_framework.urlpatterns import format_suffix_patterns

from recipes import views
from .api.views import AddToFavorites, RemoveFromFavorites, AddSubscription, RemoveSubscription

views_patterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('favorites/', views.FavoriteView.as_view(), name='favorites'),
    path('profiles/<str:username>/', views.ProfileView.as_view(), name='profile'),  # noqa
    path('subscriptions/', views.SubscriptionsView.as_view(), name='subscriptions')
]

recipes_patterns = [
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='detail'),
    path('new/', views.new_recipe, name='new_recipe'),
]

purchases_patterns = [
    # path('', views.CartListView.as_view(), name='cart_view'),
    path('download/', views.shopping_cart_download, name='download')
]

api_patterns = [
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:pk>/', RemoveFromFavorites.as_view()),
    path('subscriptions/', AddSubscription.as_view()),
    path('subscriptions/<int:pk>/', RemoveSubscription.as_view()),
    # path('purchases/', AddToPurchases.as_view()),
    # path('purchases/<int:pk>/', RemoveFromPurchases.as_view()),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns))),
    path('recipes/', include(recipes_patterns, namespace='recipes')),
    path('purchases/', include(purchases_patterns, namespace='purchases')),
]
