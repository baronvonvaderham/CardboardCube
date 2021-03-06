import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from inventory.exceptions import (
    InvalidInventoryItemException,
    InvalidGradingDetailsException,
)


class UserInventory(models.Model):
    """
    Class to contain a user's default, overall inventory that will contain all InventoryItem objects they own.
    """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    owner = models.ForeignKey('registration.User', on_delete=models.CASCADE)
    inventory_items = models.ManyToManyField('InventoryItem', blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('User Inventory')
        verbose_name_plural = _('User Inventories')

    def __str__(self):
        return f"{self.owner.username}'s Inventory"

    @property
    def cubes(self):
        kind = dict(UserSubCollection.KIND_CHOICES).get('CUBE')
        return UserSubCollection.objects.filter(owner=self.owner, kind=kind)

    @property
    def decks(self):
        kind = dict(UserSubCollection.KIND_CHOICES).get('DECK')
        return UserSubCollection.objects.filter(owner=self.owner, kind=kind)

    @property
    def collections(self):
        kind = dict(UserSubCollection.KIND_CHOICES).get('COLLECTION')
        return UserSubCollection.objects.filter(owner=self.owner, kind=kind)

    @property
    def tradelists(self):
        kind = dict(UserSubCollection.KIND_CHOICES).get('TRADELIST')
        return UserSubCollection.objects.filter(owner=self.owner, kind=kind)

    @property
    def other_subcollections(self):
        kind = dict(UserSubCollection.KIND_CHOICES).get('OTHER')
        return UserSubCollection.objects.filter(owner=self.owner, kind=kind)

    def add_items_to_inventory(self, inventory_item_pks):
        for pk in inventory_item_pks:
            try:
                inventory_item = InventoryItem.objects.get(pk=pk)
            except ObjectDoesNotExist as err:
                raise InvalidInventoryItemException({'Errors': f'Unable to retrieve inventory item to add: {err}'})
            self.inventory_items.add(inventory_item)
        return self.save()

    def remove_items_from_inventory(self, inventory_item_pks):
        for pk in inventory_item_pks:
            try:
                inventory_item = InventoryItem.objects.get(pk=pk)
            except ObjectDoesNotExist as err:
                raise InvalidInventoryItemException({'Errors': f'Unable to retrieve inventory item to add: {err}'})
            self.inventory_items.remove(inventory_item)
        return self.save()


class UserSubCollection(models.Model):
    """
    Class to contain information about a collection within a user's inventory.
    """

    KIND_CHOICES = [
        ('CUBE', 'cube'),
        ('DECK', 'deck'),
        ('COLLECTION', 'collection'),
        ('TRADELIST', 'tradelist'),
        ('OTHER', 'other'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    kind_override = models.CharField(null=True, max_length=56)
    description = models.TextField(null=True, max_length=256)
    owner = models.ForeignKey('registration.User', on_delete=models.CASCADE)
    inventory_items = models.ManyToManyField('InventoryItem', blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('User Sub-Collection')
        verbose_name_plural = _('User Sub-Collections')

    def __str__(self):
        collection_type = self.kind_override if self.kind == 'other' else self.kind
        return f"{self.owner.username}'s {collection_type}"

    def add_items_to_subcollection(self, inventory_item_pks):
        for pk in inventory_item_pks:
            try:
                inventory_item = InventoryItem.objects.get(pk=pk)
            except ObjectDoesNotExist as err:
                raise InvalidInventoryItemException({'Errors': f'Unable to retrieve inventory item to add: {err}'})
            self.inventory_items.add(inventory_item)
        return self.save()

    def remove_items_from_subcollection(self, inventory_item_pks):
        for pk in inventory_item_pks:
            try:
                inventory_item = InventoryItem.objects.get(pk=pk)
            except ObjectDoesNotExist as err:
                raise InvalidInventoryItemException({'Errors': f'Unable to retrieve inventory item to add: {err}'})
            self.inventory_items.remove(inventory_item)
        return self.save()


class InventoryItem(models.Model):
    """
    Class to contain the items entered into a user's inventory, then can be further linked to sub-collections.
    """
    DEFAULT_CONDITION = 'NM'
    CONDITION_CHOICES = (
        ('M', 'Mint'),
        ('NM', 'Near Mint'),
        ('LP', 'Lightly Played'),
        ('MP', 'Moderately Played'),
        ('HP', 'Heavily Played'),
        ('DMG', 'Damaged')
    )
    DEFAULT_LANGUAGE = 'EN'
    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('ZH', 'Chinese Traditional'),
        ('ZH-S', 'Chinese Simplified'),
        ('FR', 'French'),
        ('DE', 'German'),
        ('IT', 'Italian'),
        ('JA', 'Japanese'),
        ('KO', 'Korean'),
        ('PT', 'Portuguese'),
        ('RU', 'Russian'),
        ('ES', 'Spanish')
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    quantity_owned = models.IntegerField(default=0)
    quantity_wanted = models.IntegerField(default=0, null=True)
    card = models.ForeignKey('card_catalog.Card', null=True, blank=True, on_delete=models.SET_NULL)
    condition = models.CharField(
        max_length=3, choices=CONDITION_CHOICES, default=DEFAULT_CONDITION, help_text=_("Card condition")
    )
    language = models.CharField(
        max_length=4, choices=LANGUAGE_CHOICES, default=DEFAULT_LANGUAGE, help_text=_("Card language?")
    )
    is_foil = models.BooleanField(default=False, help_text=_("Is the card foil?"))
    is_signed = models.BooleanField(default=False, help_text=_("Is the card signed?"))
    is_altered = models.BooleanField(default=False, help_text=_("Is the card altered?"))
    is_misprint = models.BooleanField(default=False, help_text=_("Is the card misprinted?"))
    is_miscut = models.BooleanField(default=False, help_text=_("Is the card miscut?"))
    is_graded = models.BooleanField(default=False, help_text=_("Is the card graded?"))

    grading_details = models.ForeignKey('GradingDetails', null=True, on_delete=models.SET_NULL,
                                        help_text=_("Details of card grade"))
    owner = models.ForeignKey('registration.User', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = _('Inventory Item')
        verbose_name_plural = _('Inventory Items')

    def __str__(self):
        if self.is_graded and self.grading_details:
            prefix = f"{self.grading_details.determine_abbreviation()}"
        else:
            prefix = self.condition
        name = f"{prefix} {self.card}"
        CHECK_FIELDS = {
            'is_foil': 'Foil',
            'is_signed': 'Signed',
            'is_altered': 'Altered',
            'is_misprint': 'Misprint',
            'is_miscut': 'Miscut',
        }
        for field, field_name in CHECK_FIELDS.items():
            if self.__getattribute__(field):
                name += f" {field_name}"
        return name

    def add_grading_details(self, grading_data):
        try:
            grading_details = GradingDetails.objects.create(
                grading_service=grading_data.get('grading_service'),
                serial_number=grading_data.get('serial_number'),
                overall_grade=grading_data.get('overall_grade'),
                autograph_grade=grading_data.get('autograph_grade'),
                centering_grade=grading_data.get('centering_grade'),
                corners_grade=grading_data.get('corners_grade'),
                edges_grade=grading_data.get('edges_grade'),
                surface_grade=grading_data.get('surface_grade')
            )
        except (ValueError, TypeError, IntegrityError) as err:
            raise InvalidGradingDetailsException({'Errors': f'Unable to add grading details: {err}'})
        self.grading_details = grading_details
        self.is_graded = True
        return self.save()


class GradingDetails(models.Model):
    """
    Class to contain details for graded cards entered into inventory
    """

    GRADING_SERVICES = (
        ('BGS', 'Beckett Grading Services'),
        ('BAS', 'Beckett Authentication Services'),
        ('PSA', 'Professional Sports Authentication')
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    grading_service = models.CharField(max_length=32, choices=GRADING_SERVICES)
    serial_number = models.CharField(max_length=12)
    overall_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    autograph_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    centering_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    corners_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    edges_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)
    surface_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)

    objects = models.Manager()

    class Meta:
        verbose_name = _('Grading Details')
        verbose_name_plural = _('Grading Details')

    def determine_abbreviation(self):
        subgrades = [self.centering_grade, self.corners_grade, self.edges_grade, self.surface_grade]
        base = 'Q'
        modifier = ''
        for sub in subgrades:
            if sub < self.overall_grade:
                base = 'B'
            if sub > self.overall_grade:
                modifier += '+'
        formatted_grade = f'{self.overall_grade:.1f}'
        return f'{formatted_grade} {base}{modifier}'
