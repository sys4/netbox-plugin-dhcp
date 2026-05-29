from django import forms
from django.utils.translation import gettext as _

from ipam.choices import IPAddressFamilyChoices
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
    DHCPServerInterface,
    SharedNetwork,
    Subnet,
)
from utilities.forms import (
    BOOLEAN_WITH_BLANK_CHOICES,
    add_blank_choice,
    get_field_value,
)
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet

__all__ = (
    "BOOTPFormMixin",
    "ClientClassFormMixin",
    "ClientClassesFormMixin",
    "EvaluateClientClassesFormMixin",
    "PrefixFormMixin",
    "DDNSUpdateFormMixin",
    "LeaseFormMixin",
    "LifetimeFormMixin",
    "SubnetFormMixin",
    "DHCPServerFormMixin",
    "SharedNetworkFormMixin",
    "NetworkFormMixin",
)

DYNAMIC_ATTRIBUTES = {
    "hx-get": ".",
    "hx-include": "#form_fields",
    "hx-target": "#form_fields",
}


class BOOTPFormMixin:
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


class ClientClassFormMixin(forms.Form):
    FIELDS = [
        "client_class",
    ]
    FIELDSET = FieldSet(
        "client_class",
        name=_("Client Class"),
    )

    client_class = DynamicModelChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        quick_add=True,
        label=_("Client Class"),
    )


class ClientClassesFormMixin(forms.Form):
    FIELDS = [
        "client_classes",
    ]
    FIELDSET = FieldSet(
        "client_classes",
        name=_("Client Classes"),
    )

    client_classes = DynamicModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        quick_add=True,
        label=_("Client Classes"),
    )


class EvaluateClientClassesFormMixin(forms.Form):
    FIELDS = [
        "evaluate_additional_classes",
    ]
    FIELDSET = FieldSet(
        "evaluate_additional_classes",
        name=_("Client Classes"),
    )

    evaluate_additional_classes = DynamicModelMultipleChoiceField(
        queryset=ClientClass.objects.all(),
        required=False,
        quick_add=True,
        label=_("Evaluate Additional Classes"),
    )


class PrefixFormMixin(forms.Form):
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=True,
        selector=True,
        context={
            "depth": None,
        },
        quick_add=True,
        label=_("Prefix"),
    )


class DDNSUpdateFormMixin(forms.Form):
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

    def init_ddns_fields(self):
        self.fields["ddns_send_updates"].widget.attrs.update(
            {
                "hx-get": ".",
                "hx-include": "#form_fields",
                "hx-target": "#form_fields",
            }
        )

        if not get_field_value(self, "ddns_send_updates") == "True":
            for field_name in DDNSUpdateFormMixin.FIELDS:
                if field_name != "ddns_send_updates":
                    del self.fields[field_name]

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
        empty_value=None,
        required=False,
    )
    ddns_qualifying_suffix = forms.CharField(
        label=_("Qualifying Suffix"),
        empty_value=None,
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
        help_text=_("A decimal value between 0.000 and 1.000"),
        min_value=0.0,
        max_value=1.0,
        max_digits=4,
        decimal_places=3,
        required=False,
    )


class LifetimeFormMixin(forms.Form):
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

    def init_lifetime_fields(self, family=None):
        if family == IPAddressFamilyChoices.FAMILY_6:
            del self.fields["offer_lifetime"]
        elif family == IPAddressFamilyChoices.FAMILY_4:
            del self.fields["preferred_lifetime"]
            del self.fields["min_preferred_lifetime"]
            del self.fields["max_preferred_lifetime"]


