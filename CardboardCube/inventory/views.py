from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import UserInventory, InventoryItem, UserSubCollection, GradingDetails
from .serializers import UserInventorySerializer


class UserInventoryViewset(viewsets.ModelViewSet):
    """
    A viewset for User Inventories
    """
    queryset = UserInventory.objects.all()
    serializer_class = UserInventorySerializer
    permission_classes = (IsAdminUser,)


class InventoryItemViewset(viewsets.ViewSet):
    """
    A viewset for Inventory Items
    """
