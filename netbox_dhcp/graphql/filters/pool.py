from typing import Annotated, TYPE_CHECKING

import strawberry
from strawberry.scalars import ID
import strawberry_django
from strawberry_django import FilterLookup, StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

from netbox_dhcp.models import Pool

from .mixins import (
    SubnetGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
)

if TYPE_CHECKING:
    from ipam.graphql.filters import IPRangeFilter


@strawberry_django.filter_type(Pool, lookups=True)
class NetBoxDHCPPoolFilter(
    SubnetGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
    PrimaryModelFilter,
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    weight: FilterLookup[int] | None = strawberry_django.filter_field()
    pool_id: FilterLookup[int] | None = strawberry_django.filter_field()
    ip_range: (
        Annotated["IPRangeFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    ip_range_id: ID | None = strawberry_django.filter_field()
