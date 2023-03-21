from django.contrib import admin
from django.urls import path, include
from App.views import show
urlpatterns = [
    path('', show),
    path('admin/', admin.site.urls),
    path('api/v1/', include('App.urls')),
    path('api/auth/', include('djoser.urls.authtoken'))
]
