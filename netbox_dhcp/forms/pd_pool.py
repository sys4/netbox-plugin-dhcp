from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelBulkEditForm,
)
from utilities.forms.fields import (
    TagFilterField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    CSVModelChoiceField,
)
from ipam.models import Prefix
from ipam.choices import IPAddressFamilyChoices
from utilities.forms.rendering import FieldSet
from utilities.forms import get_field_value

from netbox_dhcp.models import PDPool, Subnet

from .mixins import (
    ClientClassBulkEditFormMixin,
    ClientClassFilterFormMixin,
    ClientClassFormMixin,
    ClientClassImportFormMixin,
    EvaluateClientClassBulkEditFormMixin,
    EvaluateClientClassFilterFormMixin,
    EvaluateClientClassFormMixin,
    EvaluateClientClassImportFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    NetBoxDHCPFilterFormMixin,
)

from .mixins.model import DYNAMIC_ATTRIBUTES

__all__ = (
    "PDPoolForm",
    "PDPoolFilterForm",
    "PDPoolImportForm",
    "PDPoolBulkEditForm",
)


class PDPoolForm(
    ClientClassFormMixin,
    EvaluateClientClassFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = PDPool

        fields = (
            "name",
            "description",
            "weight",
            "subnet",
            "prefix",
            "delegated_length",
            "excluded_prefix",
            *ClientClassFormMixin.FIELDS,
            *EvaluateClientClassFormMixin.FIELDS,
            "tags",
        )

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "weight",
            "subnet",
            "prefix",
            "delegated_length",
            "excluded_prefix",
            name=_("Prefix Delegation Pool"),
        ),
        FieldSet(
            *ClientClassFormMixin.FIELDS,
            *EvaluateClientClassFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["prefix"].widget.attrs.update(DYNAMIC_ATTRIBUTES)

        if prefix_id := get_field_value(self, "prefix"):
            prefix = (
                Prefix.objects.filter(pk=prefix_id)
                .values_list("prefix", flat=True)
                .first()
            )
            self.fields["excluded_prefix"].widget.add_query_param("within", str(prefix))

    subnet = DynamicModelChoiceField(
        queryset=Subnet.objects.filter(
            prefix__prefix__family=IPAddressFamilyChoices.FAMILY_6
        ),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        context={
            "description": "prefix_display",
        },
        required=True,
        selector=True,
        label=_("Subnet"),
    )
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        context={
            "depth": None,
        },
        required=True,
        selector=True,
        label=_("IPv6 Prefix"),
    )
    excluded_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        context={
            "depth": None,
        },
        required=False,
        selector=True,
        label=_("Excluded IPv6 Prefix"),
    )


class PDPoolFilterForm(
    NetBoxDHCPFilterFormMixin,
    ClientClassFilterFormMixin,
    EvaluateClientClassFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = PDPool

    fieldsets = (
        FieldSet(
            "q",
            "filter_id",
            "tag",
        ),
        FieldSet(
            "owner_group_id",
            "owner_id",
            name=_("Ownership"),
        ),
        FieldSet(
            "name",
            "description",
            "weight",
            "subnet_id",
            "prefix_id",
            "delegated_length",
            "excluded_prefix_id",
            name=_("Prefix Delegation Pool"),
        ),
        FieldSet(
            *ClientClassFilterFormMixin.FIELDS,
            *EvaluateClientClassFilterFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )

    subnet_id = DynamicModelMultipleChoiceField(
        queryset=Subnet.objects.filter(
            prefix__prefix__family=IPAddressFamilyChoices.FAMILY_6
        ),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        context={
            "description": "prefix_display",
        },
        required=False,
        label=_("Subnet"),
    )
    prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        context={
            "depth": None,
        },
        required=False,
        label=_("IPv6 Prefix"),
    )
    delegated_length = forms.IntegerField(
        required=False,
        label=_("Delegated Length"),
    )
    excluded_prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        context={
            "depth": None,
        },
        required=False,
        label=_("Excluded IPv6 Prefix"),
    )

    tag = TagFilterField(PDPool)


class PDPoolImportForm(
    ClientClassImportFormMixin,
    EvaluateClientClassImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = PDPool

        fields = (
            "name",
            "description",
            "weight",
            "subnet",
            "prefix",
            "delegated_length",
            "excluded_prefix",
            *ClientClassImportFormMixin.FIELDS,
            *EvaluateClientClassImportFormMixin.FIELDS,
            "comments",
            "tags",
        )

    subnet = CSVModelChoiceField(
        queryset=Subnet.objects.filter(
            prefix__prefix__family=IPAddressFamilyChoices.FAMILY_6
        ),
        required=True,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("Subnet %(value)s not found"),
        },
        label=_("Subnet"),
    )
    prefix = CSVModelChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        required=True,
        to_field_name="prefix",
        error_messages={
            "invalid_choice": _("IPv6 prefix %(value)s not found"),
        },
        label=_("IPv6 Prefix"),
    )
    excluded_prefix = CSVModelChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        required=False,
        to_field_name="prefix",
        error_messages={
            "invalid_choice": _("IPv6 prefix %(value)s not found"),
        },
        label=_("Excluded IPv6 Prefix"),
    )


class PDPoolBulkEditForm(
    NetBoxDHCPBulkEditFormMixin,
    ClientClassBulkEditFormMixin,
    EvaluateClientClassBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = PDPool

    fieldsets = (
        FieldSet(
            "description",
            "weight",
            "subnet",
            "delegated_length",
            name=_("Prefix Delegation Pool"),
        ),
        FieldSet(
            *ClientClassBulkEditFormMixin.FIELDS,
            *EvaluateClientClassBulkEditFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    nullable_fields = (
        "description",
        "excluded_prefix",
        *ClientClassBulkEditFormMixin.NULLABLE_FIELDS,
        *EvaluateClientClassBulkEditFormMixin.NULLABLE_FIELDS,
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )
    subnet = DynamicModelChoiceField(
        queryset=Subnet.objects.filter(
            prefix__prefix__family=IPAddressFamilyChoices.FAMILY_6
        ),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        context={
            "description": "prefix_display",
        },
        required=False,
        label=_("Subnet"),
    )
    delegated_length = forms.CharField(
        required=False,
        label=_("Delegated Length"),
    )
    excluded_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        query_params={
            "family": IPAddressFamilyChoices.FAMILY_6,
        },
        required=False,
        label=_("Excluded IPv6 Prefix"),
    )
