from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.forms import SimpleArrayField

from netbox.forms import (
    PrimaryModelForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelBulkEditForm,
)
from utilities.forms.fields import (
    TagFilterField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    CSVChoiceField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms import (
    add_blank_choice,
    BOOLEAN_WITH_BLANK_CHOICES,
)

from dcim.models import Device, Interface
from virtualization.models import VirtualMachine, VMInterface

from netbox_dhcp.models import DHCPServer, DHCPCluster
from netbox_dhcp.choices import (
    DHCPServerStatusChoices,
    DHCPServerIDTypeChoices,
    HostReservationIdentifierChoices,
)

from .mixins import (
    NetBoxDHCPFilterFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    ClientClassFormMixin,
    ClientClassFilterFormMixin,
    ClientClassImportFormMixin,
    ClientClassBulkEditFormMixin,
    BOOTPFormMixin,
    BOOTPFilterFormMixin,
    BOOTPImportFormMixin,
    BOOTPBulkEditFormMixin,
    LifetimeFormMixin,
    LifetimeFilterFormMixin,
    LifetimeImportFormMixin,
    LifetimeBulkEditFormMixin,
    LeaseFormMixin,
    LeaseImportFormMixin,
    LeaseFilterFormMixin,
    LeaseBulkEditFormMixin,
    DDNSUpdateFormMixin,
    DDNSUpdateFilterFormMixin,
    DDNSUpdateImportFormMixin,
    DDNSUpdateBulkEditFormMixin,
)

__all__ = (
    "DHCPServerForm",
    "DHCPServerFilterForm",
    "DHCPServerImportForm",
    "DHCPServerBulkEditForm",
)


class DHCPServerForm(
    BOOTPFormMixin,
    LifetimeFormMixin,
    LeaseFormMixin,
    DDNSUpdateFormMixin,
    ClientClassFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = DHCPServer

        fields = (
            "name",
            "description",
            "status",
            "dhcp_cluster",
            "device",
            "device_interfaces",
            "virtual_machine",
            "virtual_machine_interfaces",
            "server_id",
            "host_reservation_identifiers",
            "echo_client_id",
            "relay_supplied_options",
            "decline_probation_period",
            *BOOTPFormMixin.FIELDS,
            *LifetimeFormMixin.FIELDS,
            *LeaseFormMixin.FIELDS,
            *DDNSUpdateFormMixin.FIELDS,
            *ClientClassFormMixin.FIELDS,
            "tags",
        )

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "status",
            "dhcp_cluster",
            TabbedGroups(
                FieldSet(
                    "device",
                    "device_interfaces",
                    name=_("Physical"),
                ),
                FieldSet(
                    "virtual_machine",
                    "virtual_machine_interfaces",
                    name=_("Virtual"),
                ),
            ),
            name=_("DHCP Server"),
        ),
        FieldSet(
            "server_id",
            "host_reservation_identifiers",
            "echo_client_id",
            "relay_supplied_options",
            "decline_probation_period",
            name=_("Configuration"),
        ),
        BOOTPFormMixin.FIELDSET,
        LifetimeFormMixin.FIELDSET,
        LeaseFormMixin.FIELDSET,
        DDNSUpdateFormMixin.FIELDSET,
        ClientClassFormMixin.FIELDSET,
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_ddns_fields()
        self.init_lease_fields()

    status = forms.ChoiceField(
        choices=DHCPServerStatusChoices,
        required=False,
        label=_("Status"),
    )
    dhcp_cluster = DynamicModelChoiceField(
        queryset=DHCPCluster.objects.all(),
        required=False,
        quick_add=True,
        label=_("DHCP Cluster"),
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_("Device"),
        selector=True,
    )
    device_interfaces = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        query_params={
            "device_id": "$device",
        },
        required=False,
        label=_("Interfaces"),
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label=_("Virtual Machine"),
        selector=True,
    )
    virtual_machine_interfaces = DynamicModelMultipleChoiceField(
        queryset=VMInterface.objects.all(),
        query_params={
            "virtual_machine_id": "$virtual_machine",
        },
        required=False,
        label=_("Interfaces"),
    )
    echo_client_id = forms.NullBooleanField(
        label=_("Echo Client ID"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        if self.cleaned_data["virtual_machine"] and self.cleaned_data["device"]:
            error_text = _(
                "Cannot assign a device and a virtual machine to a DHCP server."
            )
            raise forms.ValidationError(
                {
                    "device": error_text,
                    "virtual_machine": error_text,
                }
            )

        if self.cleaned_data["device"]:
            self.cleaned_data["virtual_machine_interfaces"] = VMInterface.objects.none()

        if self.cleaned_data["virtual_machine"]:
            self.cleaned_data["device_interfaces"] = Interface.objects.none()


class DHCPServerFilterForm(
    BOOTPFilterFormMixin,
    LifetimeFilterFormMixin,
    LeaseFilterFormMixin,
    DDNSUpdateFilterFormMixin,
    NetBoxDHCPFilterFormMixin,
    ClientClassFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = DHCPServer

    fieldsets = (
        FieldSet(
            "q",
            "filter_id",
            "tag",
        ),
        FieldSet(
            "owner_group_id",
            "owner_id",
            name=_("Ownership"),
        ),
        FieldSet(
            "name",
            "description",
            "status",
            "dhcp_cluster",
            name=_("DHCP Server"),
        ),
        FieldSet(
            "server_id",
            "host_reservation_identifiers",
            "echo_client_id",
            "relay_supplied_options",
            "decline_probation_period",
            name=_("Configuration"),
        ),
        BOOTPFilterFormMixin.FIELDSET,
        LifetimeFilterFormMixin.FIELDSET,
        LeaseFilterFormMixin.FIELDSET,
        DDNSUpdateFilterFormMixin.FIELDSET,
        ClientClassFilterFormMixin.FIELDSET,
    )

    status = forms.MultipleChoiceField(
        choices=DHCPServerStatusChoices,
        required=False,
        label=_("Status"),
    )
    dhcp_cluster_id = DynamicModelMultipleChoiceField(
        queryset=DHCPCluster.objects.all(),
        required=False,
        label=_("DHCP Cluster"),
    )

    server_id = forms.MultipleChoiceField(
        choices=DHCPServerIDTypeChoices,
        required=False,
        label=_("Server DUID"),
    )
    host_reservation_identifiers = forms.MultipleChoiceField(
        choices=HostReservationIdentifierChoices,
        required=False,
        label=_("Host Reservation Identifier"),
    )

    tag = TagFilterField(DHCPServer)


class DHCPServerImportForm(
    BOOTPImportFormMixin,
    LifetimeImportFormMixin,
    LeaseImportFormMixin,
    DDNSUpdateImportFormMixin,
    ClientClassImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = DHCPServer

        fields = (
            "name",
            "description",
            "status",
            "dhcp_cluster",
            "device",
            "device_interfaces",
            "virtual_machine",
            "virtual_machine_interfaces",
            "server_id",
            "host_reservation_identifiers",
            "echo_client_id",
            "relay_supplied_options",
            "decline_probation_period",
            *BOOTPImportFormMixin.FIELDS,
            *LifetimeImportFormMixin.FIELDS,
            *LeaseImportFormMixin.FIELDS,
            *DDNSUpdateImportFormMixin.FIELDS,
            *ClientClassImportFormMixin.FIELDS,
            "comments",
            "tags",
        )

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        if not data:
            return

        device = data.get("device")
        virtual_machine = data.get("virtual_machine")

        if device:
            queryset = self.fields["device_interfaces"].queryset.filter(
                device__name=device
            )
            self.fields["device_interfaces"].queryset = queryset

        if virtual_machine:
            queryset = self.fields["virtual_machine_interfaces"].queryset.filter(
                virtual_machine__name=virtual_machine
            )
            self.fields["virtual_machine_interfaces"].queryset = queryset

    status = CSVChoiceField(
        choices=DHCPServerStatusChoices,
        required=False,
        label=_("Status"),
    )
    dhcp_cluster = CSVModelChoiceField(
        queryset=DHCPCluster.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("DHCP cluster %(value)s not found"),
        },
        label=_("DHCP Cluster"),
    )

    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Device %(value)s not found"),
        },
        label=_("Device"),
    )
    device_interfaces = CSVModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Interface %(value)s not found"),
        },
        label=_("Device Interfaces"),
    )
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Virtual machine %(value)s not found"),
        },
        label=_("Virtual Machine"),
    )
    virtual_machine_interfaces = CSVModelMultipleChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Interface %(value)s not found"),
        },
        label=_("Virtual Machine Interfaces"),
    )


