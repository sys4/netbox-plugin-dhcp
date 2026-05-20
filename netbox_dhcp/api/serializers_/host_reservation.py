from django.utils.translation import gettext as _
from rest_framework import serializers

from ipam.api.serializers import IPAddressSerializer, PrefixSerializer
from netbox.api.serializers import PrimaryModelSerializer
from netbox_dhcp.models import HostReservation

from .mixins import ClientClassSerializerMixin
from .option import OptionSerializer

__all__ = ("HostReservationSerializer",)


class HostReservationSerializer(
    ClientClassSerializerMixin,
    PrimaryModelSerializer,
):
    class Meta:
        model = HostReservation

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "comments",
            "dhcp_server",
            "subnet",
            "duid",
            "hw_address",
            "circuit_id",
            "client_id",
            "flex_id",
            "next_server",
            "server_hostname",
            "boot_file_name",
            "hostname",
            "ipv4_address",
            "ipv6_addresses",
            "ipv6_prefixes",
            "excluded_ipv6_prefixes",
            "client_classes",
            "options",
        )

        brief_fields = (
            "id",
            "url",
            "display",
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

    ipv4_address = IPAddressSerializer(
        nested=True,
        read_only=False,
        required=False,
        help_text=_("IPAM IPv4 Address assigned by the host reservation"),
    )
    ipv6_addresses = IPAddressSerializer(
        many=True,
        nested=True,
        read_only=False,
        required=False,
        help_text=_("IPAM IPv6 Addresses assigned by the host reservation"),
    )
    ipv6_prefixes = PrefixSerializer(
        many=True,
        nested=True,
        read_only=False,
        required=False,
        help_text=_("IPAM IPv6 Prefixes assigned by the host reservation"),
    )
    excluded_ipv6_prefixes = PrefixSerializer(
        many=True,
        nested=True,
        read_only=False,
        required=False,
        help_text=_("IPAM IPv6 Prefixes excluded by the host reservation"),
    )
    options = OptionSerializer(
        nested=True,
        many=True,
        read_only=True,
        required=False,
    )

    def create(self, validated_data):
        client_classes = validated_data.pop("client_classes", None)
        ipv6_addresses = validated_data.pop("ipv6_addresses", None)
        ipv6_prefixes = validated_data.pop("ipv6_prefixes", None)
        excluded_ipv6_prefixes = validated_data.pop("excluded_ipv6_prefixes", None)

        host_reservation = super().create(validated_data)

        if client_classes is not None:
            host_reservation.client_classes.set(client_classes)
        if ipv6_addresses is not None:
            host_reservation.ipv6_addresses.set(ipv6_addresses)
        if ipv6_prefixes is not None:
            host_reservation.ipv6_prefixes.set(ipv6_prefixes)
        if excluded_ipv6_prefixes is not None:
            host_reservation.excluded_ipv6_prefixes.set(excluded_ipv6_prefixes)

        return host_reservation

    def update(self, instance, validated_data):
        client_classes = validated_data.pop("client_classes", None)
        ipv6_addresses = validated_data.pop("ipv6_addresses", None)
        ipv6_prefixes = validated_data.pop("ipv6_prefixes", None)
        excluded_ipv6_prefixes = validated_data.pop("excluded_ipv6_prefixes", None)

        host_reservation = super().update(instance, validated_data)

        if client_classes is not None:
            host_reservation.client_classes.set(client_classes)
        if ipv6_addresses is not None:
            host_reservation.ipv6_addresses.set(ipv6_addresses)
        if ipv6_prefixes is not None:
            host_reservation.ipv6_prefixes.set(ipv6_prefixes)
        if excluded_ipv6_prefixes is not None:
            host_reservation.excluded_ipv6_prefixes.set(excluded_ipv6_prefixes)

        return host_reservation
