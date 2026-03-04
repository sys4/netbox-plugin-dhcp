from typing import Annotated, TYPE_CHECKING

import strawberry
from strawberry.scalars import ID
import strawberry_django
from strawberry_django import FilterLookup, StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

from netbox_dhcp.models import Option
from .mixins import ClientClassGraphQLFilterMixin

if TYPE_CHECKING:
    from core.graphql.filters import ContentTypeFilter
    from ipam.graphql.enums import IPAddressFamilyEnum
    from netbox_dhcp.graphql.enums import NetBoxDHCPOptionSpaceEnum
    from netbox_dhcp.graphql.filters import NetBoxDHCPOptionDefinitionFilter


@strawberry_django.filter_type(Option, lookups=True)
class NetBoxDHCPOptionFilter(
    ClientClassGraphQLFilterMixin,
    PrimaryModelFilter,
):
    definition: (
        Annotated[
            "NetBoxDHCPOptionDefinitionFilter",
            strawberry.lazy("netbox_dhcp.graphql.filters"),
        ]
        | None
    ) = strawberry_django.filter_field()
    definition_id: ID | None = strawberry_django.filter_field()
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    code: FilterLookup[int] | None = strawberry_django.filter_field()
    space: (
        Annotated[
            "NetBoxDHCPOptionSpaceEnum", strawberry.lazy("netbox_dhcp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    family: (
        Annotated["IPAddressFamilyEnum", strawberry.lazy("ipam.graphql.enums")] | None
    ) = strawberry_django.filter_field()
    data: StrFilterLookup[str] | None = strawberry_django.filter_field()
    weight: FilterLookup[int] | None = strawberry_django.filter_field()
    csv_format: FilterLookup[bool] | None = strawberry_django.filter_field()
    send_option: StrFilterLookup[str] | None = strawberry_django.filter_field()
    assigned_object_type: (
        Annotated["ContentTypeFilter", strawberry.lazy("core.graphql.filters")] | None
    ) = strawberry_django.filter_field()
    assigned_object_id: ID | None = strawberry_django.filter_field()
