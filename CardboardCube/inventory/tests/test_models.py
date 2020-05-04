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


class InventoryModelsTestCase(TestCase):
    """
    Common data setup for these test classes
    """
    fixtures = ['card_catalog.json', 'inventory.json']

    def setUp(self):
        self.user = User.objects.get(email="test_user@domain.com")
        self.inventory = UserInventory.objects.get(owner=self.user)
        self.collection = self.inventory.collections.first()
        self.arid_mesa = Card.objects.get(pk=1)
        self.steam_vents = Card.objects.get(pk=2)
        self.inventory_item1 = InventoryItem.objects.create(
            owner=self.user, card=self.arid_mesa, quantity_owned=1, is_foil=True
        )
        self.inventory_item2 = InventoryItem.objects.create(
            owner=self.user, card=self.steam_vents, quantity_owned=1, is_foil=True
        )
        self.pk_list = [self.inventory_item1.pk, self.inventory_item2.pk]
        self.item_names = ['NM Arid Mesa [EXP] Foil', 'NM Steam Vents [EXP] Foil']

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


class TestInventory(InventoryModelsTestCase):
    """
    Tests for UserInventory model and methods
    """
    def setUp(self):
        super(TestInventory, self).setUp()

    def test_inventory_name(self):
        self.assertEqual(self.inventory.__str__(), f"{self.user.username}'s Inventory")

    def test_add_items_to_inventory__success(self):
        self.inventory.add_items_to_inventory(self.pk_list)
        for item in self.inventory.inventory_items.all():
            self.assertIn(item.__str__(), self.item_names)

    def test_add_items_to_inventory__failure(self):
        with self.assertRaises(InvalidInventoryItemException):
            self.inventory.add_items_to_inventory([999999999999999999999])

    def test_remove_items_from_inventory__success(self):
        self.inventory.add_items_to_inventory(self.pk_list)
        items = self.inventory.inventory_items.all()
        self.assertEqual(len(items), 2)
        self.inventory.remove_items_from_inventory(self.pk_list)
        items = self.inventory.inventory_items.all()
        self.assertEqual(len(items), 0)

    def test_remove_items_from_inventory__failure(self):
        with self.assertRaises(InvalidInventoryItemException):
            self.inventory.remove_items_from_inventory([999999999999999999999])

    def test_cubes(self):
        self.assertEqual(len(self.inventory.cubes), 2)
        for cube in self.inventory.cubes:
            self.assertIsInstance(cube, UserSubCollection)
            self.assertEqual(cube.kind, 'cube')
            self.assertEqual(cube.__str__(), f"{self.user.username}'s {cube.kind}")

    def test_decks(self):
        self.assertEqual(len(self.inventory.cubes), 2)
        for deck in self.inventory.decks:
            self.assertIsInstance(deck, UserSubCollection)
            self.assertEqual(deck.kind, 'deck')
            self.assertEqual(deck.__str__(), f"{self.user.username}'s {deck.kind}")

    def test_collections(self):
        self.assertEqual(len(self.inventory.collections), 2)
        for collection in self.inventory.collections:
            self.assertIsInstance(collection, UserSubCollection)
            self.assertEqual(collection.kind, 'collection')
            self.assertEqual(
                collection.__str__(), f"{self.user.username}'s {collection.kind}"
            )

    def test_tradelists(self):
        self.assertEqual(len(self.inventory.tradelists), 2)
        for tradelist in self.inventory.tradelists:
            self.assertIsInstance(tradelist, UserSubCollection)
            self.assertEqual(tradelist.kind, 'tradelist')
            self.assertEqual(
                tradelist.__str__(), f"{self.user.username}'s {tradelist.kind}"
            )

    def test_other(self):
        self.assertEqual(len(self.inventory.other_subcollections), 2)
        for other in self.inventory.other_subcollections:
            self.assertIsInstance(other, UserSubCollection)
            self.assertEqual(other.kind, 'other')
            self.assertEqual(
                other.__str__(), f"{self.user.username}'s {other.kind_override}"
            )


class TestSubCollection(InventoryModelsTestCase):
    """
    Tests for UserSubCollection model and methods
    """
    def setUp(self):
        super(TestSubCollection, self).setUp()

    def test_add_items_to_subcollection__success(self):
        self.collection.add_items_to_subcollection(self.pk_list)
        for item in self.collection.inventory_items.all():
            self.assertIn(item.__str__(), self.item_names)

    def test_add_items_to_subcollection__failure(self):
        with self.assertRaises(InvalidInventoryItemException):
            self.collection.add_items_to_subcollection([999999999999999999999])

    def test_remove_items_from_subcollection__success(self):
        self.collection.add_items_to_subcollection(self.pk_list)
        items = self.collection.inventory_items.all()
        self.assertEqual(len(items), 2)
        self.collection.remove_items_from_subcollection(self.pk_list)
        items = self.collection.inventory_items.all()
        self.assertEqual(len(items), 0)

    def test_remove_items_from_subcollection__failure(self):
        with self.assertRaises(InvalidInventoryItemException):
            self.collection.remove_items_from_subcollection([999999999999999999999])
