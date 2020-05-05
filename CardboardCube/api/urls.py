from django.urls import path, include
from rest_framework import routers

from api.views import InventoryViewSet, SubCollectionViewSet

router = routers.SimpleRouter()
router.register('inventory', InventoryViewSet, basename='inventory')
router.register('subcollection', SubCollectionViewSet, basename='subcollection')

urlpatterns = router.urls
