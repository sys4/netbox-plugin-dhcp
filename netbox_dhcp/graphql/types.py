from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType

if TYPE_CHECKING:
    from dcim.graphql.types import DeviceType, InterfaceType, MACAddressType
    from ipam.graphql.types import IPAddressType, IPRangeType, PrefixType
    from virtualization.graphql.types import VirtualMachineType, VMInterfaceType

from netbox_dhcp.models import (
    ClientClass,
    DHCPCluster,
    DHCPServer,
    HostReservation,
    Option,
    OptionDefinition,
    PDPool,
    Pool,
    SharedNetwork,
    Subnet,
)

from .filters import (
    NetBoxDHCPClientClassFilter,
    NetBoxDHCPDHCPClusterFilter,
    NetBoxDHCPDHCPServerFilter,
    NetBoxDHCPHostReservationFilter,
    NetBoxDHCPOptionDefinitionFilter,
    NetBoxDHCPOptionFilter,
    NetBoxDHCPPDPoolFilter,
    NetBoxDHCPPoolFilter,
    NetBoxDHCPSharedNetworkFilter,
    NetBoxDHCPSubnetFilter,
)


@strawberry.type
class BOOTPGraphQLTypeMixin:
    next_server: str | None
    server_hostname: str | None
    boot_file_name: str | None


@strawberry.type
class DDNSUpdateGraphQLTypeMixin:
    ddns_send_updates: bool | None
    ddns_override_no_update: bool | None
    ddns_override_client_update: bool | None
    ddns_replace_client_name: str | None
    ddns_generated_prefix: str | None
    ddns_qualifying_suffix: str | None
    ddns_update_on_renew: bool | None
    ddns_conflict_resolution_mode: str | None
    ddns_ttl_percent: float | None
    ddns_ttl: int | None
    ddns_ttl_min: int | None
    ddns_ttl_max: int | None
    hostname_char_set: str | None
    hostname_char_replacement: str | None


@strawberry.type
class OfferLifetimeGraphQLTypeMixin:
    offer_lifetime: int | None


@strawberry.type
class LifetimeGraphQLTypeMixin(OfferLifetimeGraphQLTypeMixin):
    valid_lifetime: int | None
    min_valid_lifetime: int | None
    max_valid_lifetime: int | None
    preferred_lifetime: int | None
    min_preferred_lifetime: int | None
    max_preferred_lifetime: int | None


@strawberry.type
class LeaseGraphQLTypeMixin:
    renew_timer: int | None
    rebind_timer: int | None
    match_client_id: bool | None
    authoritative: bool | None
    reservations_global: bool | None
    reservations_out_of_pool: bool | None
    reservations_in_subnet: bool | None
    calculate_tee_times: bool | None
    t1_percent: float | None
    t2_percent: float | None
    cache_threshold: float | None
    cache_max_age: int | None
    adaptive_lease_time_threshold: float | None
    store_extended_info: bool | None
    allocator: str | None
    pd_allocator: str | None


@strawberry.type
class NetworkGraphQLTypeMixin:
    relay: int | None
    interface_id: str | None
    rapid_commit: bool | None


@strawberry.type
class ChildSubnetGraphQLTypeMixin:
    child_subnets: list[
        Annotated["NetBoxDHCPSubnetType", strawberry.lazy("netbox_dhcp.graphql.types")]
    ]


