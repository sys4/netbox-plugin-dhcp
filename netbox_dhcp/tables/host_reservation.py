import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import PrimaryModelTable
from netbox_dhcp.models import HostReservation

from .mixins import (
    ClientClassTableMixin,
    NetBoxDHCPTableMixin,
)

__all__ = (
    "HostReservationTable",
    "RelatedHostReservationTable",
    "ParentHostReservationTable",
)


class HostReservationTable(
    ClientClassTableMixin,
    NetBoxDHCPTableMixin,
    PrimaryModelTable,
):
    class Meta(PrimaryModelTable.Meta):
        model = HostReservation

        fields = (
            "name",
            "description",
            "duid",
            "circuit_id",
            "client_id",
            "flex_id",
            "client_classes",
            "next_server",
            "server_hostname",
            "boot_file_name",
            "hostname",
        )

        default_columns = (
            "name",
            "subnet",
            "ipv4_address",
            "ipv6_addresses",
            "hostname",
        )

    subnet = tables.Column(
        verbose_name=_("Subnet"),
        linkify=True,
    )
    dhcp_server = tables.Column(
        verbose_name=_("DHCP Server"),
        linkify=True,
    )

    hw_address = tables.Column(
        verbose_name=_("Hardware Address"),
        linkify=True,
    )

    ipv4_address = tables.Column(
        verbose_name=_("IPv4 Address"),
        linkify=True,
    )
    ipv6_addresses = tables.ManyToManyColumn(
        verbose_name=_("IPv6 Addresses"),
        linkify_item=True,
    )
    ipv6_prefixes = tables.ManyToManyColumn(
        verbose_name=_("IPv6 Prefixes"),
        linkify_item=True,
    )
    exlcuded_ipv6_prefixes = tables.ManyToManyColumn(
        verbose_name=_("Excluded IPv6 Prefixes"),
        linkify_item=True,
    )


class RelatedHostReservationTable(HostReservationTable):
    class Meta(HostReservationTable.Meta):
        fields = (
            "name",
            "description",
            "hostname",
            "duid",
            "circuit_id",
            "client_id",
            "flex_id",
        )

        default_columns = (
            "name",
            "description",
            "hostname",
        )

    actions = None


class ParentHostReservationTable(HostReservationTable):
    class Meta(HostReservationTable.Meta):
        pass

    actions = None
