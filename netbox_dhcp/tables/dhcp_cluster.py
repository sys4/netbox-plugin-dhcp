# import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import ChoiceFieldColumn, PrimaryModelTable
from netbox_dhcp.models import DHCPCluster

from .mixins import NetBoxDHCPTableMixin

__all__ = ("DHCPClusterTable",)


class DHCPClusterTable(NetBoxDHCPTableMixin, PrimaryModelTable):
    class Meta(PrimaryModelTable.Meta):
        model = DHCPCluster

        fields = (
            "name",
            "description",
        )

        default_columns = (
            "name",
            "status",
        )

    status = ChoiceFieldColumn(
        verbose_name=_("Status"),
    )
