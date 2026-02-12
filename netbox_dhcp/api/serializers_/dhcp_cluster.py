from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from netbox.api.serializers import PrimaryModelSerializer

from netbox_dhcp.models import DHCPCluster

from ..nested_serializers import NestedDHCPServerSerializer

__all__ = ("DHCPClusterSerializer",)


class DHCPClusterSerializer(PrimaryModelSerializer):
    class Meta:
        model = DHCPCluster

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "comments",
            "status",
            "dhcp_servers",
        )

        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "status",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:dhcpcluster-detail"
    )

    dhcp_servers = NestedDHCPServerSerializer(
        many=True,
        read_only=True,
        required=False,
        help_text=_("DHCP servers assigned to the cluster"),
    )
