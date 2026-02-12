from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.forms import SimpleArrayField

from netbox.forms import (
    PrimaryModelForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelBulkEditForm,
)
from utilities.forms.fields import (
    TagFilterField,
    CSVChoiceField,
    CSVMultipleChoiceField,
)
from utilities.forms.rendering import FieldSet
from utilities.forms import (
    get_field_value,
    add_blank_choice,
    BOOLEAN_WITH_BLANK_CHOICES,
)
from utilities.forms.widgets import HTMXSelect
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import OptionDefinition
from netbox_dhcp.choices import OptionTypeChoices, OptionSpaceChoices

from .mixins import (
    NetBoxDHCPFilterFormMixin,
    NetBoxDHCPBulkEditFormMixin,
)

__all__ = (
    "OptionDefinitionForm",
    "OptionDefinitionFilterForm",
    "OptionDefinitionImportForm",
    "OptionDefinitionBulkEditForm",
)


class OptionDefinitionForm(PrimaryModelForm):
    class Meta:
        model = OptionDefinition

        fields = (
            "description",
            "dhcp_server",
            "client_class",
            "family",
            "space",
            "name",
            "code",
            "type",
            "record_types",
            "encapsulate",
            "array",
        )

        widgets = {
            "type": HTMXSelect(),
            "dhcp_server": forms.HiddenInput(),
            "client_class": forms.HiddenInput(),
        }

    fieldsets = (
        FieldSet(
            "family",
            "space",
            "name",
            "code",
            "description",
            "type",
            "record_types",
            "encapsulate",
            "array",
            name=_("Option Definition"),
        ),
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if get_field_value(self, "type") != OptionTypeChoices.TYPE_RECORD:
            del self.fields["record_types"]

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        if self.cleaned_data.get("type") != OptionTypeChoices.TYPE_RECORD:
            self.cleaned_data["record_types"] = None

    record_types = SimpleArrayField(
        label=_("Record Types"),
        help_text=_(
            "Valid Types: {}".format(
                ", ".join(
                    sorted(
                        type
                        for type in OptionTypeChoices.values()
                        if type
                        not in [
                            OptionTypeChoices.TYPE_EMPTY,
                            OptionTypeChoices.TYPE_RECORD,
                        ]
                    )
                )
            )
        ),
        base_field=forms.ChoiceField(
            choices=OptionTypeChoices,
        ),
        required=False,
    )
    array = forms.NullBooleanField(
        label=_("Array"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )


class OptionDefinitionFilterForm(
    NetBoxDHCPFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = OptionDefinition

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
            "family",
            "space",
            "name",
            "description",
            "code",
            "type",
            "record_types",
            "encapsulate",
            "array",
            name=_("Option Definition"),
        ),
    )

    family = forms.ChoiceField(
        label=_("Address Family"),
        choices=add_blank_choice(IPAddressFamilyChoices),
        required=False,
    )
    space = forms.MultipleChoiceField(
        label=_("Space"),
        choices=OptionSpaceChoices,
        required=False,
    )
    code = forms.IntegerField(
        label=_("Code"),
        min_value=1,
        max_value=255,
        required=False,
    )
    type = forms.MultipleChoiceField(
        label=_("Type"),
        choices=OptionTypeChoices,
        required=False,
    )
    record_types = forms.MultipleChoiceField(
        label=_("Record Types"),
        choices=OptionTypeChoices,
        required=False,
    )
    encapsulate = forms.CharField(
        label=_("Encapsulate"),
        required=False,
    )
    array = forms.NullBooleanField(
        label=_("Array"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(OptionDefinition)


class OptionDefinitionImportForm(PrimaryModelImportForm):
    class Meta:
        model = OptionDefinition

        fields = (
            "family",
            "space",
            "name",
            "description",
            "code",
            "type",
            "record_types",
            "encapsulate",
            "array",
            "comments",
            "tags",
        )

    family = CSVChoiceField(
        choices=IPAddressFamilyChoices,
        required=False,
        label=_("Address Family"),
    )
    space = CSVChoiceField(
        choices=OptionSpaceChoices,
        required=False,
        label=_("Space"),
    )
    type = CSVChoiceField(
        choices=OptionTypeChoices,
        required=False,
        label=_("Type"),
    )
    record_types = CSVMultipleChoiceField(
        choices=OptionTypeChoices,
        required=False,
        label=_("Recoed Types"),
    )


class OptionDefinitionBulkEditForm(
    NetBoxDHCPBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = OptionDefinition

    fieldsets = (
        FieldSet(
            "family",
            "space",
            "name",
            "description",
            "code",
            "type",
            "record_types",
            "encapsulate",
            "array",
            name=_("Option Definition"),
        ),
    )

    nullable_fields = ("description",)

    family = forms.ChoiceField(
        label=_("Address Family"),
        choices=add_blank_choice(IPAddressFamilyChoices),
        required=False,
    )
    space = forms.ChoiceField(
        label=_("Space"),
        choices=add_blank_choice(OptionSpaceChoices),
        required=False,
    )
    code = forms.IntegerField(
        label=_("Code"),
        min_value=1,
        max_value=255,
        required=False,
    )
    type = forms.ChoiceField(
        label=_("Type"),
        choices=add_blank_choice(OptionTypeChoices),
        required=False,
    )
    record_types = SimpleArrayField(
        label=_("Record Types"),
        help_text=_(
            "Valid Types: {}".format(
                ", ".join(
                    sorted(
                        type
                        for type in OptionTypeChoices.values()
                        if type
                        not in [
                            OptionTypeChoices.TYPE_EMPTY,
                            OptionTypeChoices.TYPE_RECORD,
                        ]
                    )
                )
            )
        ),
        base_field=forms.ChoiceField(
            choices=OptionTypeChoices,
        ),
        required=False,
    )
    encapsulate = forms.CharField(
        label=_("Encapsulate"),
        required=False,
    )
    array = forms.NullBooleanField(
        label=_("Array"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
