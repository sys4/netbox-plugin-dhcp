from django.utils.translation import gettext as _

from netbox.api.serializers import PrimaryModelSerializer

from ..nested_serializers import (
    NestedClientClassSerializer,
)

__all__ = (
    "ClientClassSerializerMixin",
    "EvaluateClientClassSerializerMixin",
    "DHCPServerSerializerMixin",
    "SubnetSerializerMixin",
)


class ClientClassSerializerMixin(PrimaryModelSerializer):
    client_classes = NestedClientClassSerializer(
        many=True,
        read_only=False,
        required=False,
        help_text=_("Client Classes"),
    )


class EvaluateClientClassSerializerMixin(PrimaryModelSerializer):
    evaluate_additional_classes = NestedClientClassSerializer(
        many=True,
        read_only=False,
        required=False,
        help_text=_("Client classes to evaluate after matching"),
    )


class DHCPServerSerializerMixin(PrimaryModelSerializer):
    dhcp_server = NestedDHCPServerSerializer(
        read_only=False,
        required=False,
        help_text=_("DHCP server the object is assigned to"),
    )


class SubnetSerializerMixin(PrimaryModelSerializer):
    subnet = NestedSubnetSerializer(
        nested=True,
        read_only=False,
        required=False,
        help_text=_("Subnet the object is assigned to"),
    )
