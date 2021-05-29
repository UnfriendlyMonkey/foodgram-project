"""foodgram URL Configuration"""

from django.conf import settings
from django.conf.urls import include
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

handler404 = 'recipes.views.page_not_found'
handler500 = 'recipes.views.server_error'

urlpatterns = [
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('', include('recipes.urls')),
    path('api/', include('api.urls')),
]
