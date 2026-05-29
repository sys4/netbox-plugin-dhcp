from django import forms
from django.utils.translation import gettext as _

from ipam.models import Prefix
from netbox_dhcp.choices import (
    AllocatorTypeChoices,
    DDNSConflictResolutionModeChoices,
    DDNSReplaceClientNameChoices,
    PDAllocatorTypeChoices,
)
from netbox_dhcp.models import (
    ClientClass,
    DHCPServer,
    SharedNetwork,
    Subnet,
)
from utilities.forms.fields import (
    CSVChoiceField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
)

__all__ = (
    "BOOTPImportFormMixin",
    "ClientClassImportFormMixin",
    "ClientClassesImportFormMixin",
    "EvaluateClientClassesImportFormMixin",
    "PrefixImportFormMixin",
    "DDNSUpdateImportFormMixin",
    "LifetimeImportFormMixin",
    "LeaseImportFormMixin",
    "SubnetImportFormMixin",
    "DHCPServerImportFormMixin",
    "SharedNetworkImportFormMixin",
    "NetworkImportFormMixin",
)


class BOOTPImportFormMixin(forms.Form):
    FIELDS = [
        "next_server",
        "server_hostname",
        "boot_file_name",
    ]


class ClientClassImportFormMixin(forms.Form):
    FIELDS = [
        "client_class",
    ]

    client_class = CSVModelChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Client class %(value)s not found"),
        },
        label=_("Client Class"),
    )


class ClientClassesImportFormMixin(forms.Form):
    FIELDS = [
        "client_classes",
    ]

    client_classes = CSVModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Client class %(value)s not found"),
        },
        label=_("Client Classes"),
    )


class EvaluateClientClassesImportFormMixin(forms.Form):
    FIELDS = [
        "evaluate_additional_classes",
    ]

    evaluate_additional_classes = CSVModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Client class %(value)s not found"),
        },
        label=_("Evaluate Additional Classes"),
    )


class PrefixImportFormMixin(forms.Form):
    prefix = CSVModelChoiceField(
        queryset=Prefix.objects.all(),
        required=True,
        to_field_name="prefix",
        label=_("Prefix"),
    )


class DDNSUpdateImportFormMixin(forms.Form):
    FIELDS = [
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
        "hostname_char_set",
        "hostname_char_replacement",
    ]

    ddns_replace_client_name = CSVChoiceField(
        choices=DDNSReplaceClientNameChoices,
        required=False,
        label=_("Replace Client Name"),
    )
    ddns_conflict_resolution_mode = CSVChoiceField(
        choices=DDNSConflictResolutionModeChoices,
        required=False,
        label=_("Conflict Resolution Mode"),
    )


class LifetimeImportFormMixin(forms.Form):
    FIELDS = [
        "offer_lifetime",
        "valid_lifetime",
        "min_valid_lifetime",
        "max_valid_lifetime",
        "preferred_lifetime",
        "min_preferred_lifetime",
        "max_preferred_lifetime",
    ]


class LeaseImportFormMixin(forms.Form):
    FIELDS = [
        "renew_timer",
        "rebind_timer",
        "calculate_tee_times",
        "t1_percent",
        "t2_percent",
        "adaptive_lease_time_threshold",
        "match_client_id",
        "reservations_global",
        "reservations_out_of_pool",
        "reservations_in_subnet",
        "cache_threshold",
        "cache_max_age",
        "authoritative",
        "store_extended_info",
        "allocator",
        "pd_allocator",
    ]

    allocator = CSVChoiceField(
        choices=AllocatorTypeChoices,
        required=False,
        label=_("Allocator"),
    )
    pd_allocator = CSVChoiceField(
        choices=PDAllocatorTypeChoices,
        required=False,
        label=_("Prefix Delegation Allocator"),
    )


class SubnetImportFormMixin(forms.Form):
    FIELDS = [
        "subnet",
    ]

    subnet = CSVModelChoiceField(
        queryset=Subnet.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Subnet %(value)s not found"),
        },
        label=_("Subnet"),
    )


class DHCPServerImportFormMixin(forms.Form):
    FIELDS = [
        "dhcp_server",
    ]

    dhcp_server = CSVModelChoiceField(
        queryset=DHCPServer.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("DHCP Server %(value)s not found"),
        },
        label=_("DHCP Server"),
    )


class SharedNetworkImportFormMixin(forms.Form):
    FIELDS = [
        "shared_network",
    ]

    shared_network = CSVModelChoiceField(
        queryset=SharedNetwork.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Shared Network %(value)s not found"),
        },
        label=_("Shared Network"),
    )


class NetworkImportFormMixin(forms.Form):
    FIELDS = [
        "relay",
        "interface_id",
        "rapid_commit",
    ]
