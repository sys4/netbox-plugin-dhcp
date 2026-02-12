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
from utilities.forms import add_blank_choice, get_field_value
from ipam.choices import IPAddressFamilyChoices

from ipam.models import Prefix

from netbox_dhcp.models import SharedNetwork
from .mixins import (
    NetBoxDHCPFilterFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    DHCPServerFormMixin,
    DHCPServerFilterFormMixin,
    DHCPServerImportFormMixin,
    DHCPServerBulkEditFormMixin,
    ClientClassFormMixin,
    ClientClassFilterFormMixin,
    ClientClassImportFormMixin,
    ClientClassBulkEditFormMixin,
    EvaluateClientClassBulkEditFormMixin,
    EvaluateClientClassFilterFormMixin,
    EvaluateClientClassFormMixin,
    EvaluateClientClassImportFormMixin,
    LifetimeFormMixin,
    LifetimeFilterFormMixin,
    LifetimeImportFormMixin,
    LifetimeBulkEditFormMixin,
    BOOTPFormMixin,
    BOOTPFilterFormMixin,
    BOOTPImportFormMixin,
    BOOTPBulkEditFormMixin,
    PrefixFormMixin,
    PrefixFilterFormMixin,
    PrefixImportFormMixin,
    PrefixBulkEditFormMixin,
    DDNSUpdateFormMixin,
    DDNSUpdateFilterFormMixin,
    DDNSUpdateImportFormMixin,
    DDNSUpdateBulkEditFormMixin,
    LeaseFormMixin,
    LeaseFilterFormMixin,
    LeaseImportFormMixin,
    LeaseBulkEditFormMixin,
    NetworkFormMixin,
    NetworkFilterFormMixin,
    NetworkImportFormMixin,
    NetworkBulkEditFormMixin,
)

from .mixins.model import DYNAMIC_ATTRIBUTES

__all__ = (
    "SharedNetworkForm",
    "SharedNetworkFilterForm",
    "SharedNetworkImportForm",
    "SharedNetworkBulkEditForm",
)


