import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

from netbox_dhcp.models import ClientClass

from .mixins import (
    DHCPServerGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    LifetimeGraphQLFilterMixin,
)


@strawberry_django.filter_type(ClientClass, lookups=True)
class NetBoxDHCPClientClassFilter(
    DHCPServerGraphQLFilterMixin,
    BOOTPGraphQLFilterMixin,
    LifetimeGraphQLFilterMixin,
    PrimaryModelFilter,
):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    weight: FilterLookup[int] | None = strawberry_django.filter_field()
    test: StrFilterLookup[str] | None = strawberry_django.filter_field()
    template_test: StrFilterLookup[str] | None = strawberry_django.filter_field()
    only_in_additional_list: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )
