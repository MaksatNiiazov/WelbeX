from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CargoViewSet

router = DefaultRouter()
router.register(r'cargoes', CargoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
