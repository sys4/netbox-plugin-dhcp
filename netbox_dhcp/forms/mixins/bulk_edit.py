from django import forms
from django.utils.translation import gettext as _

from utilities.forms import add_blank_choice
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.widgets import BulkEditNullBooleanSelect
from utilities.forms.rendering import FieldSet
from ipam.models import Prefix

from netbox_dhcp.models import (
    ClientClass,
    Subnet,
    DHCPServer,
    SharedNetwork,
)
from netbox_dhcp.choices import (
    DDNSReplaceClientNameChoices,
    DDNSConflictResolutionModeChoices,
    AllocatorTypeChoices,
    PDAllocatorTypeChoices,
)

__all__ = (
    "NetBoxDHCPBulkEditFormMixin",
    "BOOTPBulkEditFormMixin",
    "ClientClassesBulkEditFormMixin",
    "EvaluateClientClassesBulkEditFormMixin",
    "OfferLifetimeBulkEditFormMixin",
    "LifetimeBulkEditFormMixin",
    "PrefixBulkEditFormMixin",
    "DDNSUpdateBulkEditFormMixin",
    "LeaseBulkEditFormMixin",
    "NetworkBulkEditFormMixin",
    "SubnetBulkEditFormMixin",
    "DHCPServerBulkEditFormMixin",
    "SharedNetworkBulkEditFormMixin",
)


class NetBoxDHCPBulkEditFormMixin(forms.Form):
    description = forms.CharField(
        required=False,
        label=_("Description"),
    )


class BOOTPBulkEditFormMixin(forms.Form):
    NULLABLE_FIELDS = [
        "next_server",
        "server_hostname",
        "boot_file_name",
    ]
    FIELDSET = FieldSet(
        "next_server",
        "server_hostname",
        "boot_file_name",
        name=_("BOOTP"),
    )

    next_server = forms.CharField(
        required=False,
        label=_("Next Server"),
    )
    server_hostname = forms.CharField(
        required=False,
        label=_("Server Hostname"),
    )
    boot_file_name = forms.CharField(
        required=False,
        label=_("Boot File Name"),
    )


class ClientClassesBulkEditFormMixin(forms.Form):
    FIELDS = [
        "client_classes",
    ]
    FIELDSET = FieldSet(
        "client_classes",
        name=_("Client Classes"),
    )
    NULLABLE_FIELDS = [
        "client_classes",
    ]

    client_classes = DynamicModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        quick_add=True,
        label=_("Client Classes"),
    )


class EvaluateClientClassesBulkEditFormMixin(forms.Form):
    FIELDS = [
        "evaluate_additional_classes",
    ]
    FIELDSET = FieldSet(
        "evaluate_additional_classes",
        name=_("Client Classes"),
    )
    NULLABLE_FIELDS = [
        "evaluate_additional_classes",
    ]

    evaluate_additional_classes = DynamicModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        quick_add=True,
        label=_("Evaluate Additional Classes"),
    )


class OfferLifetimeBulkEditFormMixin(forms.Form):
    offer_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Offer Lifetime"),
    )


class LifetimeBulkEditFormMixin(OfferLifetimeBulkEditFormMixin):
    FIELDSET = FieldSet(
        "offer_lifetime",
        "valid_lifetime",
        "min_valid_lifetime",
        "max_valid_lifetime",
        "preferred_lifetime",
        "min_preferred_lifetime",
        "max_preferred_lifetime",
        name=_("Lifetimes"),
    )
    NULLABLE_FIELDS = [
        "offer_lifetime",
        "valid_lifetime",
        "min_valid_lifetime",
        "max_valid_lifetime",
        "preferred_lifetime",
        "min_preferred_lifetime",
        "max_preferred_lifetime",
    ]

    valid_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Valid Lifetime"),
    )
    min_valid_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Minimum Valid Lifetime"),
    )
    max_valid_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Maximum Valid Lifetime"),
    )
    preferred_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Preferred Lifetime"),
    )
    min_preferred_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Minimum Preferred Lifetime"),
    )
    max_preferred_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Maximum Preferred Lifetime"),
    )


class PrefixBulkEditFormMixin(forms.Form):
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        selector=True,
        context={"depth": None},
        label=_("Prefix"),
    )


