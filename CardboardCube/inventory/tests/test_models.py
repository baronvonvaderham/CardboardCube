# -*- coding: utf-8 -*-
from django.test import TestCase

from card_catalog.models import CardSet, Card
from inventory.exceptions import InvalidInventoryItemException
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
        self.assertEqual(len(subcollections), 10)

    def test_add_card_to_inventory__success(self):
        card_data = {
            'card': self.arid_mesa,
            'quantity_owned': 1,
            'is_foil': True,
        }
        inventory_item = self.inventory.add_card_to_inventory(card_data=card_data)
        self.assertIsInstance(inventory_item, InventoryItem)
        self.assertEqual(inventory_item.__str__(), 'NM Arid Mesa [EXP] Foil')

    def test_add_card_to_inventory__failure(self):
        card_data = {
            'card': 'Not a card',
            'quantity_owned': 1,
            'is_foil': 'This should not be a string',
        }
        with self.assertRaises(InvalidInventoryItemException):
            inventory_item = self.inventory.add_card_to_inventory(card_data=card_data)

    def test_inventory_items(self):
        card_data = {
            'card': self.arid_mesa,
            'quantity_owned': 1,
            'is_foil': True,
        }
        inventory_item1 = self.inventory.add_card_to_inventory(card_data=card_data)
        card_data = {
            'card': self.steam_vents,
            'quantity_owned': 1,
            'is_foil': True,
        }
        inventory_item2 = self.inventory.add_card_to_inventory(card_data=card_data)
        self.assertEqual(len(self.inventory.inventory_items), 2)

    def test_cubes(self):
        self.assertEqual(len(self.inventory.cubes), 2)
        for cube in self.inventory.cubes:
            self.assertIsInstance(cube, UserSubCollection)
            self.assertEqual(cube.kind, 'cube')

    def test_decks(self):
        self.assertEqual(len(self.inventory.cubes), 2)
        for deck in self.inventory.decks:
            self.assertIsInstance(deck, UserSubCollection)
            self.assertEqual(deck.kind, 'deck')

    def test_collections(self):
        self.assertEqual(len(self.inventory.collections), 2)
        for collection in self.inventory.collections:
            self.assertIsInstance(collection, UserSubCollection)
            self.assertEqual(collection.kind, 'collection')

    def test_tradelists(self):
        self.assertEqual(len(self.inventory.tradelists), 2)
        for tradelist in self.inventory.tradelists:
            self.assertIsInstance(tradelist, UserSubCollection)
            self.assertEqual(tradelist.kind, 'tradelist')

    def test_other(self):
        self.assertEqual(len(self.inventory.other_subcollections), 2)
        for other in self.inventory.other_subcollections:
            self.assertIsInstance(other, UserSubCollection)
            self.assertEqual(other.kind, 'other')
