import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserInventory(models.Model):
    """
    Class to contain a user's default, overall inventory that will contain all InventoryItem objects they own.
    """

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    owner = models.ForeignKey('registration.User', on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return "{}'s Inventory".format(self.owner.username)


class UserSubCollection(models.Model):
    """
    Class to contain information about a collection within a user's inventory.
    """

    TYPE_CHOICES = [
        ('CUBE', 'Cube'),
        ('DECK', 'Deck'),
        ('COLLECTION', 'Collection'),
        ('TRADELIST', 'Tradelist'),
        ('OTHER', 'Other'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    type_override = models.CharField(max_length=56)
    description = models.TextField(max_length=256)
    owner = models.ForeignKey('registration.User', on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        collection_type = self.type_override if self.type == 'Other' else self.type
        return "{}'s {}}".format(self.owner.username, collection_type)


class InventoryItem(models.Model):
    """
    Class to contain the items entered into a user's inventory, then can be further linked to sub-collections.
    """

    CONDITION_CHOICES = (
        ('M', 'Mint'),
        ('NM', 'Near Mint'),
        ('LP', 'Lightly Played'),
        ('MP', 'Moderately Played'),
        ('HP', 'Heavily Played'),
        ('DMG', 'Damaged')
    )

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
    quantity_wanted = models.IntegerField(default=0)
    card = models.ForeignKey('card_catalog.Card', null=True, blank=True, on_delete=models.SET_NULL)
    condition = models.CharField(max_length=3, choices=CONDITION_CHOICES, help_text=_("Card condition"))
    language = models.CharField(max_length=4, choices=LANGUAGE_CHOICES, help_text=_("Card language?"))
    is_foil = models.BooleanField(default=False, help_text=_("Is the card foil?"))
    is_signed = models.BooleanField(default=False, help_text=_("Is the card signed?"))
    is_altered = models.BooleanField(default=False, help_text=_("Is the card altered?"))
    is_misprint = models.BooleanField(default=False, help_text=_("Is the card misprinted?"))
    is_miscut = models.BooleanField(default=False, help_text=_("Is the card miscut?"))
    is_graded = models.BooleanField(default=False, help_text=_("Is the card graded?"))

    collections = models.ManyToManyField('UserSubCollection')
    grading_details = models.ForeignKey('GradingDetails', null=True, on_delete=models.SET_NULL,
                                        help_text=_("Details of card grade"))
    inventory = models.ForeignKey('UserInventory', null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey('registration.User', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = _('inventory_item')
        verbose_name_plural = _('inventory_items')

    def __str__(self):
        name = "{condition} {card_name} [{card_set}]".format(
            condition=self.condition,
            card_name=self.card.name,
            card_set=self.card.set.code
        )
        name += " Foil" if self.is_foil else name
        name += " Signed" if self.is_signed else name
        name += " Altered" if self.is_altered else name
        name += " Misprint" if self.is_misprint else name
        name += " Miscut" if self.is_miscut else name
        if self.is_graded and self.grading_details:
            name = "{} ".format(self.grading_details.overall_grade) + name
        return name


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
    surfaces_grade = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=3)

    objects = models.Manager()

    class Meta:
        verbose_name = _('grading_details')

    def determine_abbreviation(self):
        subgrades = [self.centering_grade, self.corners_grade, self.edges_grade, self.surfaces_grade]
        base = 'Q'
        modifier = ''
        for sub in subgrades:
            if sub < self.overall_grade:
                base = 'B'
            if sub > self.overall_grade:
                modifier += '+'
        return base + modifier
