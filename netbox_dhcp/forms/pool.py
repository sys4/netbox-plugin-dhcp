from django import forms
from django.utils.translation import gettext_lazy as _

from ipam.choices import IPAddressFamilyChoices
from ipam.models import VRF, IPRange, Prefix
from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelForm,
    PrimaryModelImportForm,
)
from netbox_dhcp.models import Pool
from utilities.forms import add_blank_choice, get_field_value
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
    DDNSUpdateBulkEditFormMixin,
    DDNSUpdateFilterFormMixin,
    DDNSUpdateFormMixin,
    DDNSUpdateImportFormMixin,
    EvaluateClientClassesBulkEditFormMixin,
    EvaluateClientClassesFilterFormMixin,
    EvaluateClientClassesFormMixin,
    EvaluateClientClassesImportFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    NetBoxDHCPFilterFormMixin,
    SubnetBulkEditFormMixin,
    SubnetFilterFormMixin,
    SubnetFormMixin,
    SubnetImportFormMixin,
)
from .mixins.model import DYNAMIC_ATTRIBUTES

__all__ = (
    "PoolForm",
    "PoolFilterForm",
    "PoolImportForm",
    "PoolBulkEditForm",
)


class PoolForm(
    SubnetFormMixin,
    ClientClassesFormMixin,
    EvaluateClientClassesFormMixin,
    DDNSUpdateFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = Pool

        fields = (
            "name",
            "description",
            "weight",
            *SubnetFormMixin.FIELDS,
            "ip_range",
            *ClientClassesFormMixin.FIELDS,
            *EvaluateClientClassesFormMixin.FIELDS,
            *DDNSUpdateFormMixin.FIELDS,
            "tags",
        )

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "weight",
            *SubnetFormMixin.FIELDS,
            "ip_range",
            name=_("Address Pool"),
        ),
        FieldSet(
            *ClientClassesFormMixin.FIELDS,
            *EvaluateClientClassesFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        DDNSUpdateFormMixin.FIELDSET,
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subnet"].widget.attrs.update(DYNAMIC_ATTRIBUTES)

        if subnet_id := get_field_value(self, "subnet"):
            prefix = (
                Prefix.objects.filter(netbox_dhcp_subnets=subnet_id)
                .values_list("prefix", flat=True)
                .first()
            )
            self.fields["ip_range"].widget.add_query_param("parent", str(prefix))

        self.init_ddns_fields()

    ip_range = DynamicModelChoiceField(
        queryset=IPRange.objects.all(),
        required=True,
        quick_add=True,
        selector=True,
        label=_("IP Range"),
    )


class PoolFilterForm(
    SubnetFilterFormMixin,
    NetBoxDHCPFilterFormMixin,
    ClientClassesFilterFormMixin,
    EvaluateClientClassesFilterFormMixin,
    DDNSUpdateFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = Pool

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
            "family",
            *SubnetFilterFormMixin.FIELDS,
            "ip_range_id",
            name=_("Address Pool"),
        ),
        FieldSet(
            *ClientClassesFilterFormMixin.FIELDS,
            *EvaluateClientClassesFilterFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        DDNSUpdateFilterFormMixin.FIELDSET,
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )
    family = forms.ChoiceField(
        choices=add_blank_choice(IPAddressFamilyChoices),
        required=False,
        label=_("Address Family"),
    )
    ip_range_id = DynamicModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        query_params={
            "family": "$family",
        },
        required=False,
        label=_("IP Range"),
    )

    tag = TagFilterField(Pool)


class PoolImportForm(
    SubnetImportFormMixin,
    ClientClassesImportFormMixin,
    EvaluateClientClassesImportFormMixin,
    DDNSUpdateImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = Pool

        fields = (
            "name",
            "description",
            "weight",
            *SubnetImportFormMixin.FIELDS,
            "vrf",
            "ip_range",
            *ClientClassesImportFormMixin.FIELDS,
            *EvaluateClientClassesImportFormMixin.FIELDS,
            *DDNSUpdateImportFormMixin.FIELDS,
            "comments",
            "tags",
        )

    vrf = CSVModelChoiceField(
        queryset=VRF.objects.all(),
        to_field_name="name",
        required=False,
        label=_("IP Range VRF"),
    )
    ip_range = CSVModelChoiceField(
        queryset=IPRange.objects.all(),
        to_field_name="start_address",
        required=False,
        error_messages={
            "invalid_choice": _("IP range with start address %(value)s not found"),
        },
        label=_("IP Range Start Address"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["weight"].required = False

        if self.is_bound and "vrf" in self.data:
            self.fields["ip_range"].queryset = self.fields["ip_range"].queryset.filter(
                vrf=self.data["vrf"]
            )


class PoolBulkEditForm(
    SubnetBulkEditFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    ClientClassesBulkEditFormMixin,
    EvaluateClientClassesBulkEditFormMixin,
    DDNSUpdateBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = Pool

    fieldsets = (
        FieldSet(
            "description",
            "weight",
            *SubnetBulkEditFormMixin.FIELDS,
            name=_("Address Pool"),
        ),
        FieldSet(
            *ClientClassesBulkEditFormMixin.FIELDS,
            *EvaluateClientClassesBulkEditFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        DDNSUpdateBulkEditFormMixin.FIELDSET,
    )

    nullable_fields = (
        "description",
        *ClientClassesBulkEditFormMixin.NULLABLE_FIELDS,
        *DDNSUpdateBulkEditFormMixin.NULLABLE_FIELDS,
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )
