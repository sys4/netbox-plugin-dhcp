from django.utils.translation import gettext as _
from rest_framework import serializers

from netbox.api.serializers import PrimaryModelSerializer
from netbox_dhcp.models import OptionDefinition

from .client_class import ClientClassSerializer
from .mixins import DHCPServerSerializerMixin

__all__ = ("OptionDefinitionSerializer",)


class OptionDefinitionSerializer(
    DHCPServerSerializerMixin,
    PrimaryModelSerializer
):
    class Meta:
        model = OptionDefinition

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "dhcp_server",
            "client_class",
            "family",
            "space",
            "name",
            "description",
            "comments",
            "code",
            "type",
            "record_types",
            "encapsulate",
            "array",
            "standard",
        )

        brief_fields = (
            "id",
            "url",
            "display",
            "family",
            "space",
            "name",
            "code",
            "description",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:optiondefinition-detail"
    )

    client_class = ClientClassSerializer(
        nested=True,
        read_only=False,
        required=False,
        help_text=_("Client class this option definition is assigned to"),
    )
