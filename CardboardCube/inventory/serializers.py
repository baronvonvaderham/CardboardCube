from .models import UserInventory, UserSubCollection, InventoryItem, GradingDetails

from rest_framework import serializers


class UserInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInventory
        fields = '__all__'


class UserSubCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubCollection
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'


class GradingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingDetails
        fields = '__all__'
