from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from inventory.models import UserSubCollection
from api.serializers import UserSubCollectionSerializer
from registration.models import User


class SubCollectionViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = UserSubCollectionSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(status=200, data={'RETRIEVE WORKED!!!!!!!!!!!!!!'})

    def create(self, request, *args, **kwargs):
        return Response(status=200, data={'CREATE WORKED!!!!!!!!!!!!!!'})

    def destroy(self, request, *args, **kwargs):
        return Response(status=200, data={'DESTROY WORKED!!!!!!!!!!!!!!'})

    def update(self, request, *args, **kwargs):
        return Response(status=200, data={'UPDATE WORKED!!!!!!!!!!!!!!'})
