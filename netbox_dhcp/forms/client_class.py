from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelBulkEditForm,
)
from utilities.forms.fields import TagFilterField
from utilities.forms.rendering import FieldSet
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES

from netbox_dhcp.models import ClientClass
from .mixins import (
    DHCPServerFormMixin,
    DHCPServerFilterFormMixin,
    DHCPServerImportFormMixin,
    DHCPServerBulkEditFormMixin,
    BOOTPFormMixin,
    BOOTPFilterFormMixin,
    BOOTPImportFormMixin,
    BOOTPBulkEditFormMixin,
    LifetimeFormMixin,
    LifetimeFilterFormMixin,
    LifetimeImportFormMixin,
    LifetimeBulkEditFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    NetBoxDHCPFilterFormMixin,
)

__all__ = (
    "ClientClassForm",
    "ClientClassFilterForm",
    "ClientClassImportForm",
    "ClientClassBulkEditForm",
)


class ClientClassForm(
    DHCPServerFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = ClientClass

        fields = (
            "name",
            "description",
            "weight",
            *DHCPServerFormMixin.FIELDS,
            "test",
            "template_test",
            "only_in_additional_list",
            *BOOTPFormMixin.FIELDS,
            *LifetimeFormMixin.FIELDS,
            "tags",
        )

        widgets = {
            "test": forms.Textarea(attrs={"rows": 2}),
            "template_test": forms.Textarea(attrs={"rows": 2}),
        }

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "weight",
            *DHCPServerFormMixin.FIELDS,
            "test",
            "template_test",
            "only_in_additional_list",
            name=_("Client Class"),
        ),
        BOOTPFormMixin.FIELDSET,
        LifetimeFormMixin.FIELDSET,
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    only_in_additional_list = forms.NullBooleanField(
        required=False,
        label=_("Only in additional list"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )


class ClientClassFilterForm(
    NetBoxDHCPFilterFormMixin,
    DHCPServerFilterFormMixin,
    BOOTPFilterFormMixin,
    LifetimeFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = ClientClass

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
            *DHCPServerFilterFormMixin.FIELDS,
            "test",
            "template_test",
            "only_in_additional_list",
            name=_("Client Class"),
        ),
        BOOTPFilterFormMixin.FIELDSET,
        LifetimeFilterFormMixin.FIELDSET,
    )

    weight = forms.IntegerField(
        label=_("Weight"),
        required=False,
    )
    test = forms.CharField(
        required=False,
        label=_("Test"),
    )
    template_test = forms.CharField(
        required=False,
        label=_("Template Test"),
    )
    only_in_additional_list = forms.NullBooleanField(
        required=False,
        label=_("Only in additional list"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(ClientClass)


class ClientClassImportForm(
    DHCPServerImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = ClientClass

        fields = (
            "name",
            "description",
            "weight",
            *DHCPServerImportFormMixin.FIELDS,
            "test",
            "template_test",
            "only_in_additional_list",
            *BOOTPImportFormMixin.FIELDS,
            *LifetimeImportFormMixin.FIELDS,
            "comments",
            "tags",
        )


class ClientClassBulkEditForm(
    NetBoxDHCPBulkEditFormMixin,
    DHCPServerBulkEditFormMixin,
    BOOTPBulkEditFormMixin,
    LifetimeBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = ClientClass

    fieldsets = (
        FieldSet(
            "description",
            "weight",
            *DHCPServerBulkEditFormMixin.FIELDS,
            name=_("Client Class"),
        ),
        FieldSet(
            "test",
            "template_test",
            "only_in_additional_list",
            name=_("Selection"),
        ),
        BOOTPBulkEditFormMixin.FIELDSET,
        LifetimeBulkEditFormMixin.FIELDSET,
    )

    nullable_fields = (
        "description",
        "test",
        "template_test",
        *BOOTPBulkEditFormMixin.NULLABLE_FIELDS,
        *LifetimeBulkEditFormMixin.NULLABLE_FIELDS,
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )
    test = forms.CharField(
        required=False,
        label=_("Test"),
        widget=forms.Textarea(attrs={"rows": 2}),
    )
    template_test = forms.CharField(
        required=False,
        label=_("Template Test"),
        widget=forms.Textarea(attrs={"rows": 2}),
    )
    only_in_additional_list = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
        label=_("Only in additional list"),
    )
