import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import PrimaryModelTable
from netbox_dhcp.models import PDPool

from .mixins import (
    ClientClassTableMixin,
    EvaluateClientClassTableMixin,
    NetBoxDHCPTableMixin,
    SubnetTableMixin,
)

__all__ = (
    "PDPoolTable",
    "RelatedPDPoolTable",
    "ParentPDPoolTable",
)


class PDPoolTable(
    SubnetTableMixin,
    ClientClassTableMixin,
    EvaluateClientClassTableMixin,
    NetBoxDHCPTableMixin,
    PrimaryModelTable,
):
    class Meta(PrimaryModelTable.Meta):
        model = PDPool

        fields = (
            "name",
            "description",
            "weight",
            "subnet",
            "prefix",
            "delegated_length",
            "excluded_prefix",
            "client_classes",
            "evaluate_additional_classes",
            "tags",
        )

        default_columns = (
            "name",
            "weight",
            "subnet",
            "prefix",
            "delegated_length",
            "tags",
        )

    prefix = tables.Column(
        verbose_name=_("IPv6 Prefix"),
        linkify=True,
    )
    excluded_prefix = tables.Column(
        verbose_name=_("Excluded IPv6 Prefix"),
        linkify=True,
    )


class RelatedPDPoolTable(PDPoolTable):
    class Meta(PDPoolTable.Meta):
        fields = (
            "name",
            "description",
            "subnet",
            "excluded_prefix",
        )

        default_columns = (
            "name",
            "description",
            "subnet",
            "excluded_prefix",
        )

    actions = None


class ParentPDPoolTable(PDPoolTable):
    class Meta(PDPoolTable.Meta):
        pass

    actions = None
