from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelBulkEditForm,
)
from utilities.forms.fields import TagFilterField, CSVModelChoiceField, CSVChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms import add_blank_choice, BOOLEAN_WITH_BLANK_CHOICES
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import (
    Option,
    OptionDefinition,
    DHCPServer,
    Subnet,
    SharedNetwork,
    Pool,
    PDPool,
    HostReservation,
    ClientClass,
)
from netbox_dhcp.choices import OptionSpaceChoices, OptionSendChoices

from .mixins import (
    ClientClassFormMixin,
    ClientClassImportFormMixin,
    ClientClassFilterFormMixin,
    ClientClassBulkEditFormMixin,
)

__all__ = (
    "OptionForm",
    "OptionFilterForm",
    "OptionImportForm",
    "OptionBulkEditForm",
)


class OptionForm(
    ClientClassFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = Option

        fields = (
            "definition",
            "description",
            "data",
            "weight",
            "csv_format",
            "send_option",
            "assigned_object_id",
            "assigned_object_type",
            *ClientClassFormMixin.FIELDS,
            "tags",
        )

        widgets = {
            "assigned_object_id": forms.HiddenInput(),
            "assigned_object_type": forms.HiddenInput(),
        }

    fieldsets = (
        FieldSet(
            "definition",
            "description",
            "data",
            "weight",
            "csv_format",
            "send_option",
            name=_("Option"),
        ),
        ClientClassFormMixin.FIELDSET,
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_object_id"].required = False
        self.fields["assigned_object_type"].required = False

    csv_format = forms.NullBooleanField(
        label=_("CSV Format"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )


class OptionFilterForm(
    ClientClassFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = Option

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
            "family",
            "space",
            "code",
            "definition_id",
            "data",
            "weight",
            "csv_format",
            "send_option",
            name=_("Option"),
        ),
        ClientClassFilterFormMixin.FIELDSET,
    )

    name = forms.CharField(
        label=_("Name"),
        required=False,
    )
    description = forms.CharField(
        label=_("Description"),
        required=False,
    )
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
    data = forms.CharField(
        label=_("Data"),
        required=False,
    )
    weight = forms.IntegerField(
        label=_("Weight"),
        required=False,
    )
    code = forms.IntegerField(
        label=_("Code"),
        min_value=1,
        max_value=255,
        required=False,
    )
    weight = forms.IntegerField(
        label=_("Weight"),
        min_value=0,
        max_value=32767,
        required=False,
    )
    csv_format = forms.NullBooleanField(
        label=_("CSV Format"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    send_option = forms.ChoiceField(
        label=_("Send Option"),
        choices=add_blank_choice(OptionSendChoices),
        required=False,
    )

    tag = TagFilterField(Option)


class OptionImportForm(
    ClientClassImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = Option

        fields = (
            "description",
            "definition",
            "space",
            "name",
            "code",
            "dhcp_server",
            "subnet",
            "shared_network",
            "pool",
            "pd_pool",
            "host_reservation",
            "client_class",
            "data",
            "weight",
            "csv_format",
            "send_option",
            *ClientClassImportFormMixin.FIELDS,
            "comments",
            "tags",
        )

    definition = CSVModelChoiceField(
        label=_("Definition"),
        queryset=OptionDefinition.objects.all(),
        required=False,
    )
    space = CSVChoiceField(
        label=_("Space"),
        choices=OptionSpaceChoices,
        required=True,
    )
    name = CSVModelChoiceField(
        label=_("Name"),
        queryset=OptionDefinition.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("No option definition with name %(value)s found"),
        },
    )
    code = CSVModelChoiceField(
        label=_("Code"),
        queryset=OptionDefinition.objects.all(),
        required=False,
        to_field_name="code",
        error_messages={
            "invalid_choice": _("No option definition with code %(value)s found"),
        },
        help_text=_("If code is present, name will be ignored"),
    )

    dhcp_server = CSVModelChoiceField(
        label=_("DHCP Server"),
        queryset=DHCPServer.objects.all(),
        to_field_name="name",
        required=False,
        error_messages={
            "invalid_choice": _("DHCP Server %(value)s not found"),
        },
        help_text=_(
            "Specify exactly one of dhcp_server, subnet, shared_network, "
            "pool, pd_pool, host_reservation or client_class per line"
        ),
    )
    subnet = CSVModelChoiceField(
        label=_("Subnet"),
        queryset=Subnet.objects.all(),
        to_field_name="name",
        required=False,
        error_messages={
            "invalid_choice": _("Subnet %(value)s not found"),
        },
        help_text=_(
            "Specify exactly one of dhcp_server, subnet, shared_network, "
            "pool, pd_pool, host_reservation or client_class per line"
        ),
    )
    shared_network = CSVModelChoiceField(
        label=_("Shared Network"),
        queryset=SharedNetwork.objects.all(),
        to_field_name="name",
        required=False,
        error_messages={
            "invalid_choice": _("Shared network %(value)s not found"),
        },
        help_text=_(
            "Specify exactly one of dhcp_server, subnet, shared_network, "
            "pool, pd_pool, host_reservation or client_class per line"
        ),
    )
    pool = CSVModelChoiceField(
        label=_("Pool"),
        queryset=Pool.objects.all(),
        to_field_name="name",
        required=False,
        error_messages={
            "invalid_choice": _("Pool %(value)s not found"),
        },
        help_text=_(
            "Specify exactly one of dhcp_server, subnet, shared_network, "
            "pool, pd_pool, host_reservation or client_class per line"
        ),
    )
    pd_pool = CSVModelChoiceField(
        label=_("Prefix Delegation Pool"),
        queryset=PDPool.objects.all(),
        to_field_name="name",
        required=False,
        error_messages={
            "invalid_choice": _("Prefix delegation pool %(value)s not found"),
        },
        help_text=_(
            "Specify exactly one of dhcp_server, subnet, shared_network, "
            "pool, pd_pool, host_reservation or client_class per line"
        ),
    )
    host_reservation = CSVModelChoiceField(
        label=_("Host Reservation"),
        queryset=HostReservation.objects.all(),
        to_field_name="name",
        required=False,
        error_messages={
            "invalid_choice": _("Host reservation %(value)s not found"),
        },
        help_text=_(
            "Specify exactly one of dhcp_server, subnet, shared_network, "
            "pool, pd_pool, host_reservation or client_class per line"
        ),
    )
    client_class = CSVModelChoiceField(
        label=_("Client Class"),
        queryset=ClientClass.objects.all(),
        to_field_name="name",
        required=False,
        error_messages={
            "invalid_choice": _("Client class %(value)s not found"),
        },
        help_text=_(
            "Specify exactly one of dhcp_server, subnet, shared_network, "
            "pool, pd_pool, host_reservation or client_class per line"
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_bound and "space" in self.data:
            self.fields["code"].queryset = OptionDefinition.objects.filter(
                space=self.data.get("space")
            )
            self.fields["name"].queryset = OptionDefinition.objects.filter(
                space=self.data.get("space")
            )

        del self.fields["definition"]

    def clean(self):
        super().clean()

        name = self.cleaned_data.get("name")
        code = self.cleaned_data.get("code")

        self.cleaned_data["definition"] = code if code else name

        objects = [
            self.cleaned_data.get(object_name)
            for object_name in (
                "dhcp_server",
                "subnet",
                "shared_network",
                "pool",
                "pd_pool",
                "host_reservation",
                "client_class",
            )
            if self.cleaned_data.get(object_name) is not None
        ]
        if len(objects) != 1:
            raise forms.ValidationError(_("Exactly one assigned object is required"))

        self.cleaned_data["assigned_object"] = objects[0]

        return self.cleaned_data

    def save(self, *args, **kwargs):
        self.instance.definition = self.cleaned_data.get("definition")
        self.instance.assigned_object = self.cleaned_data.get("assigned_object")

        return super().save(*args, **kwargs)


class OptionBulkEditForm(
    ClientClassBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = Option

    fieldsets = (
        FieldSet(
            "description",
            "definition",
            "data",
            "weight",
            "csv_format",
            "send_option",
            name=_("Option"),
        ),
        ClientClassBulkEditFormMixin.FIELDSET,
    )

    nullable_fields = (
        "data",
        "description",
        "csv_format",
        "send_option",
        *ClientClassBulkEditFormMixin.NULLABLE_FIELDS,
    )

    description = forms.CharField(
        label=_("Description"),
        required=False,
    )
    definition = forms.ModelChoiceField(
        label=_("Option Definition"),
        queryset=OptionDefinition.objects.all(),
        required=False,
    )
    data = forms.CharField(
        label=_("Data"),
        required=False,
    )
    weight = forms.IntegerField(
        label=_("Weight"),
        required=False,
    )
    csv_format = forms.NullBooleanField(
        label=_("CSV Format"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
    send_option = forms.NullBooleanField(
        label=_("Send Option"),
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
