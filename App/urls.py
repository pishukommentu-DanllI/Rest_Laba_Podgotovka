from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('cart/', CartAPI.as_view()),
    path('cart/<int:pk>/', CartAPI.as_view()),

    path('order/', OrderApi.as_view()),
    path('order/<int:pk>', OrderApi.as_view()),

    path('product/', include(router.urls))
]