class DDNSUpdateBulkEditFormMixin(forms.Form):
    FIELDSET = FieldSet(
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
        name=_("Dynamic DNS Update"),
    )
    NULLABLE_FIELDS = [
        "ddns_generated_prefix",
        "ddns_qualifying_suffix",
        "ddns_ttl_percent",
        "ddns_ttl",
        "ddns_ttl_min",
        "ddns_ttl_max",
        "hostname_char_set",
        "hostname_char_replacement",
    ]

    ddns_send_updates = forms.NullBooleanField(
        label=_("Send DDNS updates"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    ddns_override_no_update = forms.NullBooleanField(
        label=_("Override client 'no update' flag"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    ddns_override_client_update = forms.NullBooleanField(
        label=_("Override client delegation flags"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    ddns_replace_client_name = forms.ChoiceField(
        choices=add_blank_choice(DDNSReplaceClientNameChoices),
        required=False,
        label=_("Replace Client Name"),
    )
    ddns_generated_prefix = forms.CharField(
        required=False,
        label=_("Generated Prefix"),
    )
    ddns_qualifying_suffix = forms.CharField(
        required=False,
        label=_("Qualifying Suffix"),
    )
    ddns_update_on_renew = forms.NullBooleanField(
        label=_("Update DDNS on renew"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    ddns_qualifying_suffix = forms.CharField(
        label=_("Replace client name"),
        required=False,
    )
    ddns_conflict_resolution_mode = forms.ChoiceField(
        label=_("Conflict Resolution Mode"),
        choices=add_blank_choice(DDNSConflictResolutionModeChoices),
        required=False,
    )
    ddns_ttl_percent = forms.DecimalField(
        label=_("TTL Percent"),
        help_text=_("A decimal value between 0.00 and 1.00"),
        min_value=0.0,
        max_value=1.0,
        max_digits=4,
        decimal_places=3,
        required=False,
    )
    ddns_ttl = forms.IntegerField(
        label=_("TTL"),
        required=False,
    )
    ddns_ttl_min = forms.IntegerField(
        label=_("Minimum TTL"),
        required=False,
    )
    ddns_ttl_max = forms.IntegerField(
        label=_("Maximum TTL"),
        required=False,
    )
    hostname_char_set = forms.CharField(
        label=_("Allowed Characters in Host Names"),
        required=False,
    )
    hostname_char_replacement = forms.CharField(
        label=_("Replacement Character for Invalid Host Names"),
        required=False,
    )


class LeaseBulkEditFormMixin(forms.Form):
    FIELDSET = FieldSet(
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
        name=_("Lease"),
    )
    NULLABLE_FIELDS = [
        "renew_timer",
        "rebind_timer",
        "t1_percent",
        "t2_percent",
        "adaptive_lease_time_threshold",
        "cache_threshold",
        "cache_max_age",
        "relay",
        "interface_id",
    ]

    renew_timer = forms.IntegerField(
        label=_("Renew Timer"),
        required=False,
    )
    rebind_timer = forms.IntegerField(
        label=_("Rebind Timer"),
        required=False,
    )
    match_client_id = forms.NullBooleanField(
        label=_("Match Client ID"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    authoritative = forms.NullBooleanField(
        label=_("Authoritative"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    reservations_global = forms.NullBooleanField(
        label=_("Global reservations"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    reservations_out_of_pool = forms.NullBooleanField(
        label=_("Out-of-pool reservations"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    reservations_in_subnet = forms.NullBooleanField(
        label=_("In-subnet reservations"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    calculate_tee_times = forms.NullBooleanField(
        label=_("Calculate T times"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    t1_percent = forms.DecimalField(
        label=_("T1 Percent"),
        help_text=_("A decimal value between 0.000 and 1.000"),
        max_digits=4,
        decimal_places=3,
        min_value=0.0,
        max_value=1.0,
        required=False,
    )
    t2_percent = forms.DecimalField(
        label=_("T2 Percent"),
        max_digits=4,
        decimal_places=3,
        min_value=0.0,
        max_value=1.0,
        required=False,
    )
    cache_threshold = forms.DecimalField(
        label=_("Cache Threshold"),
        help_text=_("A decimal value between 0.00 and 1.00"),
        max_digits=3,
        decimal_places=2,
        min_value=0.0,
        max_value=1.0,
        required=False,
    )
    cache_max_age = forms.IntegerField(
        label=_("Maximum Cache Age"),
        required=False,
    )
    adaptive_lease_time_threshold = forms.DecimalField(
        label=_("Adaptive Lease Time Threshold"),
        help_text=_("A decimal value between 0.00 and 1.00"),
        max_digits=3,
        decimal_places=2,
        min_value=0.0,
        max_value=1.0,
        required=False,
    )
    store_extended_info = forms.NullBooleanField(
        label=_("Store Extended Info"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )
    allocator = forms.ChoiceField(
        label=_("Allocator"),
        choices=add_blank_choice(AllocatorTypeChoices),
        required=False,
    )
    pd_allocator = forms.ChoiceField(
        label=_("Prefix Delegation Allocator"),
        choices=add_blank_choice(PDAllocatorTypeChoices),
        required=False,
    )


class NetworkBulkEditFormMixin(forms.Form):
    FIELDSET = FieldSet(
        "relay",
        "interface_id",
        "rapid_commit",
        name=_("Network"),
    )
    NULLABLE_FIELDS = [
        "relay",
        "interface_id",
        "rapid_commit",
    ]

    relay = forms.CharField(
        label=_("Relay IP Addresses"),
        required=False,
    )
    interface_id = forms.CharField(
        label=_("Interface ID"),
        required=False,
    )
    rapid_commit = forms.NullBooleanField(
        label=_("Rapid Commit"),
        widget=BulkEditNullBooleanSelect(),
        required=False,
    )


class SubnetBulkEditFormMixin(forms.Form):
    FIELDS = [
        "subnet",
    ]
    NULLABLE_FIELDS = [
        "subnet",
    ]

    subnet = DynamicModelChoiceField(
        queryset=Subnet.objects.all(),
        required=False,
        context={
            "description": "prefix_display",
        },
        label=_("Subnet"),
    )


class DHCPServerBulkEditFormMixin(forms.Form):
    FIELDS = [
        "dhcp_server",
    ]
    NULLABLE_FIELDS = [
        "dhcp_server",
    ]

    dhcp_server = DynamicModelChoiceField(
        queryset=DHCPServer.objects.all(),
        required=False,
        label=_("DHCP Server"),
    )


class SharedNetworkBulkEditFormMixin(forms.Form):
    FIELDS = [
        "shared_network",
    ]
    NULLABLE_FIELDS = [
        "shared_network",
    ]

    shared_network = DynamicModelChoiceField(
        queryset=SharedNetwork.objects.all(),
        required=False,
        context={"description": "prefix_display"},
        label=_("Shared Network"),
    )
