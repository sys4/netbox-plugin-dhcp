import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from ipam.choices import IPAddressFamilyChoices
from netbox.filtersets import PrimaryModelFilterSet
from netbox_dhcp.models import SharedNetwork
from utilities.filtersets import register_filterset

from .mixins import (
    BOOTPFilterMixin,
    ChildSubnetFilterMixin,
    ClientClassFilterMixin,
    DDNSUpdateFilterMixin,
    DHCPServerFilterMixin,
    EvaluateClientClassFilterMixin,
    LeaseFilterMixin,
    LifetimeFilterMixin,
    NetworkFilterMixin,
    OptionFilterMixin,
    PrefixFilterMixin,
)

__all__ = ("SharedNetworkFilterSet",)


@register_filterset
class SharedNetworkFilterSet(
    DHCPServerFilterMixin,
    PrefixFilterMixin,
    ClientClassFilterMixin,
    EvaluateClientClassFilterMixin,
    BOOTPFilterMixin,
    LifetimeFilterMixin,
    LeaseFilterMixin,
    NetworkFilterMixin,
    DDNSUpdateFilterMixin,
    ChildSubnetFilterMixin,
    OptionFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = SharedNetwork

        fields = (
            "id",
            "name",
            "description",
            "weight",
            *DHCPServerFilterMixin.FILTER_FIELDS,
            *PrefixFilterMixin.FILTER_FIELDS,
            *BOOTPFilterMixin.FILTER_FIELDS,
            *LifetimeFilterMixin.FILTER_FIELDS,
            *LeaseFilterMixin.FILTER_FIELDS,
            *DDNSUpdateFilterMixin.FILTER_FIELDS,
            *NetworkFilterMixin.FILTER_FIELDS,
            *ChildSubnetFilterMixin.FILTER_FIELDS,
        )

    family = django_filters.MultipleChoiceFilter(
        choices=IPAddressFamilyChoices,
        field_name="prefix__prefix",
        lookup_expr="family",
        label=_("Address Family"),
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(boot_file_name__icontains=value)
        return queryset.filter(qs_filter)
