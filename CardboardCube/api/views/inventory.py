from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from inventory.models import UserInventory
from api.serializers import UserInventorySerializer
from registration.models import User


class InventoryViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = UserInventorySerializer

    def retrieve(self, request, *args, **kwargs):
        owner = User.objects.get(pk=kwargs['pk'])
        if request.user != owner:
            return Response(status=403, data='You are not the owner of this inventory.')
        try:
            inventory = UserInventory.objects.get(owner=owner)
        except ObjectDoesNotExist:
            return Response(status=404, data="No inventory found for user.")
        serializer = UserInventorySerializer(inventory)
        return Response(status=200, data={'RETRIEVE WORKED!!!!!!!!!!!!!!': serializer.data})

    def create(self, request, *args, **kwargs):
        return Response(status=200, data={'CREATE WORKED!!!!!!!!!!!!!!'})

    def destroy(self, request, *args, **kwargs):
        return Response(status=200, data={'DESTROY WORKED!!!!!!!!!!!!!!'})

    def update(self, request, *args, **kwargs):
        return Response(status=200, data={'UPDATE WORKED!!!!!!!!!!!!!!'})
