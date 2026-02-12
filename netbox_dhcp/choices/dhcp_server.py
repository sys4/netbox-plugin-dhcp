from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = (
    "DHCPServerStatusChoices",
    "DHCPServerIDTypeChoices",
)


class DHCPServerStatusChoices(ChoiceSet):
    key = "DHCPServer.status"

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    CHOICES = [
        (STATUS_ACTIVE, _("Active"), "blue"),
        (STATUS_INACTIVE, _("Inactive"), "red"),
    ]


class DHCPServerIDTypeChoices(ChoiceSet):
    ID_EN = "EN"
    ID_LLT = "LLT"
    ID_LL = "LL"

    CHOICES = [
        (ID_EN, "EN", "blue"),
        (ID_LLT, "LLT", "red"),
        (ID_LL, "LL", "green"),
    ]
