from typing import Annotated, TYPE_CHECKING

import strawberry
import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from strawberry.scalars import ID

from netbox.graphql.filters import PrimaryModelFilter

if TYPE_CHECKING:
    from netbox.graphql.filter_lookups import IntegerArrayLookup
    from dcim.graphql.filters import DeviceFilter, InterfaceFilter
    from virtualization.graphql.filters import VirtualMachineFilter, VMInterfaceFilter
    from .enums import (
        NetBoxDHCPServerStatusEnum,
        NetBoxDHCPServerIDTypeEnum,
    )
    from .dhcp_cluster import NetBoxDHCPClusterFilter

from netbox_dhcp.models import DHCPServer

from .mixins import (
    ClientClassGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
    ChildSharedNetworkGraphQLFilterMixin,
    ChildSubnetGraphQLFilterMixin,
    ChildHostReservationGraphQLFilterMixin,
)

__all__ = ("NetBoxDHCPServerFilter",)


@strawberry_django.filter_type(DHCPServer, lookups=True)
class NetBoxDHCPServerFilter(
    ClientClassGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
    ChildSharedNetworkGraphQLFilterMixin,
    ChildSubnetGraphQLFilterMixin,
    ChildHostReservationGraphQLFilterMixin,
    PrimaryModelFilter,
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    server_id: (
        Annotated[
            "NetBoxDHCPServerIDTypeEnum", strawberry.lazy("netbox_dhcp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    status: (
        Annotated[
            "NetBoxDHCPServerStatusEnum", strawberry.lazy("netbox_dhcp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    #   host_reservation_identifiers: Array Lookup with Enum elements
    echo_client_id: FilterLookup[bool] | None = strawberry_django.filter_field()
    relay_supplied_options: (
        Annotated[
            "IntegerArrayLookup", strawberry.lazy("netbox.graphql.filter_lookups")
        ]
        | None
    ) = strawberry_django.filter_field()
    dhcp_cluster: (
        Annotated[
            "NetBoxDHCPClusterFilter", strawberry.lazy("netbox_dhcp.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    dhcp_cluster_id: ID | None = strawberry_django.filter_field()
    device: (
        Annotated["DeviceFilter", strawberry.lazy("dcim.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()
    device_interface: (
        Annotated["InterfaceFilter", strawberry.lazy("dcim.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    device_interface_id: ID | None = strawberry_django.filter_field()
    virtual_machine: (
        Annotated[
            "VirtualMachineFilter", strawberry.lazy("virtualization.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    virtual_machine_id: ID | None = strawberry_django.filter_field()
    virtual_machine_interface: (
        Annotated[
            "VMInterfaceFilter", strawberry.lazy("virtualization.graphql.filters")
        ]
        | None
    ) = strawberry_django.filter_field()
    virtual_machine_interface_id: ID | None = strawberry_django.filter_field()
