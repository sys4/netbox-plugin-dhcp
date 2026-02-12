from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelBulkEditForm,
)
from utilities.forms.fields import TagFilterField
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms import add_blank_choice, get_field_value
from ipam.choices import IPAddressFamilyChoices
from ipam.models import Prefix

from netbox_dhcp.models import Subnet
from .mixins import (
    NetBoxDHCPFilterFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    DHCPServerFormMixin,
    DHCPServerFilterFormMixin,
    DHCPServerImportFormMixin,
    DHCPServerBulkEditFormMixin,
    SharedNetworkFormMixin,
    SharedNetworkFilterFormMixin,
    SharedNetworkImportFormMixin,
    SharedNetworkBulkEditFormMixin,
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
    DDNSUpdateFormMixin,
    DDNSUpdateFilterFormMixin,
    DDNSUpdateImportFormMixin,
    DDNSUpdateBulkEditFormMixin,
    LeaseFormMixin,
    LeaseImportFormMixin,
    LeaseFilterFormMixin,
    LeaseBulkEditFormMixin,
    NetworkFormMixin,
    NetworkFilterFormMixin,
    NetworkImportFormMixin,
    NetworkBulkEditFormMixin,
)

from .mixins.model import DYNAMIC_ATTRIBUTES


__all__ = (
    "SubnetForm",
    "SubnetFilterForm",
    "SubnetImportForm",
    "SubnetBulkEditForm",
)


class SubnetForm(
    DHCPServerFormMixin,
    SharedNetworkFormMixin,
    PrefixFormMixin,
    ClientClassFormMixin,
    EvaluateClientClassFormMixin,
    DDNSUpdateFormMixin,
    NetworkFormMixin,
    LeaseFormMixin,
    LifetimeFormMixin,
    PrimaryModelForm,
):
    class Meta:
        model = Subnet

        fields = (
            "name",
            "description",
            "weight",
            "subnet_id",
            *DHCPServerFormMixin.FIELDS,
            *SharedNetworkFormMixin.FIELDS,
            "prefix",
            *NetworkFormMixin.FIELDS,
            *ClientClassFormMixin.FIELDS,
            *EvaluateClientClassFormMixin.FIELDS,
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
            "subnet_id",
            TabbedGroups(
                FieldSet(
                    *DHCPServerFormMixin.FIELDS,
                    name=_("DHCP Server"),
                ),
                FieldSet(
                    *SharedNetworkFormMixin.FIELDS,
                    name=_("Shared Network"),
                ),
            ),
            "prefix",
            name=_("Subnet"),
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

        self.fields["shared_network"].widget.attrs.update(DYNAMIC_ATTRIBUTES)
        self.fields["prefix"].widget.attrs.update(DYNAMIC_ATTRIBUTES)

        if shared_network_id := get_field_value(self, "shared_network"):
            parent_prefix = (
                Prefix.objects.filter(netbox_dhcp_shared_networks=shared_network_id)
                .values_list("prefix", flat=True)
                .first()
            )
            self.fields["prefix"].widget.add_query_param(
                "within_include", str(parent_prefix)
            )

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


class SubnetFilterForm(
    NetBoxDHCPFilterFormMixin,
    DHCPServerFilterFormMixin,
    SharedNetworkFilterFormMixin,
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
    model = Subnet

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
            "subnet_id",
            *DHCPServerFilterFormMixin.FIELDS,
            *SharedNetworkFilterFormMixin.FIELDS,
            "prefix_id",
            name=_("Subnet"),
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

    tag = TagFilterField(Subnet)


class SubnetImportForm(
    DHCPServerImportFormMixin,
    SharedNetworkImportFormMixin,
    PrefixImportFormMixin,
    ClientClassImportFormMixin,
    EvaluateClientClassImportFormMixin,
    DDNSUpdateImportFormMixin,
    PrimaryModelImportForm,
):
    class Meta:
        model = Subnet

        fields = (
            "name",
            "description",
            "weight",
            "subnet_id",
            *DHCPServerImportFormMixin.FIELDS,
            *SharedNetworkImportFormMixin.FIELDS,
            "prefix",
            *NetworkImportFormMixin.FIELDS,
            *ClientClassImportFormMixin.FIELDS,
            *EvaluateClientClassImportFormMixin.FIELDS,
            *BOOTPImportFormMixin.FIELDS,
            *LifetimeImportFormMixin.FIELDS,
            *LeaseImportFormMixin.FIELDS,
            *DDNSUpdateImportFormMixin.FIELDS,
            "comments",
            "tags",
        )


class SubnetBulkEditForm(
    NetBoxDHCPBulkEditFormMixin,
    DHCPServerBulkEditFormMixin,
    SharedNetworkBulkEditFormMixin,
    BOOTPBulkEditFormMixin,
    ClientClassBulkEditFormMixin,
    EvaluateClientClassBulkEditFormMixin,
    LifetimeBulkEditFormMixin,
    DDNSUpdateBulkEditFormMixin,
    LeaseBulkEditFormMixin,
    NetworkBulkEditFormMixin,
    PrimaryModelBulkEditForm,
):
    model = Subnet

    fieldsets = (
        FieldSet(
            "description",
            "weight",
            TabbedGroups(
                FieldSet(
                    *DHCPServerBulkEditFormMixin.FIELDS,
                    name=_("DHCP Server"),
                ),
                FieldSet(
                    *SharedNetworkBulkEditFormMixin.FIELDS,
                    name=_("Shared Network"),
                ),
            ),
            name=_("Subnet"),
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
        *DHCPServerBulkEditFormMixin.NULLABLE_FIELDS,
        *SharedNetworkBulkEditFormMixin.NULLABLE_FIELDS,
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
