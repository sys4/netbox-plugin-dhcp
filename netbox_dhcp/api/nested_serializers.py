from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from netbox_dhcp.models import (
    ClientClass,
    DHCPServer,
    HostReservation,
    PDPool,
    Pool,
    SharedNetwork,
    Subnet,
)

__all__ = (
    "NestedDHCPServerSerializer",
    "NestedClientClassSerializer",
    "NestedSubnetSerializer",
    "NestedSharedNetworkSerializer",
    "NestedPoolSerializer",
    "NestedPDPoolSerializer",
    "NestedHostReservationSerializer",
)


class NestedDHCPServerSerializer(WritableNestedSerializer):
    class Meta:
        model = DHCPServer

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "status",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:dhcpcluster-detail"
    )


class NestedClientClassSerializer(WritableNestedSerializer):
    class Meta:
        model = ClientClass

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "weight",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:clientclass-detail"
    )


class NestedSubnetSerializer(WritableNestedSerializer):
    class Meta:
        model = Subnet

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "weight",
            "prefix",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:subnet-detail"
    )


class NestedSharedNetworkSerializer(WritableNestedSerializer):
    class Meta:
        model = SharedNetwork

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "weight",
            "prefix",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:sharednetwork-detail"
    )


class NestedPoolSerializer(WritableNestedSerializer):
    class Meta:
        model = Pool

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "weight",
            "ip_range",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:pool-detail"
    )


class NestedPDPoolSerializer(WritableNestedSerializer):
    class Meta:
        model = PDPool

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "weight",
            "prefix",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:pdpool-detail"
    )


class NestedHostReservationSerializer(WritableNestedSerializer):
    class Meta:
        model = HostReservation

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "duid",
            "hw_address",
            "circuit_id",
            "client_id",
            "flex_id",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:hostreservation-detail"
    )
