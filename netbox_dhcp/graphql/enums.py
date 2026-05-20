import strawberry

from netbox_dhcp.choices import (
    AllocatorTypeChoices,
    DDNSReplaceClientNameChoices,
    DHCPClusterStatusChoices,
    DHCPServerIDTypeChoices,
    DHCPServerStatusChoices,
    HostReservationIdentifierChoices,
    OptionSpaceChoices,
    OptionTypeChoices,
    PDAllocatorTypeChoices,
)

__all__ = (
    "NetBoxDHCPDDNSReplaceClientNameEnum",
    "NetBoxDHCPClusterStatusEnum",
    "NetBoxDHCPServerStatusEnum",
    "NetBoxDHCPServerIDTypeEnum",
    "NetBoxDHCPHostReservationIdentifierEnum",
    "NetBoxDHCPAllocatorTypeEnum",
    "NetBoxDHCPPDAllocatorTypeEnum",
    "NetBoxDHCPOptionSpaceEnum",
    "NetBoxDHCPOptionTypeEnum",
)

NetBoxDHCPDDNSReplaceClientNameEnum = strawberry.enum(
    DDNSReplaceClientNameChoices.as_enum()
)
NetBoxDHCPClusterStatusEnum = strawberry.enum(DHCPClusterStatusChoices.as_enum())
NetBoxDHCPServerStatusEnum = strawberry.enum(DHCPServerStatusChoices.as_enum())
NetBoxDHCPServerIDTypeEnum = strawberry.enum(DHCPServerIDTypeChoices.as_enum())
NetBoxDHCPHostReservationIdentifierEnum = strawberry.enum(
    HostReservationIdentifierChoices.as_enum()
)
NetBoxDHCPAllocatorTypeEnum = strawberry.enum(AllocatorTypeChoices.as_enum())
NetBoxDHCPPDAllocatorTypeEnum = strawberry.enum(PDAllocatorTypeChoices.as_enum())
NetBoxDHCPOptionSpaceEnum = strawberry.enum(OptionSpaceChoices.as_enum())
NetBoxDHCPOptionTypeEnum = strawberry.enum(OptionTypeChoices.as_enum())
