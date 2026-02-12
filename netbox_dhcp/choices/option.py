from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

__all__ = (
    "OptionSendChoices",
    "OptionSpaceChoices",
    "OptionTypeChoices",
)


class OptionSendChoices(ChoiceSet):
    ALWAYS_SEND = "always-send"
    NEVER_SEND = "never-send"

    CHOICES = [
        (ALWAYS_SEND, "Always Send"),
        (NEVER_SEND, "Never Send"),
    ]


class OptionSpaceChoices(ChoiceSet):
    key = "Option.spaces"

    DHCPV6 = "dhcp6"
    DHCPV4 = "dhcp4"
    VENDOR = "vendor-specific-options-space"

    CHOICES = [
        (DHCPV6, "DHCPv6", "blue"),
        (DHCPV4, "DHCPv4", "green"),
        (VENDOR, "Vendor Specific", "orange"),
    ]


class OptionTypeChoices(ChoiceSet):
    key = "Option.types"

    TYPE_BINARY = "binary"
    TYPE_BOOLEAN = "boolean"
    TYPE_EMPTY = "empty"
    TYPE_FQDN = "fqdn"
    TYPE_IPV4_ADDRESS = "ipv4-address"
    TYPE_IPV6_ADDRESS = "ipv6-address"
    TYPE_IPV6_PREFIX = "ipv6-prefix"
    TYPE_PSID = "psid"
    TYPE_RECORD = "record"
    TYPE_STRING = "string"
    TYPE_TUPLE = "tuple"
    TYPE_UINT8 = "uint8"
    TYPE_UINT16 = "uint16"
    TYPE_UINT32 = "uint32"
    TYPE_INT8 = "int8"
    TYPE_INT16 = "int16"
    TYPE_INT32 = "int32"

    CHOICES = [
        (TYPE_BINARY, _("Binary")),
        (TYPE_BOOLEAN, _("Boolean")),
        (TYPE_EMPTY, _("Empty")),
        (TYPE_FQDN, _("Fully Qualified Domain Name")),
        (TYPE_IPV4_ADDRESS, _("IPv4 Address")),
        (TYPE_IPV6_ADDRESS, _("IPv6 Address")),
        (TYPE_IPV6_PREFIX, _("IPv6 Prefix")),
        (TYPE_PSID, _("PSID")),
        (TYPE_RECORD, _("Record")),
        (TYPE_STRING, _("String")),
        (TYPE_TUPLE, _("Tuple")),
        (TYPE_UINT8, _("8 Bit Unsigned Integer")),
        (TYPE_UINT16, _("16 Bit Unsigned Integer")),
        (TYPE_UINT32, _("32 Bit Unsigned Integer")),
        (TYPE_INT8, _("8 Bit Signed Integer")),
        (TYPE_INT16, _("16 Bit Signed Integer")),
        (TYPE_INT32, _("32 Bit Signed Integer")),
    ]
