from rest_framework import serializers

from ipam.api.serializers import PrefixSerializer
from netbox.api.serializers import PrimaryModelSerializer
from netbox_dhcp.models import SharedNetwork

from ..nested_serializers import NestedSubnetSerializer
from .dhcp_server import DHCPServerSerializer
from .mixins import (
    ClientClassSerializerMixin,
    EvaluateClientClassSerializerMixin,
)
from .option import OptionSerializer

__all__ = ("SharedNetworkSerializer",)


class SharedNetworkSerializer(
    ClientClassSerializerMixin,
    EvaluateClientClassSerializerMixin,
    PrimaryModelSerializer,
):
    class Meta:
        model = SharedNetwork

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "comments",
            "weight",
            "dhcp_server",
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
            "child_subnets",
            "options",
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
        view_name="plugins-api:netbox_dhcp-api:sharednetwork-detail"
    )

    dhcp_server = DHCPServerSerializer(
        nested=True,
        read_only=False,
        required=True,
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

    child_subnets = NestedSubnetSerializer(
        many=True,
        read_only=False,
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

        shared_network = super().create(validated_data)

        if client_classes is not None:
            shared_network.client_classes.set(client_classes)
        if evaluate_additional_classes is not None:
            shared_network.evaluate_additional_classes.set(evaluate_additional_classes)

        return shared_network

    def update(self, instance, validated_data):
        client_classes = validated_data.pop("client_classes", None)
        evaluate_additional_classes = validated_data.pop(
            "evaluate_additional_classes", None
        )

        shared_network = super().update(instance, validated_data)

        if client_classes is not None:
            shared_network.client_classes.set(client_classes)
        if evaluate_additional_classes is not None:
            shared_network.evaluate_additional_classes.set(evaluate_additional_classes)

        return shared_network