class DHCPServerBulkEditForm(
    BOOTPBulkEditFormMixin,
    LifetimeBulkEditFormMixin,
    LeaseBulkEditFormMixin,
    DDNSUpdateBulkEditFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    ClientClassBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = DHCPServer

    fieldsets = (
        FieldSet(
            "description",
            "status",
            "dhcp_cluster",
            name=_("DHCP Server"),
        ),
        FieldSet(
            "server_id",
            "host_reservation_identifiers",
            "echo_client_id",
            "relay_supplied_options",
            "decline_probation_period",
            name=_("Configuration"),
        ),
        BOOTPBulkEditFormMixin.FIELDSET,
        LifetimeBulkEditFormMixin.FIELDSET,
        LeaseBulkEditFormMixin.FIELDSET,
        DDNSUpdateBulkEditFormMixin.FIELDSET,
        ClientClassBulkEditFormMixin.FIELDSET,
    )

    nullable_fields = (
        "description",
        "dhcp_cluster",
        "server_id",
        "host_reservation_identifiers",
        "echo_client_id",
        "relay_supplied_options",
        "decline_probation_period",
        *BOOTPBulkEditFormMixin.NULLABLE_FIELDS,
        *LifetimeBulkEditFormMixin.NULLABLE_FIELDS,
        *LeaseBulkEditFormMixin.NULLABLE_FIELDS,
        *DDNSUpdateBulkEditFormMixin.NULLABLE_FIELDS,
        *ClientClassBulkEditFormMixin.NULLABLE_FIELDS,
    )

    status = forms.ChoiceField(
        choices=add_blank_choice(DHCPServerStatusChoices),
        required=False,
        label=_("Status"),
    )
    dhcp_cluster = DynamicModelChoiceField(
        queryset=DHCPCluster.objects.all(),
        required=False,
        label=_("DHCP Cluster"),
    )

    server_id = forms.ChoiceField(
        choices=DHCPServerIDTypeChoices,
        required=False,
        label=_("Server DUID"),
    )
    host_reservation_identifiers = forms.MultipleChoiceField(
        choices=HostReservationIdentifierChoices,
        required=False,
        label=_("Host Reservation Identifier"),
    )
    echo_client_id = forms.NullBooleanField(
        label=_("Echo Client ID"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    relay_supplied_options = SimpleArrayField(
        label=_("Relay Supplied Options"),
        base_field=forms.IntegerField(
            min_value=1,
            max_value=255,
        ),
        required=False,
    )
