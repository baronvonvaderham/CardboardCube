# -*- coding: utf-8 -*-
from django.test import TestCase

from card_catalog.models import CardSet, Card
from inventory.exceptions import InvalidInventoryItemException, InvalidGradingDetailsException
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


class TestInventoryItemAndGradingDetails(InventoryModelsTestCase):
    """
    Tests for UserInventory model and methods, as well as grading details.
    Grading details has no methods of its own, and there are grading details
    methods attached to InventoryItem, so it makes sense to combine those into
    a single testing class.
    """
    def setUp(self):
        super(TestInventoryItemAndGradingDetails, self).setUp()

    def test_add_grading_details__success(self):
        # Kaitlynn's Yule Ooze grading data used :D
        grading_data = {
            'grading_service': 'Beckett Grading Services',
            'serial_number': '0011664787',
            'overall_grade': 9.5,
            'centering_grade': 9.5,
            'corners_grade': 9,
            'edges_grade': 9.5,
            'surface_grade': 9.5
        }
        self.inventory_item1.add_grading_details(grading_data=grading_data)
        # Re-Query to make sure it's committed to the db
        queried_item = InventoryItem.objects.get(pk=self.inventory_item1.pk)
        self.assertIsInstance(queried_item.grading_details, GradingDetails)

        # This card's a basic bitch, so it should just have "B" for its abbreviation
        self.assertEqual(queried_item.grading_details.determine_abbreviation(), "B")

        # Update it to be a Quad, so should be "Q"
        queried_item.grading_details.corners_grade = 9.5
        queried_item.grading_details.save()
        self.assertEqual(queried_item.grading_details.determine_abbreviation(), "Q")

        # Bump one grade up to a 10 and this should be "Q+" now
        queried_item.grading_details.surface_grade = 10
        queried_item.grading_details.save()
        self.assertEqual(queried_item.grading_details.determine_abbreviation(), "Q+")

        # Bump a second one up to a 10 for "Q++"
        queried_item.grading_details.edges_grade = 10
        queried_item.grading_details.save()
        self.assertEqual(queried_item.grading_details.determine_abbreviation(), "Q++")

        # Bump a third one up to a 10 for "Q+++" (I guess if you have ONE really low grade)
        queried_item.grading_details.centering_grade = 10
        queried_item.grading_details.save()
        self.assertEqual(queried_item.grading_details.determine_abbreviation(), "Q+++")

        # Now if the overall grade is a 10 but the subs stay the same, it should be back to "B"
        queried_item.grading_details.overall_grade = 10
        queried_item.grading_details.save()
        self.assertEqual(queried_item.grading_details.determine_abbreviation(), "B")

    def test_add_grading_details__failure(self):
        grading_data = {
            'grading_service': 'Not a grading service',
            'serial_number': '0011664787',
            'overall_grade': 9.5,
            'centering_grade': 9.5,
            'corners_grade': 9,
            'edges_grade': 9.5,
            'surface_grade': 9.5
        }
        with self.assertRaises(InvalidGradingDetailsException):
            self.inventory_item1.add_grading_details(grading_data=grading_data)


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