@strawberry.type
class ChildSharedNetworkGraphQLTypeMixin:
    child_shared_networks: list[
        Annotated[
            "NetBoxDHCPSharedNetworkType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
    ]


@strawberry.type
class ChildPDPoolGraphQLTypeMixin:
    child_pd_pools: list[
        Annotated["NetBoxDHCPPDPoolType", strawberry.lazy("netbox_dhcp.graphql.types")]
    ]


@strawberry.type
class ChildPoolGraphQLTypeMixin:
    child_pools: list[
        Annotated["NetBoxDHCPPoolType", strawberry.lazy("netbox_dhcp.graphql.types")]
    ]


@strawberry.type
class ChildHostReservationGraphQLTypeMixin:
    child_host_reservations: list[
        Annotated[
            "NetBoxDHCPHostReservationType",
            strawberry.lazy("netbox_dhcp.graphql.types"),
        ]
    ]


@strawberry.type
class ClientClassGraphQLTypeMixin:
    client_classes: list[
        Annotated[
            "NetBoxDHCPClientClassType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
    ]


@strawberry.type
class EvaluateClientClassGraphQLTypeMixin:
    evaluate_additional_classes: list[
        Annotated[
            "NetBoxDHCPClientClassType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
    ]


@strawberry.type
class DHCPServerGraphQLTypeMixin:
    dhcp_server: (
        Annotated[
            "NetBoxDHCPDHCPServerType",
            strawberry.lazy("netbox_dhcp.graphql.types"),
        ]
        | None
    )


@strawberry.type
class SubnetGraphQLTypeMixin:
    subnet: (
        Annotated[
            "NetBoxDHCPSubnetType",
            strawberry.lazy("netbox_dhcp.graphql.types"),
        ]
        | None
    )


@strawberry.type
class SharedNetworkGraphQLTypeMixin:
    shared_network: (
        Annotated[
            "NetBoxDHCPSharedNetworkType",
            strawberry.lazy("netbox_dhcp.graphql.types"),
        ]
        | None
    )


@strawberry_django.type(
    ClientClass, fields="__all__", filters=NetBoxDHCPClientClassFilter
)
class NetBoxDHCPClientClassType(
    DHCPServerGraphQLTypeMixin,
    BOOTPGraphQLTypeMixin,
    LifetimeGraphQLTypeMixin,
    PrimaryObjectType,
):
    name: str
    test: str | None
    template_test: str | None
    only_in_additional_list: bool | None


@strawberry_django.type(
    DHCPCluster, fields="__all__", filters=NetBoxDHCPDHCPClusterFilter
)
class NetBoxDHCPDHCPClusterType(PrimaryObjectType):
    name: str
    status: str
    dhcp_servers: list[
        Annotated[
            "NetBoxDHCPDHCPServerType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
    ]


@strawberry_django.type(
    DHCPServer, fields="__all__", filters=NetBoxDHCPDHCPServerFilter
)
class NetBoxDHCPDHCPServerType(
    BOOTPGraphQLTypeMixin,
    DDNSUpdateGraphQLTypeMixin,
    LifetimeGraphQLTypeMixin,
    LeaseGraphQLTypeMixin,
    ChildSubnetGraphQLTypeMixin,
    ChildSharedNetworkGraphQLTypeMixin,
    ChildHostReservationGraphQLTypeMixin,
    PrimaryObjectType,
):
    name: str
    status: str
    server_id: str | None
    #   host_reservation_identifiers:
    echo_client_id: bool | None
    relay_supplied_options: list[int] | None
    dhcp_cluster: (
        Annotated[
            "NetBoxDHCPDHCPClusterType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
        | None
    )
    device: Annotated["DeviceType", strawberry.lazy("dcim.graphql.types")] | None
    device_interfaces: (
        list[Annotated["InterfaceType", strawberry.lazy("dcim.graphql.types")]] | None
    )
    virtual_machine: (
        Annotated["VirtualMachineType", strawberry.lazy("virtualization.graphql.types")]
        | None
    )
    virtual_machine_interfaces: (
        list[
            Annotated[
                "VMInterfaceType", strawberry.lazy("virtualization.graphql.types")
            ]
        ]
        | None
    )
    decline_probation_period: float | None


@strawberry_django.type(
    HostReservation, fields="__all__", filters=NetBoxDHCPHostReservationFilter
)
class NetBoxDHCPHostReservationType(
    DHCPServerGraphQLTypeMixin,
    SubnetGraphQLTypeMixin,
    BOOTPGraphQLTypeMixin,
    PrimaryObjectType,
):
    name: str
    duid: str | None
    hw_address: (
        Annotated["MACAddressType", strawberry.lazy("dcim.graphql.types")] | None
    )
    flex_id: str | None
    circuit_id: str | None
    client_id: str | None
    hostname: str | None
    ipv4_address: (
        Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
    )
    ipv6_addresses: (
        list[Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    ipv6_prefixes: (
        list[Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    excluded_ipv6_prefixes: (
        list[Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]] | None
    )
    client_classes: (
        list[
            Annotated[
                "NetBoxDHCPClientClassType",
                strawberry.lazy("netbox_dhcp.graphql.types"),
            ]
        ]
        | None
    )


@strawberry_django.type(
    OptionDefinition, fields="__all__", filters=NetBoxDHCPOptionDefinitionFilter
)
class NetBoxDHCPOptionDefinitionType(PrimaryObjectType):
    name: str
    code: int
    space: str
    encapsulate: str | None
    family: int
    type: str
    record_types: list[str] | None
    dhcp_server: (
        Annotated[
            "NetBoxDHCPDHCPServerType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
        | None
    )
    client_class: (
        Annotated[
            "NetBoxDHCPClientClassType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
        | None
    )


@strawberry_django.type(
    Option,
    exclude=["assigned_object_type", "assigned_object_id"],
    filters=NetBoxDHCPOptionFilter,
)
class NetBoxDHCPOptionType(PrimaryObjectType):
    definition: Annotated[
        "NetBoxDHCPOptionDefinitionType", strawberry.lazy("netbox_dhcp.graphql.types")
    ]
    data: str | None
    weight: int | None
    csv_format: bool | None
    send_option: str | None

    @strawberry_django.field
    def assigned_object(
        self,
    ) -> Annotated[
        Annotated[
            "NetBoxDHCPDHCPServerType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
        | Annotated[
            "NetBoxDHCPSubnetType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
        | Annotated[
            "NetBoxDHCPSharedNetworkType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
        | Annotated["NetBoxDHCPPoolType", strawberry.lazy("netbox_dhcp.graphql.types")]
        | Annotated[
            "NetBoxDHCPPDPoolType", strawberry.lazy("netbox_dhcp.graphql.types")
        ]
        | Annotated[
            "NetBoxDHCPHostReservationType",
            strawberry.lazy("netbox_dhcp.graphql.types"),
        ]
        | Annotated[
            "NetBoxDHCPClientClassType", strawberry.lazy("netbox_dhcp.graphql.types")
        ],
        strawberry.union("OptionAssignmentType"),
    ]:
        return self.assigned_object


@strawberry_django.type(PDPool, fields="__all__", filters=NetBoxDHCPPDPoolFilter)
class NetBoxDHCPPDPoolType(
    SubnetGraphQLTypeMixin,
    ClientClassGraphQLTypeMixin,
    EvaluateClientClassGraphQLTypeMixin,
    PrimaryObjectType,
):
    name: str
    pool_id: int | None
    delegated_length: int
    # +
    # TODO: Actually prefix cannot be Npne, but the tests fail if it is not allowed.
    # -
    prefix: Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")] | None
    excluded_prefix: (
        Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")] | None
    )


@strawberry_django.type(Pool, fields="__all__", filters=NetBoxDHCPPoolFilter)
class NetBoxDHCPPoolType(
    SubnetGraphQLTypeMixin,
    ClientClassGraphQLTypeMixin,
    EvaluateClientClassGraphQLTypeMixin,
    DDNSUpdateGraphQLTypeMixin,
    PrimaryObjectType,
):
    name: str
    pool_id: int | None
    # +
    # TODO: Actually ip_range cannot be Npne, but the tests fail if it is not allowed.
    # -
    ip_range: Annotated["IPRangeType", strawberry.lazy("ipam.graphql.types")] | None


@strawberry_django.type(Subnet, fields="__all__", filters=NetBoxDHCPSubnetFilter)
class NetBoxDHCPSubnetType(
    DHCPServerGraphQLTypeMixin,
    SharedNetworkGraphQLTypeMixin,
    ClientClassGraphQLTypeMixin,
    EvaluateClientClassGraphQLTypeMixin,
    BOOTPGraphQLTypeMixin,
    DDNSUpdateGraphQLTypeMixin,
    LifetimeGraphQLTypeMixin,
    LeaseGraphQLTypeMixin,
    NetworkGraphQLTypeMixin,
    ChildPoolGraphQLTypeMixin,
    ChildPDPoolGraphQLTypeMixin,
    ChildHostReservationGraphQLTypeMixin,
    PrimaryObjectType,
):
    name: str
    subnet_id: int | None
    prefix: Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")] | None


@strawberry_django.type(
    SharedNetwork, fields="__all__", filters=NetBoxDHCPSharedNetworkFilter
)
class NetBoxDHCPSharedNetworkType(
    DHCPServerGraphQLTypeMixin,
    ClientClassGraphQLTypeMixin,
    EvaluateClientClassGraphQLTypeMixin,
    BOOTPGraphQLTypeMixin,
    DDNSUpdateGraphQLTypeMixin,
    LifetimeGraphQLTypeMixin,
    LeaseGraphQLTypeMixin,
    NetworkGraphQLTypeMixin,
    ChildSubnetGraphQLTypeMixin,
    PrimaryObjectType,
):
    name: str
    # +
    # TODO: Actually prefix cannot be Npne, but the tests fail if it is not allowed.
    # -
    prefix: Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")] | None
