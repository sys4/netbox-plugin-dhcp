import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import ChoiceFieldColumn, NetBoxTable, TagColumn

__all__ = (
    "NetBoxDHCPTableMixin",
    "DHCPServerTableMixin",
    "ClientClassTableMixin",
    "EvaluateClientClassTableMixin",
    "DDNSUpdateTableMixin",
    "LeaseTableMixin",
    "SubnetTableMixin",
)


class NetBoxDHCPTableMixin(NetBoxTable):
    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    tags = TagColumn(
        url_name="plugins:netbox_dhcp:subnet_list",
    )


class DHCPServerTableMixin(NetBoxTable):
    dhcp_server = tables.Column(
        verbose_name=_("DHCP Server"),
        linkify=True,
    )


class ClientClassTableMixin(NetBoxTable):
    client_classes = tables.ManyToManyColumn(
        verbose_name=_("Client Classes"),
        linkify_item=True,
    )


class EvaluateClientClassTableMixin(NetBoxTable):
    evaluate_additional_classes = tables.ManyToManyColumn(
        verbose_name=_("Evaluate Additional Classes"),
        linkify_item=True,
    )


class PrefixTableMixin(NetBoxTable):
    prefix = tables.Column(
        verbose_name=_("Prefix"),
        linkify=True,
    )


class DDNSUpdateTableMixin(NetBoxTable):
    ddns_replace_client_name = ChoiceFieldColumn(
        verbose_name=_("Replace Client Name"),
    )
    ddns_conflict_resolution_mode = ChoiceFieldColumn(
        verbose_name=_("Conflict Resolution Mode"),
    )


class LeaseTableMixin(NetBoxTable):
    allocator = ChoiceFieldColumn(
        verbose_name=_("Allocator"),
    )
    pd_allocator = ChoiceFieldColumn(
        verbose_name=_("Prefix Delegation Allocator"),
    )


class SubnetTableMixin(NetBoxTable):
    subnet = tables.Column(
        verbose_name=_("Subnet"),
        linkify=True,
    )
