from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search

from .mixins import (
    BOOTPModelMixin,
    LifetimeModelMixin,
    NetBoxDHCPModelMixin,
)
from .option import Option

__all__ = (
    "ClientClass",
    "ClientClassIndex",
)


class ClientClass(
    NetBoxDHCPModelMixin,
    BOOTPModelMixin,
    LifetimeModelMixin,
    PrimaryModel,
):
    class Meta:
        verbose_name = _("Client Class")
        verbose_name_plural = _("Client Classes")

        ordering = (
            "-weight",
            "name",
        )

    clone_fields = (
        "name",
        "description",
        "dhcp_server",
        "test",
        "template_test",
        "only_in_additional_list",
        "next_server",
        "server_hostname",
        "boot_file_name",
        "offer_lifetime",
        "valid_lifetime",
        "min_valid_lifetime",
        "max_valid_lifetime",
        "preferred_lifetime",
        "min_preferred_lifetime",
        "max_preferred_lifetime",
    )

    dhcp_server = models.ForeignKey(
        verbose_name=_("DHCP Server"),
        to="netbox_dhcp.DHCPServer",
        related_name="client_class_definition_set",
        on_delete=models.CASCADE,
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name=_("Weight"),
        default=100,
    )

    test = models.TextField(
        verbose_name=_("Test"),
        blank=True,
    )
    template_test = models.TextField(
        verbose_name=_("Template Test"),
        blank=True,
    )
    only_in_additional_list = models.BooleanField(
        verbose_name=_("Only in additional list"),
        help_text=_(
            "Evaluate the client class template test only if it is used in additional lists"
        ),
        null=True,
        blank=True,
    )
    options = GenericRelation(
        to=Option,
        content_type_field="assigned_object_type",
        object_id_field="assigned_object_id",
    )


@register_search
class ClientClassIndex(SearchIndex):
    model = ClientClass

    fields = (
        ("name", 100),
        ("description", 200),
        ("next_server", 300),
        ("server_hostname", 300),
        ("boot_file_name", 300),
    )
