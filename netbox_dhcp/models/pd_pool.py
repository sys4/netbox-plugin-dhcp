from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation

from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search
from ipam.models import Prefix
from ipam.choices import IPAddressFamilyChoices
from utilities.querysets import RestrictedQuerySet

from .mixins import (
    NetBoxDHCPModelMixin,
    ClientClassModelMixin,
    EvaluateClientClassModelMixin,
)
from .option import Option

__all__ = (
    "PDPool",
    "PDPoolIndex",
)


class PDPoolManager(models.Manager.from_queryset(RestrictedQuerySet)):
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


class PDPool(
    NetBoxDHCPModelMixin,
    ClientClassModelMixin,
    EvaluateClientClassModelMixin,
    PrimaryModel,
):
    class Meta:
        verbose_name = _("Prefix Delegation Pool")
        verbose_name_plural = _("Prefix Delegation Pools")

        ordering = (
            "-weight",
            "name",
        )

    clone_fields = (
        "name",
        "description",
        "delegated_length",
        "client_classes",
        "evaluate_additional_classes",
    )

    subnet = models.ForeignKey(
        verbose_name=_("Parent Subnet"),
        to="netbox_dhcp.Subnet",
        on_delete=models.CASCADE,
        related_name="child_pd_pools",
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name=_("Weight"),
        default=100,
    )

    objects = PDPoolManager()

    pool_id = models.PositiveIntegerField(
        verbose_name=_("Pool ID"),
        blank=True,
        null=True,
    )
    prefix = models.ForeignKey(
        verbose_name=_("IPv6 Prefix"),
        to=Prefix,
        related_name="netbox_dhcp_pd_pools",
        on_delete=models.PROTECT,
    )
    delegated_length = models.IntegerField(
        verbose_name=_("Delegated Length"),
        validators=[MinValueValidator(0), MaxValueValidator(128)],
    )
    excluded_prefix = models.ForeignKey(
        verbose_name=_("Excluded IPv6 Prefix"),
        to=Prefix,
        related_name="netbox_dhcp_pd_excluded_pools",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    options = GenericRelation(
        to=Option,
        content_type_field="assigned_object_type",
        object_id_field="assigned_object_id",
    )

    @property
    def family(self):
        return IPAddressFamilyChoices.FAMILY_6

    @property
    def parent_dhcp_server(self):
        return self.subnet.parent_dhcp_server

    @property
    def available_client_classes(self):
        return self.subnet.available_client_classes

    def clean(self):
        super().clean()

        if self.subnet.family != 6:
            raise ValidationError(
                {
                    "subnet": _("Subnet family must be IPv6"),
                }
            )

        if self.prefix.family != 6:
            raise ValidationError(
                {
                    "prefix": _("Prefix family must be IPv6"),
                }
            )

        if self.excluded_prefix and self.excluded_prefix.family != 6:
            raise ValidationError(
                {
                    "excluded_prefix": _("Excluded prefix family must be IPv6"),
                }
            )

        if self.delegated_length < self.prefix.prefix.prefixlen:
            raise ValidationError(
                {
                    "delegated_length": _(
                        "Delegated length must not be shorter than the length of the prefix"
                    ),
                }
            )

        if (
            self.excluded_prefix
            and self.excluded_prefix.prefix not in self.prefix.prefix
        ):
            raise ValidationError(
                {
                    "excluded_prefix": _(
                        "Excluded prefix must be a sub-prefix of the prefix"
                    ),
                }
            )

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)


@register_search
class PDPoolIndex(SearchIndex):
    model = PDPool

    fields = (
        ("name", 100),
        ("description", 200),
    )
