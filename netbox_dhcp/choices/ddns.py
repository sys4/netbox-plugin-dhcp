from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = (
    "DDNSReplaceClientNameChoices",
    "DDNSConflictResolutionModeChoices",
)


class DDNSReplaceClientNameChoices(ChoiceSet):
    key = "DDNS.replace_client_name"

    NEVER = "never"
    ALWAYS = "always"
    WHEN_PRESENT = "when_present"
    WHEN_NOT_PRESENT = "when_not_present"

    CHOICES = [
        (NEVER, _("Never"), "red"),
        (ALWAYS, _("Always"), "green"),
        (WHEN_PRESENT, _("When Present"), "blue"),
        (WHEN_NOT_PRESENT, _("When Not Present"), "orange"),
    ]


class DDNSConflictResolutionModeChoices(ChoiceSet):
    CHECK_WITH_DHCID = "check-with-dhcid"
    NO_CHECK_WITH_DHCID = "no-check-with-dhcid"
    CHECK_EXISTS_WITH_DHCID = "check-exists-with-dhcid"
    NO_CHECK_WITHOUT_DHCID = "no-check-without-dhcid"

    CHOICES = [
        (CHECK_WITH_DHCID, _("Overwrite existing records with matching DHCID"), "red"),
        (NO_CHECK_WITH_DHCID, _("Overwrite existing records and add DHCID"), "green"),
        (
            CHECK_EXISTS_WITH_DHCID,
            _("Overwrite existing records with any DHCID"),
            "blue",
        ),
        (
            NO_CHECK_WITHOUT_DHCID,
            _("Overwrite existing records and do not add DHCID"),
            "orange",
        ),
    ]
