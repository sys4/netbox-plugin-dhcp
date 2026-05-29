import strawberry
import strawberry_django

from .types import (
    NetBoxDHCPClientClassType,
    NetBoxDHCPDHCPClusterType,
    NetBoxDHCPDHCPServerType,
    NetBoxDHCPHostReservationType,
    NetBoxDHCPOptionDefinitionType,
    NetBoxDHCPOptionType,
    NetBoxDHCPPDPoolType,
    NetBoxDHCPPoolType,
    NetBoxDHCPSharedNetworkType,
    NetBoxDHCPSubnetType,
)


@strawberry.type(name="Query")
class NetBoxDHCPClusterQuery:
    netbox_dhcp_dhcp_cluster: NetBoxDHCPDHCPClusterType = strawberry_django.field()
    netbox_dhcp_dhcp_cluster_list: list[NetBoxDHCPDHCPClusterType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxDHCPServerQuery:
    netbox_dhcp_dhcp_server: NetBoxDHCPDHCPServerType = strawberry_django.field()
    netbox_dhcp_dhcp_server_list: list[NetBoxDHCPDHCPServerType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxDHCPClientClassQuery:
    netbox_dhcp_client_class: NetBoxDHCPClientClassType = strawberry_django.field()
    netbox_dhcp_client_class_list: list[NetBoxDHCPClientClassType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxDHCPHostReservationQuery:
    netbox_dhcp_host_reservation: NetBoxDHCPHostReservationType = (
        strawberry_django.field()
    )
    netbox_dhcp_host_reservation_list: list[NetBoxDHCPHostReservationType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxDHCPOptionDefinitionQuery:
    netbox_dhcp_option_definition: NetBoxDHCPOptionDefinitionType = (
        strawberry_django.field()
    )
    netbox_dhcp_option_definition_list: list[NetBoxDHCPOptionDefinitionType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxDHCPOptionQuery:
    netbox_dhcp_option: NetBoxDHCPOptionType = strawberry_django.field()
    netbox_dhcp_option_list: list[NetBoxDHCPOptionType] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxDHCPPDPoolQuery:
    netbox_dhcp_prefix_delegation_pool: NetBoxDHCPPDPoolType = strawberry_django.field()
    netbox_dhcp_prefix_delegation_pool_list: list[NetBoxDHCPPDPoolType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxDHCPPoolQuery:
    netbox_dhcp_pool: NetBoxDHCPPoolType = strawberry_django.field()
    netbox_dhcp_pool_list: list[NetBoxDHCPPoolType] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxDHCPSubnetQuery:
    netbox_dhcp_subnet: NetBoxDHCPSubnetType = strawberry_django.field()
    netbox_dhcp_subnet_list: list[NetBoxDHCPSubnetType] = strawberry_django.field()


@strawberry.type(name="Query")
class NetBoxDHCPSharedNetworkQuery:
    netbox_dhcp_shared_network: NetBoxDHCPSharedNetworkType = strawberry_django.field()
    netbox_dhcp_shared_network_list: list[NetBoxDHCPSharedNetworkType] = (
        strawberry_django.field()
    )
