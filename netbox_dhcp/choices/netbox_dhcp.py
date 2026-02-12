from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = (
    "AllocatorTypeChoices",
    "PDAllocatorTypeChoices",
)


class AllocatorTypeChoices(ChoiceSet):
    key = "NetBoxDHCP.allocator_types"

    ITERATIVE = "iterative"
    RANDOM = "random"
    FREE_LEASE_QUEUE = "flq"

    CHOICES = [
        (ITERATIVE, _("Iterative"), "blue"),
        (RANDOM, _("Random"), "red"),
        (FREE_LEASE_QUEUE, _("Free Lease Queue"), "green"),
    ]


class PDAllocatorTypeChoices(AllocatorTypeChoices):
    key = "NetBoxDHCP.pd_allocator_types"

    CHOICES = AllocatorTypeChoices.CHOICES
