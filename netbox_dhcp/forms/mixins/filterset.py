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
from utilities.forms import (
    BOOLEAN_WITH_BLANK_CHOICES,
    add_blank_choice,
)
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet

__all__ = (
    "ClientClassFilterFormMixin",
    "ClientClassesFilterFormMixin",
    "EvaluateClientClassesFilterFormMixin",
    "BOOTPFilterFormMixin",
    "NetBoxDHCPFilterFormMixin",
    "OfferLifetimeFilterFormMixin",
    "LifetimeFilterFormMixin",
    "PrefixFilterFormMixin",
    "DDNSUpdateFilterFormMixin",
    "LeaseFilterFormMixin",
    "NetworkFilterFormMixin",
    "SubnetFilterFormMixin",
    "DHCPServerFilterFormMixin",
    "SharedNetworkFilterFormMixin",
)


class NetBoxDHCPFilterFormMixin(forms.Form):
    name = forms.CharField(
        required=False,
        label=_("Name"),
    )
    description = forms.CharField(
        required=False,
        label=_("Description"),
    )


class BOOTPFilterFormMixin(forms.Form):
    FIELDS = [
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


class OfferLifetimeFilterFormMixin(forms.Form):
    offer_lifetime = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Offer Lifetime"),
    )


class LifetimeFilterFormMixin(OfferLifetimeFilterFormMixin):
    FIELDS = [
        "offer_lifetime",
        "valid_lifetime",
        "min_valid_lifetime",
        "max_valid_lifetime",
        "preferred_lifetime",
        "min_preferred_lifetime",
        "max_preferred_lifetime",
    ]
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


class ClientClassFilterFormMixin(forms.Form):
    FIELDS = [
        "client_class_id",
    ]
    FIELDSET = FieldSet(
        "client_class_id",
        name=_("Client Class"),
    )

    client_class_id = DynamicModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        label=_("Client Class"),
    )


class ClientClassesFilterFormMixin(forms.Form):
    FIELDS = [
        "client_class_id",
    ]
    FIELDSET = FieldSet(
        "client_class_id",
        name=_("Client Classes"),
    )

    client_class_id = DynamicModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        label=_("Client Classes"),
    )


class EvaluateClientClassesFilterFormMixin(forms.Form):
    FIELDS = [
        "evaluate_additional_class_id",
    ]
    FIELDSET = FieldSet(
        "evaluate_additional_class_id",
        name=_("Client Classes"),
    )

    evaluate_additional_class_id = DynamicModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        label=_("Evaluate Additional Classes"),
    )


class PrefixFilterFormMixin(forms.Form):
    prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        selector=True,
        context={
            "depth": None,
        },
        label=_("Prefix"),
    )


class DDNSUpdateFilterFormMixin(forms.Form):
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

    ddns_send_updates = forms.NullBooleanField(
        label=_("Send DDNS updates"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    ddns_send_updates = forms.NullBooleanField(
        label=_("Send DDNS updates"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    ddns_override_no_update = forms.NullBooleanField(
        label=_("Override client 'no update' flag"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    ddns_override_client_update = forms.NullBooleanField(
        label=_("Override client delegation flags"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    ddns_replace_client_name = forms.ChoiceField(
        choices=add_blank_choice(DDNSReplaceClientNameChoices),
        required=False,
        label=_("Replace Client Name"),
    )
    ddns_generated_prefix = forms.CharField(
        label=_("Generated Prefix"),
        required=False,
    )
    ddns_qualifying_suffix = forms.CharField(
        label=_("Qualifying Suffix"),
        required=False,
    )
    ddns_update_on_renew = forms.NullBooleanField(
        label=_("Update DDNS on renew"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    ddns_conflict_resolution_mode = forms.ChoiceField(
        choices=add_blank_choice(DDNSConflictResolutionModeChoices),
        required=False,
        label=_("Conflict Resolution Mode"),
    )
    ddns_ttl_percent = forms.DecimalField(
        label=_("TTL Percent"),
        max_digits=4,
        decimal_places=3,
        min_value=0.0,
        max_value=1.0,
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
        max_length=255,
        required=False,
    )
    hostname_char_replacement = forms.CharField(
        label=_("Replacement Character for Invalid Host Names"),
        max_length=255,
        required=False,
    )


class LeaseFilterFormMixin(forms.Form):
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
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    authoritative = forms.NullBooleanField(
        label=_("Authoritative"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    reservations_global = forms.NullBooleanField(
        label=_("Global reservations"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    reservations_out_of_pool = forms.NullBooleanField(
        label=_("Out-of-pool reservations"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    reservations_in_subnet = forms.NullBooleanField(
        label=_("In-subnet reservations"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    calculate_tee_times = forms.NullBooleanField(
        label=_("Calculate T times"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    t1_percent = forms.DecimalField(
        label=_("T1 Percent"),
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
        max_digits=3,
        decimal_places=2,
        min_value=0.0,
        max_value=1.0,
        required=False,
    )
    store_extended_info = forms.NullBooleanField(
        label=_("Store Extended Info"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
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


class NetworkFilterFormMixin(forms.Form):
    FIELDSET = FieldSet(
        "relay",
        "interface_id",
        "rapid_commit",
        name=_("Network"),
    )

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
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )


class SubnetFilterFormMixin(forms.Form):
    FIELDS = [
        "subnet_id",
    ]

    subnet_id = DynamicModelMultipleChoiceField(
        queryset=Subnet.objects.all(),
        required=False,
        context={
            "description": "prefix_display",
        },
        label=_("Subnet"),
    )


class DHCPServerFilterFormMixin(forms.Form):
    FIELDS = [
        "dhcp_server_id",
    ]

    dhcp_server_id = DynamicModelMultipleChoiceField(
        queryset=DHCPServer.objects.all(),
        required=False,
        label=_("DHCP Server"),
    )


class SharedNetworkFilterFormMixin(forms.Form):
    FIELDS = [
        "shared_network_id",
    ]

    shared_network_id = DynamicModelMultipleChoiceField(
        queryset=SharedNetwork.objects.all(),
        required=False,
        context={
            "description": "prefix_display",
        },
        label=_("Shared Network"),
    )
