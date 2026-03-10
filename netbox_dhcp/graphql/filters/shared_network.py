import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

from netbox_dhcp.models import SharedNetwork

from .mixins import (
    DHCPServerGraphQLFilterMixin,
    PrefixGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
    LifetimeGraphQLFilterMixin,
    NetworkGraphQLFilterMixin,
    LeaseGraphQLFilterMixin,
    ChildSubnetGraphQLFilterMixin,
)


@strawberry_django.filter_type(SharedNetwork, lookups=True)
class NetBoxDHCPSharedNetworkFilter(
    DHCPServerGraphQLFilterMixin,
    PrefixGraphQLFilterMixin,
    ClientClassGraphQLFilterMixin,
    EvaluateClientClassGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    DDNSUpdateGraphQLFilterMixin,
    LifetimeGraphQLFilterMixin,
    NetworkGraphQLFilterMixin,
    LeaseGraphQLFilterMixin,
    ChildSubnetGraphQLFilterMixin,
    PrimaryModelFilter,
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    weight: FilterLookup[int] | None = strawberry_django.filter_field()
