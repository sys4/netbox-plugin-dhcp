import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import PrimaryModelTable
from netbox_dhcp.models import Pool

from .mixins import (
    ClientClassTableMixin,
    EvaluateClientClassTableMixin,
    NetBoxDHCPTableMixin,
    SubnetTableMixin,
)

__all__ = (
    "PoolTable",
    "RelatedPoolTable",
    "ParentPoolTable",
)


class PoolTable(
    SubnetTableMixin,
    ClientClassTableMixin,
    EvaluateClientClassTableMixin,
    NetBoxDHCPTableMixin,
    PrimaryModelTable,
):
    class Meta(PrimaryModelTable.Meta):
        model = Pool

        fields = (
            "name",
            "description",
            "weight",
            "subnet",
            "ip_range",
            "client_classes",
            "evaluate_additional_classes",
            "tags",
        )

        default_columns = (
            "name",
            "weight",
            "subnet",
            "ip_range",
            "tags",
        )

    ip_range = tables.Column(
        verbose_name=_("IP Range"),
        linkify=True,
    )


class RelatedPoolTable(PoolTable):
    class Meta(PoolTable.Meta):
        fields = (
            "name",
            "description",
            "subnet",
        )

        default_columns = (
            "name",
            "description",
            "subnet",
        )

    actions = None


class ParentPoolTable(PoolTable):
    class Meta(PoolTable.Meta):
        pass

    actions = None
