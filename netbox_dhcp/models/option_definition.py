from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from ipam.choices import IPAddressFamilyChoices
from netbox.models import PrimaryModel
from netbox.search import SearchIndex, register_search
from netbox_dhcp.choices import OptionSpaceChoices, OptionTypeChoices
from netbox_dhcp.fields import ChoiceArrayField

__all__ = (
    "OptionDefinition",
    "OptionDefinitionIndex",
)


class OptionDefinition(PrimaryModel):
    class Meta:
        verbose_name = _("Option Definition")
        verbose_name_plural = _("Option Definitions")

        ordering = (
            "space",
            "code",
            "name",
        )

        constraints = [
            models.CheckConstraint(
                condition=Q(
                    Q(
                        standard=True,
                        dhcp_server__isnull=True,
                        client_class__isnull=True,
                    )
                    | Q(
                        standard=False,
                        dhcp_server__isnull=False,
                        client_class__isnull=True,
                    )
                    | Q(
                        standard=False,
                        dhcp_server__isnull=True,
                        client_class__isnull=False,
                    )
                ),
                violation_error_message=_(
                    "Option definitions must either be standard or have a unique parent object"
                ),
                name="option_definition_standard_or_unique_parent_object",
            ),
            models.UniqueConstraint(
                fields=["space", "name"],
                name="standard_option_definition_unique_name",
                condition=Q(standard=True),
                violation_error_message=_(
                    "Standard option definitions must be uniqe in space and name"
                ),
            ),
            models.UniqueConstraint(
                fields=["space", "code"],
                name="standard_option_definition_unique_code",
                condition=Q(standard=True),
                violation_error_message=_(
                    "Standard option definitions must be uniqe in space and code"
                ),
            ),
            models.UniqueConstraint(
                fields=["space", "name", "dhcp_server"],
                name="global_option_definition_unique_name",
                condition=Q(dhcp_server__isnull=False),
                violation_error_message=_(
                    "Global custom option definitions must be uniqe in space and name"
                ),
            ),
            models.UniqueConstraint(
                fields=["space", "code", "dhcp_server"],
                name="global_option_definition_unique_code",
                condition=Q(dhcp_server__isnull=False),
                violation_error_message=_(
                    "Global custom option definitions must be uniqe in space and code"
                ),
            ),
            models.UniqueConstraint(
                fields=["space", "name", "client_class"],
                name="client_class_option_definition_unique_name",
                condition=Q(client_class__isnull=False),
                violation_error_message=_(
                    "Classification custom option definitions must be uniqe in space and name"
                ),
            ),
            models.UniqueConstraint(
                fields=["space", "code", "client_class"],
                name="client_class_option_definition_unique_code",
                condition=Q(client_class__isnull=False),
                violation_error_message=_(
                    "Classification custom option definitions must be uniqe in space and code"
                ),
            ),
        ]

    clone_fields = ("space",)

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=False,
        null=False,
    )
    family = models.PositiveIntegerField(
        verbose_name=_("Address Family"),
        choices=IPAddressFamilyChoices,
        blank=False,
        null=False,
        default=IPAddressFamilyChoices.FAMILY_4,
    )
    space = models.CharField(
        verbose_name=_("Space"),
        choices=OptionSpaceChoices,
        blank=False,
        null=False,
        default=OptionSpaceChoices.DHCPV4,
    )
    code = models.PositiveIntegerField(
        verbose_name=_("Code"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(255),
        ],
        blank=False,
        null=False,
    )
    type = models.CharField(
        verbose_name=_("Type"),
        choices=OptionTypeChoices,
        blank=False,
        null=False,
    )
    record_types = ChoiceArrayField(
        base_field=models.CharField(
            choices=OptionTypeChoices,
        ),
        verbose_name=_("Record Types"),
        blank=True,
        null=True,
    )
    encapsulate = models.CharField(
        verbose_name=_("Encapsulate"),
        blank=True,
        null=True,
    )
    array = models.BooleanField(
        verbose_name=_("Array"),
        null=True,
        blank=True,
    )
    standard = models.BooleanField(
        verbose_name=_("Standard Option Type"),
        blank=False,
        null=False,
        default=False,
    )

    dhcp_server = models.ForeignKey(
        verbose_name=_("DHCP Server"),
        to="DHCPServer",
        on_delete=models.CASCADE,
        related_name="option_definitions",
        blank=True,
        null=True,
    )
    client_class = models.ForeignKey(
        verbose_name=_("Client Class"),
        to="ClientClass",
        on_delete=models.CASCADE,
        related_name="option_definitions",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.dhcp_server:
            return f"{self.space} {self.name} ({self.code}) [{self.dhcp_server.name}]"

        if self.client_class:
            return f"{self.space} {self.name} ({self.code}) [{self.client_class.name}]"

        return f"{self.space} {self.name} ({self.code})"

    def get_space_color(self):
        return OptionSpaceChoices.colors.get(self.space)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)


@register_search
class OptionDefinitionIndex(SearchIndex):
    model = OptionDefinition

    fields = (("name", 100),)
