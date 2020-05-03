# -*- coding: utf-8 -*-
from django.test import TestCase

from card_catalog.models import CardSet, Card
from inventory.models import (
    UserInventory,
    UserSubCollection,
    InventoryItem,
    GradingDetails,
)
from registration.models import User


class TestInventoryModels(TestCase):
    """
    Tests for Inventory models
    """
    fixtures = ['card_catalog.json', 'inventory.json']

    def setUp(self):
        self.user = User.objects.get(email="test_user@domain.com")
        self.inventory = UserInventory.objects.get(owner=self.user)
        self.arid_mesa = Card.objects.get(pk=1)
        self.steam_vents = Card.objects.get(pk=2)

    def test_fixture_stuff_exists(self):
        card_sets = CardSet.objects.all()
        cards = Card.objects.all()
        users = User.objects.all()
        inventories = UserInventory.objects.all()
        subcollections = UserSubCollection.objects.all()

        self.assertEqual(len(card_sets), 1)
        self.assertEqual(len(cards), 45)
        self.assertEqual(len(users), 2)
        self.assertEqual(len(inventories), 1)
        self.assertEqual(len(subcollections), 11)

    def test_add_card_to_inventory(self):
        card_data = {
            'card': self.arid_mesa,
            'quantity_owned': 1,
            'is_foil': True,
        }
        inventory_item = self.inventory.add_card_to_inventory(card_data=card_data)
        self.assertIsInstance(inventory_item, InventoryItem)
        self.assertEqual(inventory_item.__str__(), 'NM Arid Mesa [EXP] Foil')