class SharedNetworkForm(
    DHCPServerFormMixin,
    PrefixFormMixin,
    ClientClassFormMixin,
    EvaluateClientClassFormMixin,
    NetworkFormMixin,
    LifetimeFormMixin,
    DDNSUpdateFormMixin,
    LeaseFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = SharedNetwork

        fields = (
            "name",
            "description",
            "weight",
            *DHCPServerFormMixin.FIELDS,
            "prefix",
            *ClientClassFormMixin.FIELDS,
            *EvaluateClientClassFormMixin.FIELDS,
            *NetworkFormMixin.FIELDS,
            *BOOTPFormMixin.FIELDS,
            *LifetimeFormMixin.FIELDS,
            *LeaseFormMixin.FIELDS,
            *DDNSUpdateFormMixin.FIELDS,
            "tags",
        )

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "weight",
            *DHCPServerFormMixin.FIELDS,
            "prefix",
            name=_("Shared Network"),
        ),
        FieldSet(
            *ClientClassFormMixin.FIELDS,
            *EvaluateClientClassFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        NetworkFormMixin.FIELDSET,
        BOOTPFormMixin.FIELDSET,
        LifetimeFormMixin.FIELDSET,
        LeaseFormMixin.FIELDSET,
        DDNSUpdateFormMixin.FIELDSET,
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["dhcp_server"].required = True

        self.fields["prefix"].widget.attrs.update(DYNAMIC_ATTRIBUTES)

        family = None
        if prefix_id := get_field_value(self, "prefix"):
            family = (
                Prefix.objects.filter(pk=prefix_id)
                .values_list("prefix", flat=True)
                .first()
                .version
            )

        if family == IPAddressFamilyChoices.FAMILY_6:
            self.fieldsets = (
                *self.fieldsets[0:3],
                *self.fieldsets[4:],
            )

        self.init_ddns_fields()

        self.init_lease_fields(family=family)
        self.init_lifetime_fields(family=family)
        self.init_network_fields(family=family)


class SharedNetworkFilterForm(
    NetBoxDHCPFilterFormMixin,
    DHCPServerFilterFormMixin,
    PrefixFilterFormMixin,
    BOOTPFilterFormMixin,
    ClientClassFilterFormMixin,
    EvaluateClientClassFilterFormMixin,
    LifetimeFilterFormMixin,
    DDNSUpdateFilterFormMixin,
    LeaseFilterFormMixin,
    NetworkFilterFormMixin,
    PrimaryModelFilterSetForm,
):
    model = SharedNetwork

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
            *DHCPServerFilterFormMixin.FIELDS,
            "prefix_id",
            name=_("Shared Network"),
        ),
        FieldSet(
            *ClientClassFilterFormMixin.FIELDS,
            *EvaluateClientClassFilterFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        NetworkFilterFormMixin.FIELDSET,
        BOOTPFilterFormMixin.FIELDSET,
        LifetimeFilterFormMixin.FIELDSET,
        LeaseFilterFormMixin.FIELDSET,
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

    tag = TagFilterField(SharedNetwork)


class SharedNetworkImportForm(
    DHCPServerImportFormMixin,
    PrefixImportFormMixin,
    ClientClassImportFormMixin,
    EvaluateClientClassImportFormMixin,
    DDNSUpdateImportFormMixin,
    LeaseImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = SharedNetwork

        fields = (
            "name",
            "description",
            "weight",
            *DHCPServerImportFormMixin.FIELDS,
            "prefix",
            *ClientClassImportFormMixin.FIELDS,
            *EvaluateClientClassImportFormMixin.FIELDS,
            *NetworkImportFormMixin.FIELDS,
            *BOOTPImportFormMixin.FIELDS,
            *LifetimeImportFormMixin.FIELDS,
            *LeaseImportFormMixin.FIELDS,
            *DDNSUpdateImportFormMixin.FIELDS,
            "comments",
            "tags",
        )


class SharedNetworkBulkEditForm(
    NetBoxDHCPBulkEditFormMixin,
    DHCPServerBulkEditFormMixin,
    PrefixBulkEditFormMixin,
    BOOTPBulkEditFormMixin,
    ClientClassBulkEditFormMixin,
    EvaluateClientClassBulkEditFormMixin,
    LifetimeBulkEditFormMixin,
    DDNSUpdateBulkEditFormMixin,
    LeaseBulkEditFormMixin,
    NetworkBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = SharedNetwork

    fieldsets = (
        FieldSet(
            "description",
            "weight",
            "prefix",
            *DHCPServerBulkEditFormMixin.FIELDS,
            name=_("Shared Network"),
        ),
        FieldSet(
            *ClientClassBulkEditFormMixin.FIELDS,
            *EvaluateClientClassBulkEditFormMixin.FIELDS,
            name=_("Client Classes"),
        ),
        NetworkBulkEditFormMixin.FIELDSET,
        BOOTPBulkEditFormMixin.FIELDSET,
        LifetimeBulkEditFormMixin.FIELDSET,
        LeaseBulkEditFormMixin.FIELDSET,
        DDNSUpdateBulkEditFormMixin.FIELDSET,
    )

    nullable_fields = (
        "description",
        *NetworkBulkEditFormMixin.NULLABLE_FIELDS,
        *ClientClassBulkEditFormMixin.NULLABLE_FIELDS,
        *EvaluateClientClassBulkEditFormMixin.NULLABLE_FIELDS,
        *BOOTPBulkEditFormMixin.NULLABLE_FIELDS,
        *LifetimeBulkEditFormMixin.NULLABLE_FIELDS,
        *LeaseBulkEditFormMixin.NULLABLE_FIELDS,
        *DDNSUpdateBulkEditFormMixin.NULLABLE_FIELDS,
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )
