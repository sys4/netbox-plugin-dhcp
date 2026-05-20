import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from netbox_dhcp.models import Subnet

from .mixins import (
    BOOTPGraphQLFilterMixin,
    ChildHostReservationGraphQLFilterMixin,
    ChildPDPoolGraphQLFilterMixin,
    ChildPoolGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    LeaseGraphQLFilterMixin,
    LifetimeGraphQLFilterMixin,
    NetworkGraphQLFilterMixin,
    PrefixGraphQLFilterMixin,
)


@strawberry_django.filter_type(Subnet, lookups=True)
class NetBoxDHCPSubnetFilter(
    PrefixGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
    LifetimeGraphQLFilterMixin,
    NetworkGraphQLFilterMixin,
    LeaseGraphQLFilterMixin,
    ChildPoolGraphQLFilterMixin,
    ChildPDPoolGraphQLFilterMixin,
    ChildHostReservationGraphQLFilterMixin,
    PrimaryModelFilter,
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    weight: FilterLookup[int] | None = strawberry_django.filter_field()
    subnet_id: FilterLookup[int] | None = strawberry_django.filter_field()
