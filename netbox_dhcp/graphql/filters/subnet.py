import strawberry_django
from strawberry_django import FilterLookup, StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

from netbox_dhcp.models import Subnet

from .mixins import (
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
