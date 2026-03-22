from rest_framework import serializers

from netbox.api.serializers import PrimaryModelSerializer

from netbox_dhcp.models import ClientClass

from .option import OptionSerializer
from .dhcp_server import DHCPServerSerializer

__all__ = ("ClientClassSerializer",)


class ClientClassSerializer(PrimaryModelSerializer):
    class Meta:
        model = ClientClass

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "comments",
            "dhcp_server",
            "weight",
            "test",
            "template_test",
            "only_in_additional_list",
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
            "options",
        )

        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "weight",
            "test",
            "template_test",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:clientclass-detail"
    )

    dhcp_server = DHCPServerSerializer(
        nested=True,
        read_only=False,
        required=True,
    )
    options = OptionSerializer(
        nested=True,
        many=True,
        read_only=True,
        required=False,
    )
