from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import Case, F, Q, When
from django.utils.translation import gettext_lazy as _

from netbox.models import NetBoxModel, PrimaryModel
from netbox.search import SearchIndex, register_search
from netbox_dhcp.choices import (
    DHCPServerIDTypeChoices,
    DHCPServerStatusChoices,
    HostReservationIdentifierChoices,
)
from netbox_dhcp.fields import ChoiceArrayField
from utilities.querysets import RestrictedQuerySet

from .mixins import (
    BOOTPModelMixin,
    DDNSUpdateModelMixin,
    LeaseModelMixin,
    LifetimeModelMixin,
    NetBoxDHCPModelMixin,
)
from .option import Option

__all__ = (
    "DHCPServerInterface",
    "DHCPServer",
    "DHCPServerIndex",
)


class DHCPServerInterfaceManager(models.Manager.from_queryset(RestrictedQuerySet)):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                name=models.ExpressionWrapper(
                    Case(
                        When(
                            device_interface__isnull=False,
                            then=F("device_interface__name"),
                        ),
                        When(
                            virtual_machine_interface__isnull=False,
                            then=F("virtual_machine_interface__name"),
                        ),
                    ),
                    output_field=models.CharField(),
                ),
                parent_name=models.ExpressionWrapper(
                    Case(
                        When(
                            device_interface__isnull=False,
                            then=F("device_interface__device__name"),
                        ),
                        When(
                            virtual_machine_interface__isnull=False,
                            then=F("virtual_machine_interface__virtual_machine__name"),
                        ),
                    ),
                    output_field=models.CharField(),
                ),
            )
            .order_by("dhcp_server", "name")
        )


class DHCPServerInterface(NetBoxModel):
    class Meta:
        verbose_name = _("DHCP Server Interface")
        verbose_name_plural = _("DHCP Server Interfaces")

        constraints = [
            models.CheckConstraint(
                condition=Q(
                    Q(
                        device_interface__isnull=False,
                        virtual_machine_interface__isnull=True,
                    )
                    | Q(
                        device_interface__isnull=True,
                        virtual_machine_interface__isnull=False,
                    )
                ),
                name="dhcp_server_interface_device_vm",
                violation_error_message=_(
                    "Interface must refer to either a device or vm interface"
                ),
            ),
        ]

    objects = DHCPServerInterfaceManager()

    dhcp_server = models.ForeignKey(
        to="DHCPServer",
        related_name="+",
        blank=True,
        on_delete=models.CASCADE,
    )
    device_interface = models.ForeignKey(
        to="dcim.Interface",
        related_name="netbox_dhcp_dhcp_server_interfaces",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    virtual_machine_interface = models.ForeignKey(
        to="virtualization.VMInterface",
        related_name="netbox_dhcp_dhcp_server_interfaces",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if hasattr(self, "name"):
            return self.name

        return super().__str__()


class DHCPServer(
    NetBoxDHCPModelMixin,
    BOOTPModelMixin,
    LeaseModelMixin,
    DDNSUpdateModelMixin,
    LifetimeModelMixin,
    PrimaryModel,
):
    class Meta:
        verbose_name = _("DHCP Server")
        verbose_name_plural = _("DHCP Servers")

        ordering = ("name",)

    clone_fields = (
        "name",
        "description",
        "status",
        "dhcp_cluster",
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=50,
        choices=DHCPServerStatusChoices,
        default=DHCPServerStatusChoices.STATUS_ACTIVE,
        blank=True,
    )

    dhcp_cluster = models.ForeignKey(
        to="DHCPCluster",
        verbose_name=_("DHCP Cluster"),
        on_delete=models.SET_NULL,
        related_name="dhcp_servers",
        blank=True,
        null=True,
    )
    device = models.ForeignKey(
        to="dcim.Device",
        verbose_name=_("Device"),
        on_delete=models.SET_NULL,
        related_name="netbox_dhcp_dhcp_servers",
        blank=True,
        null=True,
    )
    device_interfaces = models.ManyToManyField(
        to="dcim.Interface",
        verbose_name=_("Interfaces"),
        related_name="netbox_dhcp_dhcp_servers",
        blank=True,
    )
    virtual_machine = models.ForeignKey(
        to="virtualization.VirtualMachine",
        verbose_name=_("Virtual Machine"),
        on_delete=models.SET_NULL,
        related_name="netbox_dhcp_dhcp_servers",
        blank=True,
        null=True,
    )
    virtual_machine_interfaces = models.ManyToManyField(
        to="virtualization.VMInterface",
        verbose_name=_("Interfaces"),
        related_name="netbox_dhcp_dhcp_servers",
        blank=True,
    )
    interfaces = models.ManyToManyField(
        to=DHCPServerInterface,
        verbose_name=_("Interfaces"),
        related_name="dhcp_servers",
        blank=True,
    )
    decline_probation_period = models.PositiveIntegerField(
        verbose_name=_("Decline Probation Period"),
        blank=True,
        null=True,
    )
    host_reservation_identifiers = ChoiceArrayField(
        base_field=models.CharField(
            choices=HostReservationIdentifierChoices,
        ),
        verbose_name=_("Host Reservation Identifiers"),
        blank=True,
        null=True,
        default=list,
    )
    echo_client_id = models.BooleanField(
        verbose_name=_("Echo Client ID"),
        null=True,
        blank=True,
    )
    relay_supplied_options = ArrayField(
        verbose_name=_("Relay Supplied Options"),
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(0),
                MaxValueValidator(255),
            ]
        ),
        blank=True,
        default=list,
    )
    server_id = models.CharField(
        verbose_name=_("Server DUID"),
        choices=DHCPServerIDTypeChoices,
        blank=True,
        null=True,
    )
    options = GenericRelation(
        to=Option,
        content_type_field="assigned_object_type",
        object_id_field="assigned_object_id",
    )

    def get_status_color(self):
        return DHCPServerStatusChoices.colors.get(self.status)

    def get_server_id_color(self):
        return DHCPServerIDTypeChoices.colors.get(self.server_id)

    def clean(self):
        super().clean()

        if self.device and self.virtual_machine:
            error_message = (
                _("Specifying both a device and a virtual machine is not supported"),
            )
            raise ValidationError(
                {
                    "device": error_message,
                    "virtual_machine": error_message,
                }
            )


@register_search
class DHCPServerIndex(SearchIndex):
    model = DHCPServer

    fields = (
        ("name", 100),
        ("description", 200),
    )
