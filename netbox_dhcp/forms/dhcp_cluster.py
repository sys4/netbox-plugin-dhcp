from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelBulkEditForm,
)
from utilities.forms.fields import TagFilterField, CSVChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms import add_blank_choice

from netbox_dhcp.models import DHCPCluster
from netbox_dhcp.choices import DHCPClusterStatusChoices

from .mixins import (
    NetBoxDHCPFilterFormMixin,
    NetBoxDHCPBulkEditFormMixin,
)


__all__ = (
    "DHCPClusterForm",
    "DHCPClusterFilterForm",
    "DHCPClusterImportForm",
    "DHCPClusterBulkEditForm",
)


class DHCPClusterForm(PrimaryModelForm):
    class Meta:
        model = DHCPCluster

        fields = (
            "name",
            "description",
            "status",
            "tags",
        )

    fieldsets = (
        FieldSet(
            "name",
            "description",
            "status",
            name=_("DHCP Cluster"),
        ),
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )


class DHCPClusterFilterForm(NetBoxDHCPFilterFormMixin, PrimaryModelFilterSetForm):
    model = DHCPCluster

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
            "status",
            name=_("DHCP Cluster"),
        ),
    )

    status = forms.MultipleChoiceField(
        choices=DHCPClusterStatusChoices,
        required=False,
        label=_("Status"),
    )

    tag = TagFilterField(DHCPCluster)


class DHCPClusterImportForm(PrimaryModelImportForm):
    class Meta:
        model = DHCPCluster

        fields = (
            "name",
            "description",
            "status",
            "comments",
            "tags",
        )

    status = CSVChoiceField(
        choices=DHCPClusterStatusChoices,
        required=False,
        label=_("Status"),
    )


class DHCPClusterBulkEditForm(NetBoxDHCPBulkEditFormMixin, PrimaryModelBulkEditForm):
    model = DHCPCluster

    fieldsets = (
        FieldSet(
            "description",
            "status",
            name=_("DHCP Cluster"),
        ),
    )

    nullable_fields = ("description",)

    status = forms.ChoiceField(
        choices=add_blank_choice(DHCPClusterStatusChoices),
        required=False,
        label=_("Status"),
    )
