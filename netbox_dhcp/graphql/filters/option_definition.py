from typing import Annotated, TYPE_CHECKING

import strawberry
import strawberry_django
from strawberry_django import FilterLookup

try:
    from strawberry_django import StrFilterLookup
except ImportError:
    from strawberry_django import FilterLookup as StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter

from netbox_dhcp.models import OptionDefinition

if TYPE_CHECKING:
    from dhcp.graphql.enums import IPAddressFamilyEnum
    from netbox_dhcp.graphql.enums import (
        NetBoxDHCPOptionSpaceEnum,
        NetBoxDHCPOptionTypeEnum,
    )


@strawberry_django.filter_type(OptionDefinition, lookups=True)
class NetBoxDHCPOptionDefinitionFilter(PrimaryModelFilter):
    name: StrFilterLookup[str] | None = strawberry_django.filter_field()
    code: FilterLookup[int] | None = strawberry_django.filter_field()
    space: (
        Annotated[
            "NetBoxDHCPOptionSpaceEnum", strawberry.lazy("netbox_dhcp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    encapsulate: StrFilterLookup[str] | None = strawberry_django.filter_field()
    family: (
        Annotated["IPAddressFamilyEnum", strawberry.lazy("ipam.graphql.enums")] | None
    ) = strawberry_django.filter_field()
    type: (
        Annotated[
            "NetBoxDHCPOptionTypeEnum", strawberry.lazy("netbox_dhcp.graphql.enums")
        ]
        | None
    ) = strawberry_django.filter_field()
    record_type: StrFilterLookup[str] | None = strawberry_django.filter_field()
