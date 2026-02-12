from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from netbox.api.serializers import PrimaryModelSerializer
from netbox.api.fields import ContentTypeField
from utilities.api import get_serializer_for_model

from netbox_dhcp.models import Option
from netbox_dhcp.choices import OptionSendChoices

from .mixins import ClientClassSerializerMixin

__all__ = ("OptionSerializer",)


OPTION_ASSIGNMENT_MODELS = Q(
    app_label="netbox_dhcp",
    model__in=[
        "dhcpserver",
        "subnet",
        "sharednetwork",
        "pool",
        "pdpool",
        "hostresevration",
        "clientclass",
    ],
)


class OptionSerializer(
    ClientClassSerializerMixin,
    PrimaryModelSerializer,
):
    class Meta:
        model = Option

        fields = (
            "id",
            "url",
            "display",
            "display_url",
            "definition",
            "name",
            "description",
            "comments",
            "space",
            "code",
            "data",
            "weight",
            "csv_format",
            "send_option",
            "always_send",
            "never_send",
            "client_classes",
            "assigned_object",
            "assigned_object_id",
            "assigned_object_type",
        )

        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "space",
            "code",
            "weight",
            "data",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dhcp-api:option-detail"
    )

    name = serializers.SerializerMethodField(
        read_only=True,
    )
    space = serializers.SerializerMethodField(
        read_only=True,
    )
    code = serializers.SerializerMethodField(
        read_only=True,
    )
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(OPTION_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True,
    )
    assigned_object = serializers.SerializerMethodField(
        read_only=True,
    )
    always_send = serializers.SerializerMethodField(
        read_only=True,
    )
    never_send = serializers.SerializerMethodField(
        read_only=True,
    )

    def get_name(self, instance):
        return instance.definition.name

    def get_space(self, instance):
        return instance.definition.space

    def get_code(self, instance):
        return instance.definition.code

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, instance):
        if instance.assigned_object is None:
            return None
        serializer = get_serializer_for_model(instance.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(instance.assigned_object, nested=True, context=context).data

    def get_always_send(self, instance):
        if instance.send_option is not None:
            return instance.send_option == OptionSendChoices.ALWAYS_SEND

    def get_never_send(self, instance):
        if instance.send_option is not None:
            return instance.send_option == OptionSendChoices.NEVER_SEND

    def create(self, validated_data):
        client_classes = validated_data.pop("client_classes", None)

        option = super().create(validated_data)

        if client_classes is not None:
            option.client_classes.set(client_classes)

        return option

    def update(self, instance, validated_data):
        client_classes = validated_data.pop("client_classes", None)

        option = super().update(instance, validated_data)

        if client_classes is not None:
            option.client_classes.set(client_classes)

        return option
