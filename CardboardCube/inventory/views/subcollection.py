from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from CardboardCube.inventory.models import UserInventory, InventoryItem, UserSubCollection, GradingDetails
from CardboardCube.inventory.serializers import UserInventorySerializer


@api_view(['GET'])
def get_user_subcollections(request, user_pk, inv_pk):
    pass


@api_view(['POST'])
def create_user_inventory(request, user_pk, inv_pk):
    pass


@api_view(['DELETE'])
def delete_user_subcollection(request, user_pk, sub_pk):
    pass


@api_view(['PATCH'])
def update_user_subcollection(request, user_pk, sub_pk):
    pass
