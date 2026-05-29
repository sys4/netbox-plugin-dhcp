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
from netbox_dhcp.models import Subnet
from utilities.forms import add_blank_choice, get_field_value
from utilities.forms.fields import TagFilterField
from utilities.forms.rendering import FieldSet, TabbedGroups

from .mixins import (
    BOOTPBulkEditFormMixin,
    BOOTPFilterFormMixin,
    BOOTPFormMixin,
    BOOTPImportFormMixin,
    ClientClassesBulkEditFormMixin,
    ClientClassesFilterFormMixin,
    ClientClassesFormMixin,
    ClientClassesImportFormMixin,
    DDNSUpdateBulkEditFormMixin,
    DDNSUpdateFilterFormMixin,
    DDNSUpdateFormMixin,
    DDNSUpdateImportFormMixin,
    DHCPServerBulkEditFormMixin,
    DHCPServerFilterFormMixin,
    DHCPServerFormMixin,
    DHCPServerImportFormMixin,
    EvaluateClientClassesBulkEditFormMixin,
    EvaluateClientClassesFilterFormMixin,
    EvaluateClientClassesFormMixin,
    EvaluateClientClassesImportFormMixin,
    LeaseBulkEditFormMixin,
    LeaseFilterFormMixin,
    LeaseFormMixin,
    LeaseImportFormMixin,
    LifetimeBulkEditFormMixin,
    LifetimeFilterFormMixin,
    LifetimeFormMixin,
    LifetimeImportFormMixin,
    NetBoxDHCPBulkEditFormMixin,
    NetBoxDHCPFilterFormMixin,
    NetworkBulkEditFormMixin,
    NetworkFilterFormMixin,
    NetworkFormMixin,
    NetworkImportFormMixin,
    PrefixFilterFormMixin,
    PrefixFormMixin,
    PrefixImportFormMixin,
    SharedNetworkBulkEditFormMixin,
    SharedNetworkFilterFormMixin,
    SharedNetworkFormMixin,
    SharedNetworkImportFormMixin,
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
    ClientClassesFormMixin,
    EvaluateClientClassesFormMixin,
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
            *ClientClassesFormMixin.FIELDS,
            *EvaluateClientClassesFormMixin.FIELDS,
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
            *ClientClassesFormMixin.FIELDS,
            *EvaluateClientClassesFormMixin.FIELDS,
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
    ClientClassesFilterFormMixin,
    EvaluateClientClassesFilterFormMixin,
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
            *ClientClassesFilterFormMixin.FIELDS,
            *EvaluateClientClassesFilterFormMixin.FIELDS,
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
    ClientClassesImportFormMixin,
    EvaluateClientClassesImportFormMixin,
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
            *ClientClassesImportFormMixin.FIELDS,
            *EvaluateClientClassesImportFormMixin.FIELDS,
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
    ClientClassesBulkEditFormMixin,
    EvaluateClientClassesBulkEditFormMixin,
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
            *ClientClassesBulkEditFormMixin.FIELDS,
            *EvaluateClientClassesBulkEditFormMixin.FIELDS,
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
        *ClientClassesBulkEditFormMixin.NULLABLE_FIELDS,
        *EvaluateClientClassesBulkEditFormMixin.NULLABLE_FIELDS,
        *BOOTPBulkEditFormMixin.NULLABLE_FIELDS,
        *LifetimeBulkEditFormMixin.NULLABLE_FIELDS,
        *LeaseBulkEditFormMixin.NULLABLE_FIELDS,
        *DDNSUpdateBulkEditFormMixin.NULLABLE_FIELDS,
    )

    weight = forms.IntegerField(
        required=False,
        label=_("Weight"),
    )
