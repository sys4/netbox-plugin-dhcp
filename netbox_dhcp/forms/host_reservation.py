from django import forms
from django.utils.translation import gettext_lazy as _

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
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms import get_field_value

from ipam.models import IPAddress, Prefix
from ipam.choices import IPAddressFamilyChoices
from dcim.models import MACAddress

from netbox_dhcp.models import HostReservation

from .mixins import (
    DHCPServerFormMixin,
    DHCPServerFilterFormMixin,
    DHCPServerImportFormMixin,
    DHCPServerBulkEditFormMixin,
    SubnetFormMixin,
    SubnetFilterFormMixin,
    SubnetImportFormMixin,
    SubnetBulkEditFormMixin,
    ClientClassFormMixin,
    ClientClassFilterFormMixin,
    ClientClassImportFormMixin,
    ClientClassBulkEditFormMixin,
    BOOTPFormMixin,
    BOOTPFilterFormMixin,
    BOOTPImportFormMixin,
    BOOTPBulkEditFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    NetBoxDHCPFilterFormMixin,
)


__all__ = (
    "HostReservationForm",
    "HostReservationFilterForm",
    "HostReservationImportForm",
    "HostReservationBulkEditForm",
)


class HostReservationForm(
    DHCPServerFormMixin,
    SubnetFormMixin,
    ClientClassFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = HostReservation

        fields = (
            "name",
            "description",
            *DHCPServerFormMixin.FIELDS,
            *SubnetFormMixin.FIELDS,
            "duid",
            "hw_address",
            "circuit_id",
            "client_id",
            "flex_id",
            "hostname",
            "ipv4_address",
            "ipv6_addresses",
            "ipv6_prefixes",
            "excluded_ipv6_prefixes",
            *ClientClassFormMixin.FIELDS,
            *BOOTPFormMixin.FIELDS,
            "tags",
        )

    fieldsets = (
        FieldSet(
            "name",
            "description",
            TabbedGroups(
                FieldSet(
                    *DHCPServerFormMixin.FIELDS,
                    name=_("DHCP Server"),
                ),
                FieldSet(
                    *SubnetFormMixin.FIELDS,
                    name=_("Subnet"),
                ),
            ),
            name=_("Host Reservation"),
        ),
        FieldSet(
            "duid",
            "hw_address",
            "circuit_id",
            "client_id",
            "flex_id",
            name=_("Selection"),
        ),
        FieldSet(
            "ipv4_address",
            "ipv6_addresses",
            "ipv6_prefixes",
            "excluded_ipv6_prefixes",
            "hostname",
            name=_("Assignment"),
        ),
        ClientClassFormMixin.FIELDSET,
        BOOTPFormMixin.FIELDSET,
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subnet"].widget.attrs.update(
            {
                "hx-get": ".",
                "hx-include": "#form_fields",
                "hx-target": "#form_fields",
            }
        )

        if subnet_id := get_field_value(self, "subnet"):
            prefix = (
                Prefix.objects.filter(netbox_dhcp_subnets=subnet_id)
                .values_list("prefix", flat=True)
                .first()
            )
            if prefix.version == IPAddressFamilyChoices.FAMILY_4:
                del self.fields["ipv6_addresses"]
                del self.fields["ipv6_prefixes"]
                del self.fields["excluded_ipv6_prefixes"]
                self.fields["ipv4_address"].widget.add_query_param(
                    "parent", str(prefix)
                )
            else:
                del self.fields["ipv4_address"]
                self.fields["ipv6_addresses"].widget.add_query_param(
                    "parent", str(prefix)
                )
                self.fields["ipv6_prefixes"].widget.add_query_param(
                    "within_include", str(prefix)
                )
                self.fields["excluded_ipv6_prefixes"].widget.add_query_param(
                    "within", str(prefix)
                )

    def clean(self):
        super().clean()

        if subnet := self.cleaned_data.get("subnet"):
            if subnet.family == IPAddressFamilyChoices.FAMILY_4:
                self.cleaned_data["ipv6_addresses"] = IPAddress.objects.none()
                self.cleaned_data["ipv6_prefixes"] = Prefix.objects.none()
                self.cleaned_data["excluded_ipv6_prefixes"] = Prefix.objects.none()
            else:
                self.cleaned_data["ipv4_address"] = None

    hw_address = DynamicModelChoiceField(
        queryset=MACAddress.objects.all(),
        required=False,
        quick_add=True,
        selector=True,
        label=_("Hardware Address"),
    )

    ipv4_address = DynamicModelChoiceField(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_4
        ),
        query_params={"family": IPAddressFamilyChoices.FAMILY_4},
        required=False,
        selector=True,
        label=_("IPv4 Address"),
    )
    ipv6_addresses = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_6
        ),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        required=False,
        selector=True,
        label=_("IPv6 Addresses"),
    )
    ipv6_prefixes = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        context={
            "depth": None,
        },
        required=False,
        selector=True,
        label=_("IPv6 Prefixes"),
    )
    excluded_ipv6_prefixes = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        context={
            "depth": None,
        },
        required=False,
        selector=True,
        label=_("Excluded IPv6 Prefixes"),
    )


