from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from dcim.models import MACAddress
from ipam.models import IPAddress, Prefix
from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search

from .mixins import (
    BOOTPModelMixin,
    ClientClassModelMixin,
    NetBoxDHCPModelMixin,
)
from .option import Option

__all__ = (
    "HostReservation",
    "HostReservationIndex",
)


class HostReservation(
    NetBoxDHCPModelMixin,
    ClientClassModelMixin,
    BOOTPModelMixin,
    PrimaryModel,
):
    class Meta:
        verbose_name = _("Host Reservation")
        verbose_name_plural = _("Host Reservations")

        ordering = ("name",)

        constraints = [
            models.CheckConstraint(
                condition=Q(
                    Q(dhcp_server__isnull=False, subnet__isnull=True)
                    | Q(dhcp_server__isnull=True, subnet__isnull=False)
                ),
                name="host_reservation_unique_parent_object",
                violation_error_message=_(
                    "Either DHCP Server or Subnet is required, not both"
                ),
            )
        ]

    clone_fields = (
        "name",
        "description",
        "circuit_id",
        "flex_id",
        "hostname",
        "dhcp_server",
        "subnet",
        "client_classes",
    )

    duid = models.CharField(
        verbose_name=_("DUID"),
        blank=True,
        null=True,
        max_length=255,
    )
    hw_address = models.ForeignKey(
        verbose_name=_("Hardware Address"),
        to=MACAddress,
        related_name="netbox_dhcp_host_reservations",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    flex_id = models.CharField(
        verbose_name=_("Flex ID"),
        blank=True,
        null=True,
        max_length=255,
    )
    # IPv4 only
    circuit_id = models.CharField(
        verbose_name=_("Circuit ID"),
        blank=True,
        null=True,
        max_length=255,
    )
    # IPv4 only
    client_id = models.CharField(
        verbose_name=_("Client ID"),
        blank=True,
        null=True,
        max_length=255,
    )
    hostname = models.CharField(
        verbose_name=_("Hostname"),
        blank=True,
        null=True,
        max_length=255,
    )

    dhcp_server = models.ForeignKey(
        verbose_name=_("DHCP Server"),
        to="netbox_dhcp.DHCPServer",
        on_delete=models.CASCADE,
        related_name="child_host_reservations",
        blank=True,
        null=True,
    )
    subnet = models.ForeignKey(
        verbose_name=_("Subnet"),
        to="netbox_dhcp.Subnet",
        on_delete=models.CASCADE,
        related_name="child_host_reservations",
        blank=True,
        null=True,
    )

    ipv4_address = models.ForeignKey(
        verbose_name=_("IPv4 Addresses"),
        to=IPAddress,
        related_name="netbox_dhcp_ipv4_host_reservations",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    ipv6_addresses = models.ManyToManyField(
        verbose_name=_("IPv6 Addresses"),
        to=IPAddress,
        related_name="netbox_dhcp_ipv6_host_reservations",
    )
    ipv6_prefixes = models.ManyToManyField(
        verbose_name=_("IPv6 Prefixes"),
        to=Prefix,
        related_name="netbox_dhcp_ipv6_host_reservations",
    )
    excluded_ipv6_prefixes = models.ManyToManyField(
        verbose_name=_("Excluded IPv6 Prefixes"),
        to=Prefix,
        related_name="netbox_dhcp_excluded_ipv6_host_reservations",
    )
    options = GenericRelation(
        to=Option,
        content_type_field="assigned_object_type",
        object_id_field="assigned_object_id",
    )

    @property
    def family(self):
        return self.subnet.family if self.subnet else None


@register_search
class HostReservationIndex(SearchIndex):
    model = HostReservation

    fields = (
        ("name", 100),
        ("duid", 150),
        ("hw_address", 150),
        ("circuit_id", 150),
        ("client_id", 150),
        ("flex_id", 150),
        ("hostname", 180),
        ("description", 200),
    )
