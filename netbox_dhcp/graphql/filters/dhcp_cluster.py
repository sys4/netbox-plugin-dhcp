from typing import Annotated, TYPE_CHECKING

import strawberry
import strawberry_django

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

if TYPE_CHECKING:
    from .enums import (
        NetBoxDHCPClusterStatusEnum,
    )

from netbox_dhcp.models import DHCPCluster

__all__ = ("NetBoxDHCPClusterFilter",)


@strawberry_django.filter_type(DHCPCluster, lookups=True)
class NetBoxDHCPClusterFilter(PrimaryModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    status: (
        Annotated[
            "NetBoxDHCPClusterStatusEnum", strawberry.lazy("netbox_dhcp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
