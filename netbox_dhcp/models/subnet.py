from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError

from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search
from ipam.models import Prefix
from utilities.querysets import RestrictedQuerySet

from .mixins import (
    NetBoxDHCPModelMixin,
    ClientClassModelMixin,
    EvaluateClientClassModelMixin,
    BOOTPModelMixin,
    LifetimeModelMixin,
    DDNSUpdateModelMixin,
    LeaseModelMixin,
    NetworkModelMixin,
)
from .option import Option

__all__ = (
    "Subnet",
    "SubnetIndex",
)


class SubnetManager(models.Manager.from_queryset(RestrictedQuerySet)):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                prefix_display=models.ExpressionWrapper(
                    models.F("prefix__prefix"),
                    output_field=models.CharField(),
                )
            )
        )


class Subnet(
    NetBoxDHCPModelMixin,
    ClientClassModelMixin,
    EvaluateClientClassModelMixin,
    BOOTPModelMixin,
    LifetimeModelMixin,
    DDNSUpdateModelMixin,
    LeaseModelMixin,
    NetworkModelMixin,
    PrimaryModel,
):
    class Meta:
        verbose_name = _("Subnet")
        verbose_name_plural = _("Subnets")

        ordering = (
            "-weight",
            "name",
        )

        constraints = [
            models.UniqueConstraint(
                fields=["subnet_id"], name="subnet_unique_subnet_id"
            ),
            models.CheckConstraint(
                condition=Q(
                    Q(dhcp_server__isnull=False, shared_network__isnull=True)
                    | Q(dhcp_server__isnull=True, shared_network__isnull=False)
                ),
                name="subnet_unique_parent_object",
                violation_error_message=_(
                    "Either DHCP Server or Shared Network is required, not both"
                ),
            ),
        ]

    clone_fields = (
        "name",
        "description",
        "dhcp_server",
        "shared_network",
        "next_server",
        "server_hostname",
        "boot_file_name",
        "client_classes",
        "evaluate_additional_classes",
        "offer_lifetime",
        "valid_lifetime",
        "min_valid_lifetime",
        "max_valid_lifetime",
        "preferred_lifetime",
        "min_preferred_lifetime",
        "max_preferred_lifetime",
        "renew_timer",
        "rebind_timer",
        "match_client_id",
        "authoritative",
        "reservations_global",
        "reservations_out_of_pool",
        "reservations_in_subnet",
        "calculate_tee_times",
        "t1_percent",
        "t2_percent",
        "cache_threshold",
        "cache_max_age",
        "adaptive_lease_time_threshold",
        "store_extended_info",
        "allocator",
        "pd_allocator",
        "relay",
        "interface_id",
        "rapid_commit",
        "hostname_char_set",
        "hostname_char_replacement",
        "ddns_send_updates",
        "ddns_override_no_update",
        "ddns_override_client_update",
        "ddns_replace_client_name",
        "ddns_generated_prefix",
        "ddns_qualifying_suffix",
        "ddns_update_on_renew",
        "ddns_conflict_resolution_mode",
        "ddns_ttl_percent",
        "ddns_ttl",
        "ddns_ttl_min",
        "ddns_ttl_max",
    )

    objects = SubnetManager()

    subnet_id = models.PositiveIntegerField(
        verbose_name=_("Subnet ID"),
        blank=True,
        null=False,
    )

    dhcp_server = models.ForeignKey(
        verbose_name=_("DHCP Server"),
        to="netbox_dhcp.DHCPServer",
        on_delete=models.CASCADE,
        related_name="child_subnets",
        blank=True,
        null=True,
    )
    shared_network = models.ForeignKey(
        verbose_name=_("Shared Network"),
        to="netbox_dhcp.SharedNetwork",
        on_delete=models.CASCADE,
        related_name="child_subnets",
        blank=True,
        null=True,
    )

    prefix = models.ForeignKey(
        verbose_name=_("Prefix"),
        to=Prefix,
        related_name="netbox_dhcp_subnets",
        on_delete=models.PROTECT,
        null=False,
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name=_("Weight"),
        default=100,
    )

    options = GenericRelation(
        to=Option,
        content_type_field="assigned_object_type",
        object_id_field="assigned_object_id",
    )

    @property
    def family(self):
        return self.prefix.family if self.prefix else None

    @property
    def parent_dhcp_server(self):
        if self.shared_network is not None:
            return self.shared_network.dhcp_server

        return self.dhcp_server

    @property
    def available_client_classes(self):
        return self.parent_dhcp_server.client_classes.all()

    def clean(self):
        super().clean()

        if not self.shared_network:
            return

        if (prefix := self.prefix).prefix not in (
            shared_network := self.shared_network
        ).prefix.prefix:
            raise ValidationError(
                {
                    "prefix": _(
                        "Prefix {prefix} is not within shared network {shared_network} ({shared_network_prefix})"
                    ).format(
                        prefix=prefix,
                        shared_network=shared_network.name,
                        shared_network_prefix=shared_network.prefix,
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.clean()

        if self.subnet_id is None:
            max_subnet_id = (
                0
                if (
                    max_id := Subnet.objects.aggregate(models.Max("subnet_id")).get(
                        "subnet_id__max"
                    )
                )
                is None
                else max_id
            )
            self.subnet_id = max_subnet_id + 1

        self.full_clean()

        super().save(*args, **kwargs)


@register_search
class SubnetIndex(SearchIndex):
    model = Subnet

    fields = (
        ("name", 100),
        ("description", 200),
        ("next_server", 300),
        ("server_hostname", 300),
        ("boot_file_name", 300),
    )
