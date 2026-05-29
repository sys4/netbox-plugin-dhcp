from rest_framework import serializers

from ipam.api.serializers import PrefixSerializer
from netbox.api.serializers import PrimaryModelSerializer
from netbox_dhcp.models import PDPool

from .mixins import (
    ClientClassSerializerMixin,
    EvaluateClientClassSerializerMixin,
)
from .option import OptionSerializer
from .subnet import SubnetSerializer

__all__ = ("PDPoolSerializer",)


class PDPoolSerializer(
    ClientClassSerializerMixin,
    EvaluateClientClassSerializerMixin,
    PrimaryModelSerializer,
):
    class Meta:
        model = PDPool

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "name",
            "description",
            "comments",
            "weight",
            "subnet",
            "prefix",
            "prefix_display",
            "delegated_length",
            "excluded_prefix",
            "client_classes",
            "evaluate_additional_classes",
            "options",
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
            "delegated_length",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:pdpool-detail"
    )

    subnet = SubnetSerializer(
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
    excluded_prefix = PrefixSerializer(
        nested=True,
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

        pd_pool = super().create(validated_data)

        if client_classes is not None:
            pd_pool.client_classes.set(client_classes)
        if evaluate_additional_classes is not None:
            pd_pool.evaluate_additional_classes.set(evaluate_additional_classes)

        return pd_pool

    def update(self, instance, validated_data):
        client_classes = validated_data.pop("client_classes", None)
        evaluate_additional_classes = validated_data.pop(
            "evaluate_additional_classes", None
        )

        pd_pool = super().update(instance, validated_data)

        if client_classes is not None:
            pd_pool.client_classes.set(client_classes)
        if evaluate_additional_classes is not None:
            pd_pool.evaluate_additional_classes.set(evaluate_additional_classes)

        return pd_pool
