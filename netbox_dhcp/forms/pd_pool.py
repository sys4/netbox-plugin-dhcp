from django import forms
from django.utils.translation import gettext_lazy as _

from ipam.choices import IPAddressFamilyChoices
from ipam.models import Prefix
from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelForm,
    PrimaryModelImportForm,
)
from netbox_dhcp.models import PDPool, Subnet
from utilities.forms import get_field_value
from utilities.forms.fields import (
    CSVModelChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet

from .mixins import (
    ClientClassesBulkEditFormMixin,
    ClientClassesFilterFormMixin,
    ClientClassesFormMixin,
    ClientClassesImportFormMixin,
    EvaluateClientClassesBulkEditFormMixin,
    EvaluateClientClassesFilterFormMixin,
    EvaluateClientClassesFormMixin,
    EvaluateClientClassesImportFormMixin,
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
    ClientClassesFormMixin,
    EvaluateClientClassesFormMixin,
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
            *ClientClassesFormMixin.FIELDS,
            *EvaluateClientClassesFormMixin.FIELDS,
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
            *ClientClassesFormMixin.FIELDS,
            *EvaluateClientClassesFormMixin.FIELDS,
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
    ClientClassesFilterFormMixin,
    EvaluateClientClassesFilterFormMixin,
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
            *ClientClassesFilterFormMixin.FIELDS,
            *EvaluateClientClassesFilterFormMixin.FIELDS,
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
    ClientClassesImportFormMixin,
    EvaluateClientClassesImportFormMixin,
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
            *ClientClassesImportFormMixin.FIELDS,
            *EvaluateClientClassesImportFormMixin.FIELDS,
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
    ClientClassesBulkEditFormMixin,
    EvaluateClientClassesBulkEditFormMixin,
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
            *ClientClassesBulkEditFormMixin.FIELDS,
            *EvaluateClientClassesBulkEditFormMixin.FIELDS,
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
        *ClientClassesBulkEditFormMixin.NULLABLE_FIELDS,
        *EvaluateClientClassesBulkEditFormMixin.NULLABLE_FIELDS,
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
