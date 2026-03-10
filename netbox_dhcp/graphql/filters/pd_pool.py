from typing import Annotated, TYPE_CHECKING

import strawberry
from strawberry.scalars import ID
import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

from netbox_dhcp.models import PDPool

from .mixins import (
    SubnetGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    PrefixGraphQLFilterMixin,
)

if TYPE_CHECKING:
    from ipam.graphql.filters import PrefixFilter


@strawberry_django.filter_type(PDPool, lookups=True)
class NetBoxDHCPPDPoolFilter(
    SubnetGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    PrefixGraphQLFilterMixin,
    PrimaryModelFilter,
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    weight: FilterLookup[int] | None = strawberry_django.filter_field()
    pool_id: FilterLookup[int] | None = strawberry_django.filter_field()
    delegated_length: FilterLookup[int] | None = strawberry_django.filter_field()
    excluded_prefix: (
        Annotated["PrefixFilter", strawberry.lazy("ipam.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    excluded_prefix_id: ID | None = strawberry_django.filter_field()
