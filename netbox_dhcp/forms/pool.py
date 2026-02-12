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
from utilities.forms import add_blank_choice, get_field_value
from utilities.forms.rendering import FieldSet
from ipam.models import IPRange, Prefix
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import Pool

from .mixins import (
    SubnetFormMixin,
    SubnetFilterFormMixin,
    SubnetImportFormMixin,
    SubnetBulkEditFormMixin,
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
    DDNSUpdateFormMixin,
    DDNSUpdateFilterFormMixin,
    DDNSUpdateImportFormMixin,
    DDNSUpdateBulkEditFormMixin,
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
    ClientClassFormMixin,
    EvaluateClientClassFormMixin,
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
            *ClientClassFormMixin.FIELDS,
            *EvaluateClientClassFormMixin.FIELDS,
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
            *ClientClassFormMixin.FIELDS,
            *EvaluateClientClassFormMixin.FIELDS,
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
                .values_list("prefix")
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
    ClientClassFilterFormMixin,
    EvaluateClientClassFilterFormMixin,
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
            *ClientClassFilterFormMixin.FIELDS,
            *EvaluateClientClassFilterFormMixin.FIELDS,
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
    ClientClassImportFormMixin,
    EvaluateClientClassImportFormMixin,
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
            "ip_range",
            *ClientClassImportFormMixin.FIELDS,
            *EvaluateClientClassImportFormMixin.FIELDS,
            *DDNSUpdateImportFormMixin.FIELDS,
            "comments",
            "tags",
        )

    # TODO: Specify IP ranges by (start_address,end_address)
    ip_range = CSVModelChoiceField(
        queryset=IPRange.objects.all(),
        required=True,
        error_messages={
            "invalid_choice": _("IP range %(value)s not found"),
        },
        label=_("IP Range"),
    )


class PoolBulkEditForm(
    SubnetBulkEditFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    ClientClassBulkEditFormMixin,
    EvaluateClientClassBulkEditFormMixin,
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
            *ClientClassBulkEditFormMixin.FIELDS,
            *EvaluateClientClassBulkEditFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        DDNSUpdateBulkEditFormMixin.FIELDSET,
    )

    nullable_fields = (
        "description",
        *ClientClassBulkEditFormMixin.NULLABLE_FIELDS,
        *DDNSUpdateBulkEditFormMixin.NULLABLE_FIELDS,
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )
