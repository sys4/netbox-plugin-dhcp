from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search
from netbox_dhcp.choices import DHCPClusterStatusChoices

from .mixins import (
    NetBoxDHCPModelMixin,
)

__all__ = (
    "DHCPCluster",
    "DHCPClusterIndex",
)


class DHCPCluster(NetBoxDHCPModelMixin, PrimaryModel):
    class Meta:
        verbose_name = _("DHCP Cluster")
        verbose_name_plural = _("DHCP Clusters")

        ordering = ("name",)

    clone_fields = (
        "name",
        "description",
        "status",
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=DHCPClusterStatusChoices,
        default=DHCPClusterStatusChoices.STATUS_ACTIVE,
        blank=True,
    )

    def get_status_color(self):
        return DHCPClusterStatusChoices.colors.get(self.status)


@register_search
class DHCPClusterIndex(SearchIndex):
    model = DHCPCluster

    fields = (
        ("name", 100),
        ("description", 200),
    )
