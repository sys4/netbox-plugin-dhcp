from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError

from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search
from ipam.models import IPRange

from .mixins import (
    NetBoxDHCPModelMixin,
    ClientClassModelMixin,
    EvaluateClientClassModelMixin,
    DDNSUpdateModelMixin,
)
from .option import Option

__all__ = (
    "Pool",
    "PoolIndex",
)


class Pool(
    NetBoxDHCPModelMixin,
    ClientClassModelMixin,
    EvaluateClientClassModelMixin,
    DDNSUpdateModelMixin,
    PrimaryModel,
):
    class Meta:
        verbose_name = _("Pool")
        verbose_name_plural = _("Pools")

        ordering = (
            "-weight",
            "name",
        )

    clone_fields = (
        "name",
        "description",
        "subnet",
        "client_classes",
        "evaluate_additional_classes",
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

    subnet = models.ForeignKey(
        verbose_name=_("Subnet"),
        to="netbox_dhcp.Subnet",
        related_name="child_pools",
        on_delete=models.CASCADE,
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name=_("Weight"),
        default=100,
    )

    pool_id = models.PositiveIntegerField(
        verbose_name=_("Pool ID"),
        blank=True,
        null=True,
    )
    ip_range = models.ForeignKey(
        verbose_name=_("IP Range"),
        to=IPRange,
        related_name="netbox_dhcp_pools",
        on_delete=models.PROTECT,
    )
    options = GenericRelation(
        to=Option,
        content_type_field="assigned_object_type",
        object_id_field="assigned_object_id",
    )

    @property
    def family(self):
        return self.ip_range.family if self.ip_range else None

    @property
    def parent_dhcp_server(self):
        return self.subnet.parent_dhcp_server

    @property
    def available_client_classes(self):
        return self.subnet.available_client_classes

    def clean(self):
        super().clean()

        ip_range = self.ip_range.range
        prefix = self.subnet.prefix.prefix

        if ip_range not in prefix:
            raise ValidationError(
                {
                    "ip_range": _(
                        "IP Range {range} is not within subnet {subnet} ({prefix})"
                    ).format(
                        range=str(ip_range),
                        subnet=self.subnet.name,
                        prefix=self.subnet.prefix,
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)


@register_search
class PoolIndex(SearchIndex):
    model = Pool

    fields = (
        ("name", 100),
        ("description", 200),
    )
