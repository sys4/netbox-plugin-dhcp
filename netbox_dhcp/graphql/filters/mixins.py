from dataclasses import dataclass

from typing import Annotated, TYPE_CHECKING

import strawberry
from strawberry.scalars import ID
import strawberry_django
from strawberry_django import FilterLookup, StrFilterLookup

if TYPE_CHECKING:
    from ipam.graphql.filters import (
        PrefixFilter,
    )
    from netbox_dhcp.graphql.filters import (
        NetBoxDHCPClientClassFilter,
        NetBoxDHCPSubnetFilter,
        NetBoxDHCPSharedNetworkFilter,
        NetBoxDHCPPoolFilter,
        NetBoxDHCPPDPoolFilter,
        NetBoxDHCPHostReservationFilter,
        NetBoxDHCPServerFilter,
    )
    from netbox_dhcp.graphql.enums import (
        NetBoxDHCPAllocatorTypeEnum,
        NetBoxDHCPPDAllocatorTypeEnum,
    )


__all__ = (
    "BOOTPGraphQLFilterMixin",
    "DDNSUpdateGraphQLFilterMixin",
    "OfferLifetimeGraphQLFilterMixin",
    "LifetimeGraphQLFilterMixin",
    "LeaseGraphQLFilterMixin",
    "ClientClassGraphQLFilterMixin",
    "EvaluateClientClassGraphQLFilterMixin",
    "PrefixGraphQLFilterMixin",
    "ChildSubnetGraphQLFilterMixin",
    "ChildSharedNetworkGraphQLFilterMixin",
    "ChildPDPoolGraphQLFilterMixin",
    "ChildPoolGraphQLFilterMixin",
    "ChildHostReservationGraphQLFilterMixin",
    "NetworkGraphQLFilterMixin",
    "SubnetGraphQLFilterMixin",
    "DHCPServerGraphQLFilterMixin",
)


@dataclass
class BOOTPGraphQLFilterMixin:
    next_server: StrFilterLookup[str] | None = strawberry_django.filter_field()
    server_hostname: StrFilterLookup[str] | None = strawberry_django.filter_field()
    boot_file_name: StrFilterLookup[str] | None = strawberry_django.filter_field()


@dataclass
class DDNSUpdateGraphQLFilterMixin:
    ddns_send_updates: FilterLookup[bool] | None = strawberry_django.filter_field()
    ddns_override_no_update: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
    ddns_override_client_update: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
    ddns_replace_client_name: StrFilterLookup[str] | None = (
        strawberry_django.filter_field()
    )
    ddns_generated_prefix: StrFilterLookup[str] | None = (
        strawberry_django.filter_field()
    )
    ddns_qualifying_suffix: StrFilterLookup[str] | None = (
        strawberry_django.filter_field()
    )
    ddns_update_on_renew: FilterLookup[bool] | None = strawberry_django.filter_field()
    ddns_conflict_resolution_mode: StrFilterLookup[str] | None = (
        strawberry_django.filter_field()
    )
    ddns_ttl_percent: FilterLookup[float] | None = strawberry_django.filter_field()
    ddns_ttl: FilterLookup[int] | None = strawberry_django.filter_field()
    ddns_ttl_min: FilterLookup[int] | None = strawberry_django.filter_field()
    ddns_ttl_max: FilterLookup[int] | None = strawberry_django.filter_field()
    hostname_char_set: StrFilterLookup[str] | None = strawberry_django.filter_field()
    hostname_char_replacement: StrFilterLookup[str] | None = (
        strawberry_django.filter_field()
    )


@strawberry.type
class OfferLifetimeGraphQLFilterMixin:
    offer_lifetime: FilterLookup[int] | None = strawberry_django.filter_field()


@strawberry.type
class LifetimeGraphQLFilterMixin(OfferLifetimeGraphQLFilterMixin):
    valid_lifetime: FilterLookup[int] | None = strawberry_django.filter_field()
    min_valid_lifetime: FilterLookup[int] | None = strawberry_django.filter_field()
    max_valid_lifetime: FilterLookup[int] | None = strawberry_django.filter_field()
    preferred_lifetime: FilterLookup[int] | None = strawberry_django.filter_field()
    min_preferred_lifetime: FilterLookup[int] | None = strawberry_django.filter_field()
    max_preferred_lifetime: FilterLookup[int] | None = strawberry_django.filter_field()