class HostReservationFilterForm(
    DHCPServerFilterFormMixin,
    SubnetFilterFormMixin,
    NetBoxDHCPFilterFormMixin,
    ClientClassFilterFormMixin,
    BOOTPFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = HostReservation

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
            *DHCPServerFilterFormMixin.FIELDS,
            *SubnetFilterFormMixin.FIELDS,
            name=_("Host Reservation"),
        ),
        FieldSet(
            "duid",
            "hw_address_id",
            "circuit_id",
            "client_id",
            "flex_id",
            "client_class_id",
            name=_("Selection"),
        ),
        FieldSet(
            "ipv4_address_id",
            "ipv6_address_id",
            "ipv6_prefix_id",
            "excluded_ipv6_prefix_id",
            "hostname",
            name=_("Assignment"),
        ),
        ClientClassFilterFormMixin.FIELDSET,
        BOOTPFilterFormMixin.FIELDSET,
    )

    duid = forms.CharField(
        required=False,
        label=_("DUID"),
    )
    hw_address_id = DynamicModelMultipleChoiceField(
        queryset=MACAddress.objects.all(),
        required=False,
        selector=True,
        label=_("Hardware Address"),
    )
    circuit_id = forms.CharField(
        required=False,
        label=_("Circuit ID"),
    )
    client_id = forms.CharField(
        required=False,
        label=_("Client ID"),
    )
    flex_id = forms.CharField(
        required=False,
        label=_("Flex ID"),
    )

    hostname = forms.CharField(
        required=False,
        label=_("Host Name"),
    )
    ipv4_address_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_4
        ),
        query_params={"family": IPAddressFamilyChoices.FAMILY_4},
        required=False,
        selector=True,
        label=_("IPv4 Address"),
    )
    ipv6_address_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_6
        ),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        required=False,
        selector=True,
        label=_("IPv6 Address"),
    )
    ipv6_prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        required=False,
        selector=True,
        label=_("IPv6 Prefix"),
    )
    excluded_ipv6_prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        required=False,
        selector=True,
        label=_("Excluded IPv6 Prefix"),
    )

    tag = TagFilterField(HostReservation)


class HostReservationImportForm(
    DHCPServerImportFormMixin,
    SubnetImportFormMixin,
    ClientClassImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = HostReservation

        fields = (
            "name",
            "description",
            *DHCPServerImportFormMixin.FIELDS,
            *SubnetImportFormMixin.FIELDS,
            "duid",
            "hw_address",
            "circuit_id",
            "client_id",
            "flex_id",
            "hostname",
            "ipv4_address",
            "ipv6_addresses",
            "ipv6_prefixes",
            "excluded_ipv6_prefixes",
            *ClientClassImportFormMixin.FIELDS,
            *BOOTPImportFormMixin.FIELDS,
            "comments",
            "tags",
        )

    hw_address = CSVModelChoiceField(
        queryset=MACAddress.objects.all(),
        required=False,
        to_field_name="mac_address",
        help_text=_("Hardware address in xx:xx:xx:xx:xx:xx format"),
        error_messages={
            "invalid_choice": _("Hardware address %(value)s not found"),
        },
        label=_("Hardware Address"),
    )

    ipv4_address = CSVModelChoiceField(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_4
        ),
        required=False,
        to_field_name="address",
        error_messages={
            "invalid_choice": _("IPv4 address %(value)s not found"),
        },
        label=_("IPv4 Address"),
    )
    ipv6_addresses = CSVModelMultipleChoiceField(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_6
        ),
        required=False,
        to_field_name="address",
        error_messages={
            "invalid_choice": _("IPv6 address %(value)s not found"),
        },
        label=_("IPv6 Addresses"),
    )
    ipv6_prefixes = CSVModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        required=False,
        to_field_name="prefix",
        error_messages={
            "invalid_choice": _("IPv6 prefix %(value)s not found"),
        },
        label=_("IPv6 Prefixes"),
    )
    excluded_ipv6_prefixes = CSVModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        required=False,
        to_field_name="prefix",
        error_messages={
            "invalid_choice": _("IPv6 prefix %(value)s not found"),
        },
        label=_("Excluded IPv6 Prefixes"),
    )


class HostReservationBulkEditForm(
    DHCPServerBulkEditFormMixin,
    SubnetBulkEditFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    BOOTPBulkEditFormMixin,
    ClientClassBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = HostReservation

    fieldsets = (
        FieldSet(
            "description",
            TabbedGroups(
                FieldSet(
                    *DHCPServerBulkEditFormMixin.FIELDS,
                    name=_("DHCP Server"),
                ),
                FieldSet(
                    *SubnetBulkEditFormMixin.FIELDS,
                    name=_("Subnet"),
                ),
            ),
            name=_("Host Reservation"),
        ),
        FieldSet(
            "circuit_id",
            "flex_id",
            name=_("Selection"),
        ),
        FieldSet(
            "ipv6_prefixes",
            "excluded_ipv6_prefixes",
            name=_("Assignment"),
        ),
        ClientClassBulkEditFormMixin.FIELDSET,
        BOOTPBulkEditFormMixin.FIELDSET,
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    nullable_fields = (
        "description",
        *DHCPServerBulkEditFormMixin.NULLABLE_FIELDS,
        *SubnetBulkEditFormMixin.NULLABLE_FIELDS,
        "flex_id",
        "ipv6_prefixes",
        "excluded_ipv6_prefixes",
        *BOOTPBulkEditFormMixin.NULLABLE_FIELDS,
        *ClientClassBulkEditFormMixin.NULLABLE_FIELDS,
    )

    circuit_id = forms.CharField(
        required=False,
        label=_("Circuit ID"),
    )
    flex_id = forms.CharField(
        required=False,
        label=_("Flex ID"),
    )

    ipv6_prefixes = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        required=False,
        selector=True,
        label=_("IPv6 Prefixes"),
    )
    excluded_ipv6_prefixes = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={"family": IPAddressFamilyChoices.FAMILY_6},
        required=False,
        selector=True,
        label=_("Excluded IPv6 Prefixes"),
    )
