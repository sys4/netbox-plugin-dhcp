from typing import Annotated, TYPE_CHECKING

import strawberry
import strawberry_django
from strawberry.scalars import ID
from strawberry_django import StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

if TYPE_CHECKING:
    from ipam.graphql.filters import IPAddressFilter, PrefixFilter
    from dcim.graphql.filters import MACAddressFilter
    from netbox_dhcp.filters import NetBoxDHCPClientClassFilter

from netbox_dhcp.models import HostReservation

from .mixins import (
    ClientClassGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
)

__all__ = ("NetBoxDHCPHostReservationFilter",)


@strawberry_django.filter_type(HostReservation, lookups=True)
class NetBoxDHCPHostReservationFilter(
    ClientClassGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    PrimaryModelFilter,
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    duid: StrFilterLookup[str] | None = strawberry_django.filter_field()
    hw_address: (
        Annotated["MACAddressFilter", strawberry.lazy("dcim.graphql.filters")] | None
    )
    hw_address_id: ID | None = strawberry_django.filter_field()
    flex_id: StrFilterLookup[str] | None = strawberry_django.filter_field()
    circuit_id: StrFilterLookup[str] | None = strawberry_django.filter_field()
    client_id: StrFilterLookup[str] | None = strawberry_django.filter_field()
    hostname: StrFilterLookup[str] | None = strawberry_django.filter_field()
    ipv4_address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    )
    ipv4_address_id: ID | None = strawberry_django.filter_field()
    ipv6_address: (
        Annotated["IPAddressFilter", strawberry.lazy("ipam.graphql.filters")] | None
    )
    ipv6_address_id: ID | None = strawberry_django.filter_field()
    ipv6_prefix: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    )
    ipv6_prefix_id: ID | None = strawberry_django.filter_field()
    excluded_ipv6_prefix: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    )
    excluded_ipv6_prefix_id: ID | None = strawberry_django.filter_field()
    client_class: (
        Annotated[
            "NetBoxDHCPClientClassFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    )
    client_class_id: ID | None = strawberry_django.filter_field()
