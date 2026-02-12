from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = ("HostReservationIdentifierChoices",)


class HostReservationIdentifierChoices(ChoiceSet):
    key = "HostReservation.identifiers"

    CIRCUIT_ID = "circuit-id"
    HW_ADDRESS = "hw-address"
    DUID = "duid"
    CLIENT_ID = "client-id"

    CHOICES = [
        (CIRCUIT_ID, _("Circuit ID"), "blue"),
        (HW_ADDRESS, _("Hardware Address"), "red"),
        (DUID, "DUID", "green"),
        (CLIENT_ID, _("Client ID"), "orange"),
    ]