class LeaseFormMixin(forms.Form):
    FIELDS = [
        "allocator",
        "adaptive_lease_time_threshold",
        "pd_allocator",
        "calculate_tee_times",
        "renew_timer",
        "rebind_timer",
        "t1_percent",
        "t2_percent",
        "match_client_id",
        "reservations_global",
        "reservations_out_of_pool",
        "reservations_in_subnet",
        "cache_threshold",
        "cache_max_age",
        "authoritative",
        "store_extended_info",
    ]
    FIELDSET = FieldSet(
        "allocator",
        "adaptive_lease_time_threshold",
        "pd_allocator",
        "calculate_tee_times",
        "renew_timer",
        "rebind_timer",
        "t1_percent",
        "t2_percent",
        "match_client_id",
        "reservations_global",
        "reservations_out_of_pool",
        "reservations_in_subnet",
        "cache_threshold",
        "cache_max_age",
        "authoritative",
        "store_extended_info",
        name=_("Lease"),
    )

    def init_lease_fields(self, family=None):
        self.fields["calculate_tee_times"].widget.attrs.update(DYNAMIC_ATTRIBUTES)
        self.fields["allocator"].widget.attrs.update(DYNAMIC_ATTRIBUTES)

        if get_field_value(self, "calculate_tee_times") == "True":
            del self.fields["renew_timer"]
            del self.fields["rebind_timer"]
        else:
            del self.fields["t1_percent"]
            del self.fields["t2_percent"]

        if get_field_value(self, "allocator") != AllocatorTypeChoices.FREE_LEASE_QUEUE:
            del self.fields["adaptive_lease_time_threshold"]

        if (
            (instance := self.instance).pk
            and hasattr(instance, "family")
            and instance.family != IPAddressFamilyChoices.FAMILY_6
        ):
            del self.fields["pd_allocator"]

        if family == IPAddressFamilyChoices.FAMILY_6:
            del self.fields["match_client_id"]
            del self.fields["authoritative"]

    calculate_tee_times = forms.NullBooleanField(
        label=_("Calculate T Times"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
    match_client_id = forms.NullBooleanField(
        label=_("Match Client ID"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
    authoritative = forms.NullBooleanField(
        label=_("Authoritative"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
    reservations_global = forms.NullBooleanField(
        label=_("Global reservations"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
    reservations_out_of_pool = forms.NullBooleanField(
        label=_("Out-of-pool reservations"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
    reservations_in_subnet = forms.NullBooleanField(
        label=_("In-subnet reservations"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
    store_extended_info = forms.NullBooleanField(
        label=_("Store extended info"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
    t1_percent = forms.DecimalField(
        label=_("T1"),
        help_text=_("A decimal value between 0.000 and 1.000"),
        max_digits=4,
        decimal_places=3,
        min_value=0.0,
        max_value=1.0,
        required=False,
    )
    t2_percent = forms.DecimalField(
        label=_("T2"),
        help_text=_("A decimal value between 0.000 and 1.000"),
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
    adaptive_lease_time_threshold = forms.DecimalField(
        label=_("Adaptive Lease Time Threshold"),
        help_text=_("A decimal value between 0.00 and 1.00"),
        max_digits=3,
        decimal_places=2,
        min_value=0.0,
        max_value=1.0,
        required=False,
    )
    allocator = forms.ChoiceField(
        choices=add_blank_choice(AllocatorTypeChoices),
        required=False,
        label=_("Allocator"),
    )
    pd_allocator = forms.ChoiceField(
        choices=add_blank_choice(PDAllocatorTypeChoices),
        required=False,
        label=_("Prefix Delegation Allocator"),
    )


class SubnetFormMixin(forms.Form):
    FIELDS = [
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


class DHCPServerFormMixin(forms.Form):
    FIELDS = [
        "dhcp_server",
    ]

    dhcp_server = DynamicModelChoiceField(
        queryset=DHCPServer.objects.all(),
        required=False,
        label=_("DHCP Server"),
    )


class SharedNetworkFormMixin(forms.Form):
    FIELDS = [
        "shared_network",
    ]

    shared_network = DynamicModelChoiceField(
        queryset=SharedNetwork.objects.all(),
        required=False,
        context={
            "description": "prefix_display",
        },
        label=_("Shared Network"),
    )


class NetworkFormMixin(forms.Form):
    FIELDS = [
        "server_interfaces",
        "relay",
        "interface_id",
        "rapid_commit",
    ]
    FIELDSET = FieldSet(
        "server_interfaces",
        "relay",
        "interface_id",
        "rapid_commit",
        name=_("Network"),
    )

    def init_network_fields(self, family=None):
        if family == IPAddressFamilyChoices.FAMILY_4:
            del self.fields["interface_id"]
            del self.fields["rapid_commit"]

    server_interfaces = DynamicModelMultipleChoiceField(
        queryset=DHCPServerInterface.objects.all(),
        required=False,
        label=_("Interfaces"),
        context={
            "parent": "dhcp_server",
        },
    )
    rapid_commit = forms.NullBooleanField(
        label=_("Rapid Commit"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        required=False,
    )
