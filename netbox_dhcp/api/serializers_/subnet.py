from rest_framework import serializers

from ipam.api.serializers import PrefixSerializer
from netbox.api.serializers import PrimaryModelSerializer
from netbox_dhcp.models import Subnet

from ..nested_serializers import (
    NestedHostReservationSerializer,
    NestedPDPoolSerializer,
    NestedPoolSerializer,
)
from .dhcp_server import DHCPServerSerializer
from .mixins import (
    ClientClassSerializerMixin,
    EvaluateClientClassSerializerMixin,
)
from .option import OptionSerializer
from .shared_network import SharedNetworkSerializer

__all__ = ("SubnetSerializer",)


class SubnetSerializer(
    ClientClassSerializerMixin,
    EvaluateClientClassSerializerMixin,
    PrimaryModelSerializer,
):
    class Meta:
        model = Subnet

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "comments",
            "weight",
            "subnet_id",
            "dhcp_server",
            "shared_network",
            "child_pools",
            "child_pd_pools",
            "child_host_reservations",
            "options",
            "prefix",
            "prefix_display",
            "next_server",
            "server_hostname",
            "boot_file_name",
            "offer_lifetime",
            "valid_lifetime",
            "min_valid_lifetime",
            "max_valid_lifetime",
            "preferred_lifetime",
            "min_preferred_lifetime",
            "max_preferred_lifetime",
            "client_classes",
            "evaluate_additional_classes",
            "renew_timer",
            "rebind_timer",
            "match_client_id",
            "authoritative",
            "reservations_global",
            "reservations_out_of_pool",
            "reservations_in_subnet",
            "calculate_tee_times",
            "t1_percent",
            "t2_percent",
            "cache_threshold",
            "cache_max_age",
            "adaptive_lease_time_threshold",
            "store_extended_info",
            "allocator",
            "pd_allocator",
            "relay",
            "interface_id",
            "rapid_commit",
            "hostname_char_set",
            "hostname_char_replacement",
            "ddns_send_updates",
            "ddns_override_no_update",
            "ddns_override_client_update",
            "ddns_replace_client_name",
            "ddns_generated_prefix",
            "ddns_qualifying_suffix",
            "ddns_update_on_renew",
            "ddns_conflict_resolution_mode",
            "ddns_ttl_percent",
            "ddns_ttl",
            "ddns_ttl_min",
            "ddns_ttl_max",
            "tags",
        )

        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "weight",
            "prefix_display",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:subnet-detail"
    )

    dhcp_server = DHCPServerSerializer(
        nested=True,
        read_only=False,
        required=False,
    )
    shared_network = SharedNetworkSerializer(
        nested=True,
        read_only=False,
        required=False,
    )
    prefix = PrefixSerializer(
        nested=True,
        read_only=False,
        required=True,
    )
    prefix_display = serializers.CharField(
        required=False,
        read_only=True,
    )

    child_pd_pools = NestedPDPoolSerializer(
        many=True,
        read_only=True,
        required=False,
    )
    child_pools = NestedPoolSerializer(
        many=True,
        read_only=True,
        required=False,
    )
    child_host_reservations = NestedHostReservationSerializer(
        many=True,
        read_only=True,
        required=False,
    )
    options = OptionSerializer(
        nested=True,
        many=True,
        read_only=True,
        required=False,
    )

    def create(self, validated_data):
        client_classes = validated_data.pop("client_classes", None)
        evaluate_additional_classes = validated_data.pop(
            "evaluate_additional_classes", None
        )

        subnet = super().create(validated_data)

        if client_classes is not None:
            subnet.client_classes.set(client_classes)
        if evaluate_additional_classes is not None:
            subnet.evaluate_additional_classes.set(evaluate_additional_classes)

        return subnet

    def update(self, instance, validated_data):
        client_classes = validated_data.pop("client_classes", None)
        evaluate_additional_classes = validated_data.pop(
            "evaluate_additional_classes", None
        )

        subnet = super().update(instance, validated_data)

        if client_classes is not None:
            subnet.client_classes.set(client_classes)
        if evaluate_additional_classes is not None:
            subnet.evaluate_additional_classes.set(evaluate_additional_classes)

        return subnet