@dataclass
class LeaseGraphQLFilterMixin:
    renew_timer: FilterLookup[int] | None = strawberry_django.filter_field()
    rebind_timer: FilterLookup[int] | None = strawberry_django.filter_field()
    match_client_id: FilterLookup[bool] | None = strawberry_django.filter_field()
    authoritative: FilterLookup[bool] | None = strawberry_django.filter_field()
    reservations_global: FilterLookup[bool] | None = strawberry_django.filter_field()
    reservations_out_of_pool: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
    reservations_in_subnet: FilterLookup[bool] | None = strawberry_django.filter_field()
    calculate_tee_times: FilterLookup[bool] | None = strawberry_django.filter_field()
    t1_percent: FilterLookup[float] | None = strawberry_django.filter_field()
    t2_percent: FilterLookup[float] | None = strawberry_django.filter_field()
    cache_threshold: FilterLookup[float] | None = strawberry_django.filter_field()
    cache_max_age: FilterLookup[int] | None = strawberry_django.filter_field()
    adaptive_lease_time_threshold: FilterLookup[float] | None = (
        strawberry_django.filter_field()
    )
    store_extended_info: FilterLookup[bool] | None = strawberry_django.filter_field()
    allocator: (
        Annotated[
            "NetBoxDHCPAllocatorTypeEnum", strawberry.lazy("netbox_dhcp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    pd_allocator: (
        Annotated[
            "NetBoxDHCPPDAllocatorTypeEnum",
            strawberry.lazy("netbox_dhcp.graphql.enums"),
        ]
        | None
    ) = strawberry_django.filter_field()


@dataclass
class ClientClassGraphQLFilterMixin:
    client_class: (
        Annotated[
            "NetBoxDHCPClientClassFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    client_class_id: ID | None = strawberry_django.filter_field()


@dataclass
class EvaluateClientClassGraphQLFilterMixin:
    evaluate_additional_class: (
        Annotated[
            "NetBoxDHCPClientClassFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    evaluate_additional_class_id: ID | None = strawberry_django.filter_field()


@dataclass
class PrefixGraphQLFilterMixin:
    prefix: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    prefix_id: ID | None = strawberry_django.filter_field()


@dataclass
class ChildSharedNetworkGraphQLFilterMixin:
    child_shared_network: (
        Annotated[
            "NetBoxDHCPSharedNetworkFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    child_shared_network_id: ID | None = strawberry_django.filter_field()


@dataclass
class ChildSubnetGraphQLFilterMixin:
    child_subnet: (
        Annotated[
            "NetBoxDHCPSubnetFilter", strawberry.lazy("netbox_dhcp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    child_subnet_id: ID | None = strawberry_django.filter_field()


@dataclass
class ChildPoolGraphQLFilterMixin:
    child_pool: (
        Annotated[
            "NetBoxDHCPPoolFilter", strawberry.lazy("netbox_dhcp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    child_pool_id: ID | None = strawberry_django.filter_field()


@dataclass
class ChildPDPoolGraphQLFilterMixin:
    child_pd_pool: (
        Annotated[
            "NetBoxDHCPPDPoolFilter", strawberry.lazy("netbox_dhcp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    child_pd_pool_id: ID | None = strawberry_django.filter_field()


@dataclass
class ChildHostReservationGraphQLFilterMixin:
    child_host_reservation: (
        Annotated[
            "NetBoxDHCPHostReservationFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    child_host_reservation_id: ID | None = strawberry_django.filter_field()


@dataclass
class NetworkGraphQLFilterMixin:
    relay: StrFilterLookup[str] | None = strawberry_django.filter_field()
    interface_id: FilterLookup[int] | None = strawberry_django.filter_field()
    rapid_commit: FilterLookup[bool] | None = strawberry_django.filter_field()


@dataclass
class SubnetGraphQLFilterMixin:
    subnet: (
        Annotated[
            "NetBoxDHCPSubnetFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    subnet_id: ID | None = strawberry_django.filter_field()


@dataclass
class DHCPServerGraphQLFilterMixin:
    dhcp_server: (
        Annotated[
            "NetBoxDHCPServerFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    dhcp_server_id: ID | None = strawberry_django.filter_field()
