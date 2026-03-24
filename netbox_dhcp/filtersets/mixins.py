import django_filters
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet
from ipam.models import Prefix

from netbox_dhcp.models import (
    ClientClass,
    Subnet,
    Pool,
    PDPool,
    HostReservation,
    SharedNetwork,
    DHCPServer,
    DHCPServerInterface,
    OptionDefinition,
)
from netbox_dhcp.choices import (
    DDNSReplaceClientNameChoices,
    DDNSConflictResolutionModeChoices,
    AllocatorTypeChoices,
    PDAllocatorTypeChoices,
)

__all__ = (
    "BOOTPFilterMixin",
    "OfferLifetimeFilterMixin",
    "LeaseFilterMixin",
    "NetworkFilterMixin",
    "PrefixFilterMixin",
    "ClientClassFilterMixin",
    "EvaluateClientClassFilterMixin",
    "DDNSUpdateFilterMixin",
    "SubnetFilterMixin",
    "DHCPServerFilterMixin",
    "SharedNetworkFilterMixin",
    "ChildSubnetFilterMixin",
    "ChildSharedNetworkFilterMixin",
    "ChildPoolFilterMixin",
    "ChildPDPoolFilterMixin",
    "ChildHostReservationFilterMixin",
    "OptionFilterMixin",
)


class BOOTPFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "next_server",
        "server_hostname",
        "boot_file_name",
    ]


class OfferLifetimeFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "offer_lifetime",
    ]


class LifetimeFilterMixin(OfferLifetimeFilterMixin):
    FILTER_FIELDS = [
        "offer_lifetime",
        "valid_lifetime",
        "min_valid_lifetime",
        "max_valid_lifetime",
        "preferred_lifetime",
        "min_preferred_lifetime",
        "max_preferred_lifetime",
    ]


class LeaseFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = (
        "renew_timer",
        "rebind_timer",
        "match_client_id",
        "authoritative",
        "reservations_global",
        "reservations_out_of_pool",
        "reservations_in_subnet",
        "calculate_tee_times",
        "t1_percent",
        "t2_percent",
        "cache_threshold",
        "cache_max_age",
        "adaptive_lease_time_threshold",
        "store_extended_info",
        "allocator",
        "pd_allocator",
    )

    allocator = django_filters.MultipleChoiceFilter(
        choices=AllocatorTypeChoices,
        label=_("Allocator"),
    )
    pd_allocator = django_filters.MultipleChoiceFilter(
        choices=PDAllocatorTypeChoices,
        label=_("Prefix Delegation Allocator"),
    )


class ClientClassFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "client_class_id",
    ]
    client_class = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="client_classes__name",
        to_field_name="name",
        label=_("Client Class"),
    )
    client_class_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="client_classes",
        label=_("Client Class ID"),
    )


class EvaluateClientClassFilterMixin(NetBoxModelFilterSet):
    evaluate_additional_class = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="evaluate_additional_classes__name",
        to_field_name="name",
        label=_("Evaluate Additional Class"),
    )
    evaluate_additional_class_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="evaluate_additional_classes",
        label=_("Evaluate Additional Class ID"),
    )


class DDNSUpdateFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "hostname_char_set",
        "hostname_char_replacement",
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
    ]

    ddns_replace_client_name = django_filters.MultipleChoiceFilter(
        choices=DDNSReplaceClientNameChoices,
        label=_("Replace Client Name"),
    )
    ddns_conflict_resolution_mode = django_filters.MultipleChoiceFilter(
        choices=DDNSConflictResolutionModeChoices,
        label=_("Conflict Resolution Mode"),
    )


class NetworkFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "server_interfaces",
        "relay",
        "interface_id",
        "rapid_commit",
    ]

    server_interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DHCPServerInterface.objects.all(),
        field_name="server_interfaces",
        label=_("Server Interface ID"),
    )


class PrefixFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "prefix",
    ]

    prefix_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
        field_name="prefix",
        label=_("Prefix ID"),
    )
    prefix = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
        field_name="prefix__prefix",
        to_field_name="prefix",
        label=_("Prefix"),
    )


class DHCPServerFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "dhcp_server",
    ]

    dhcp_server = django_filters.ModelMultipleChoiceFilter(
        queryset=DHCPServer.objects.all(),
        field_name="dhcp_server__name",
        to_field_name="name",
        label=_("DHCP Server"),
    )
    dhcp_server_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DHCPServer.objects.all(),
        field_name="dhcp_server",
        label=_("DHCP Server ID"),
    )


class SubnetFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "subnet",
    ]

    subnet = django_filters.ModelMultipleChoiceFilter(
        queryset=Subnet.objects.all(),
        field_name="subnet__name",
        to_field_name="name",
        label=_("Subnet"),
    )
    subnet_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Subnet.objects.all(),
        field_name="subnet",
        label=_("Subnet ID"),
    )


class SharedNetworkFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "shared_network",
    ]

    shared_network = django_filters.ModelMultipleChoiceFilter(
        queryset=SharedNetwork.objects.all(),
        field_name="shared_network__name",
        to_field_name="name",
        label=_("Shared Network"),
    )
    shared_network_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SharedNetwork.objects.all(),
        field_name="shared_network",
        label=_("Shared Network ID"),
    )


class ChildSubnetFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "child_subnets",
    ]

    child_subnet = django_filters.ModelMultipleChoiceFilter(
        queryset=Subnet.objects.all(),
        field_name="child_subnets__name",
        to_field_name="name",
        label=_("Subnet"),
    )
    child_subnet_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Subnet.objects.all(),
        field_name="child_subnets",
        label=_("Subnet ID"),
    )


class ChildSharedNetworkFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "child_shared_networks",
    ]

    child_shared_network = django_filters.ModelMultipleChoiceFilter(
        queryset=SharedNetwork.objects.all(),
        field_name="child_shared_networks__name",
        to_field_name="name",
        label=_("Shared Network"),
    )
    child_shared_network_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SharedNetwork.objects.all(),
        field_name="child_shared_networks",
        label=_("Shared Network ID"),
    )


class ChildPoolFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "child_pools",
    ]

    child_pool = django_filters.ModelMultipleChoiceFilter(
        queryset=Pool.objects.all(),
        field_name="child_pools__name",
        to_field_name="name",
        label=_("Pool"),
    )
    child_pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Pool.objects.all(),
        field_name="child_pools",
        label=_("Pool ID"),
    )


class ChildPDPoolFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "child_pd_pools",
    ]

    child_pd_pool = django_filters.ModelMultipleChoiceFilter(
        queryset=PDPool.objects.all(),
        field_name="child_pd_pools__name",
        to_field_name="name",
        label=_("Prefix Delegation Pool"),
    )
    child_pd_pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=PDPool.objects.all(),
        field_name="child_pd_pools",
        label=_("Prefix Delegation Pool ID"),
    )


class ChildHostReservationFilterMixin(NetBoxModelFilterSet):
    FILTER_FIELDS = [
        "child_host_reservations",
    ]

    child_host_reservation = django_filters.ModelMultipleChoiceFilter(
        queryset=HostReservation.objects.all(),
        field_name="child_host_reservations__name",
        to_field_name="name",
        label=_("Host Reservation"),
    )
    child_host_reservation_id = django_filters.ModelMultipleChoiceFilter(
        queryset=HostReservation.objects.all(),
        field_name="child_host_reservations",
        label=_("Host Reservation ID"),
    )


class OptionFilterMixin(NetBoxModelFilterSet):
    option_name = django_filters.ModelMultipleChoiceFilter(
        queryset=OptionDefinition.objects.all(),
        method="filter_option",
        to_field_name="name",
        label=_("Option Name"),
    )
    option_code = django_filters.ModelMultipleChoiceFilter(
        queryset=OptionDefinition.objects.all(),
        method="filter_option",
        to_field_name="code",
        label=_("Option Code"),
    )
    option_space = django_filters.ModelMultipleChoiceFilter(
        queryset=OptionDefinition.objects.all(),
        method="filter_option",
        to_field_name="space",
        label=_("Option Space"),
    )

    def filter_option(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(options__definition__in=value).distinct()
