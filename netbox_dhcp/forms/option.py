from django import forms
from django.core.exceptions import FieldError, ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from ipam.choices import IPAddressFamilyChoices
from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelForm,
    PrimaryModelImportForm,
)
from netbox_dhcp.choices import OptionSendChoices, OptionSpaceChoices
from netbox_dhcp.models import (
    ClientClass,
    DHCPServer,
    HostReservation,
    Option,
    OptionDefinition,
    PDPool,
    Pool,
    SharedNetwork,
    Subnet,
)
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from utilities.forms.fields import CSVChoiceField, CSVModelChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from .mixins import (
    ClientClassesBulkEditFormMixin,
    ClientClassesFilterFormMixin,
    ClientClassesFormMixin,
    ClientClassesImportFormMixin,
)

__all__ = (
    "OptionForm",
    "OptionFilterForm",
    "OptionImportForm",
    "OptionBulkEditForm",
)


class CSVOptionDefinitionChoiceField(CSVModelChoiceField):
    # +
    # Custom variant of the NetBox CSVModelChoiceField
    #
    # The value is generated from a queryset that may or may not
    # return exactly one result. In case of multiple records matching the
    # queryset,  the first result is returned as the result after ordering
    # it by standard, -client_class and -dhcp_server.
    #
    # At the moment, ordering is hard-coded, but this field class may
    # be extended to receive the ordering criteria as a parameter at a
    # later time.
    # -
    def to_python(self, value):
        if value in self.empty_values:
            return None

        self.validate_no_null_characters(value)

        try:
            key = self.to_field_name or "pk"
            if isinstance(value, self.queryset.model):
                value = getattr(value, key)

            result = self.queryset.filter(**{key: value}).order_by(
                "standard",
                "-client_class",
                "-dhcp_server",
            )[:1]

            if result.exists():
                return result.first()
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )

        except (ValueError, TypeError):
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )
        except FieldError:
            raise forms.ValidationError(
                _('"{field_name}" is an invalid accessor field name.').format(
                    field_name=self.to_field_name
                )
            )


class OptionForm(
    ClientClassesFormMixin,
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
            *ClientClassesFormMixin.FIELDS,
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
        ClientClassesFormMixin.FIELDSET,
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
    ClientClassesFilterFormMixin,
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
        ClientClassesFilterFormMixin.FIELDSET,
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
    ClientClassesImportFormMixin,
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
            *ClientClassesImportFormMixin.FIELDS,
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
    name = CSVOptionDefinitionChoiceField(
        label=_("Name"),
        queryset=OptionDefinition.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": _("No option definition with name %(value)s found"),
        },
    )
    code = CSVOptionDefinitionChoiceField(
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

        self.fields["weight"].required = False

        if self.is_bound:
            dhcp_server = None
            client_class = None

            if "client_class" in self.data:
                try:
                    client_class = self.fields["client_class"].to_python(
                        self.data["client_class"]
                    )
                    dhcp_server = client_class.dhcp_server
                except forms.ValidationError:
                    pass

            elif "dhcp_server" in self.data:
                try:
                    dhcp_server = self.fields["dhcp_server"].to_python(
                        self.data["dhcp_server"]
                    )
                except forms.ValidationError:
                    pass

            else:
                for object_name in (
                    "subnet",
                    "shared_network",
                    "pool",
                    "pd_pool",
                    "host_reservation",
                ):
                    if object_name in self.data:
                        obj = self.fields[object_name].to_python(self.data[object_name])
                        dhcp_server = obj.dhcp_server
                        continue

            queryset = OptionDefinition.objects.filter(
                Q(
                    Q(standard=True)
                    | Q(
                        standard=False,
                        dhcp_server__isnull=False,
                        dhcp_server=dhcp_server,
                    )
                    | Q(
                        standard=False,
                        client_class__isnull=False,
                        client_class=client_class,
                    )
                ),
                Q(space=self.data.get("space")),
            )

            self.fields["code"].queryset = queryset
            self.fields["name"].queryset = queryset

    def clean(self):
        super().clean()

        name = self.cleaned_data.get("name")
        code = self.cleaned_data.get("code")

        if code is not None:
            self.cleaned_data["definition"] = code
        elif name is not None:
            self.cleaned_data["definition"] = name

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

        if len(objects) == 1:
            self.cleaned_data["assigned_object"] = objects[0]
        elif len(objects) > 1 or self.instance._state.adding:
            raise forms.ValidationError(_("Exactly one assigned object is required"))

        return self.cleaned_data

    def save(self, *args, **kwargs):
        if "definition" in self.cleaned_data:
            self.instance.definition = self.cleaned_data.get("definition")

        if "assigned_object" in self.cleaned_data:
            self.instance.assigned_object = self.cleaned_data.get("assigned_object")

        return super().save(*args, **kwargs)


class OptionBulkEditForm(
    ClientClassesBulkEditFormMixin,
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
        ClientClassesBulkEditFormMixin.FIELDSET,
    )

    nullable_fields = (
        "data",
        "description",
        "csv_format",
        "send_option",
        *ClientClassesBulkEditFormMixin.NULLABLE_FIELDS,
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
