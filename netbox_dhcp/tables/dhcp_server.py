import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import ChoiceFieldColumn, PrimaryModelTable, columns
from netbox_dhcp.models import DHCPServer

from .mixins import (
    ClientClassTableMixin,
    NetBoxDHCPTableMixin,
)

__all__ = ("DHCPServerTable",)


class DHCPServerTable(
    ClientClassTableMixin,
    NetBoxDHCPTableMixin,
    PrimaryModelTable,
):
    class Meta(PrimaryModelTable.Meta):
        model = DHCPServer

        fields = (
            "name",
            "description",
            "status",
            "dhcp_cluster",
            "device",
            "virtual_machine",
            "server_id",
            "echo_client_id",
            "client_classes",
            "tags",
        )

        default_columns = (
            "name",
            "status",
            "dhcp_cluster",
        )

    status = ChoiceFieldColumn(
        verbose_name=_("Status"),
    )
    dhcp_cluster = tables.Column(
        verbose_name=_("DHCP Cluster"),
        linkify=True,
    )

    device = tables.Column(
        verbose_name=_("Device"),
        linkify=True,
    )
    device_interfaces = columns.ManyToManyColumn(
        verbose_name=_("Device Interfaces"),
        linkify_item=True,
    )
    virtual_machine = tables.Column(
        verbose_name=_("Virtual Machine"),
        linkify=True,
    )
    virtual_machine_interfaces = columns.ManyToManyColumn(
        verbose_name=_("Virtual Machine Interfaces"),
        linkify_item=True,
    )
    server_id = ChoiceFieldColumn(
        verbose_name=_("Server DUID"),
    )
