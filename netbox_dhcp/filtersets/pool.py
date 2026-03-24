import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset
from ipam.models import IPRange
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import Pool

from .mixins import (
    SubnetFilterMixin,
    ClientClassFilterMixin,
    EvaluateClientClassFilterMixin,
    DDNSUpdateFilterMixin,
    OptionFilterMixin,
)

__all__ = ("PoolFilterSet",)


@register_filterset
class PoolFilterSet(
    SubnetFilterMixin,
    ClientClassFilterMixin,
    EvaluateClientClassFilterMixin,
    DDNSUpdateFilterMixin,
    OptionFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = Pool

        fields = (
            "id",
            "name",
            "description",
            "pool_id",
            "weight",
            *SubnetFilterMixin.FILTER_FIELDS,
            *DDNSUpdateFilterMixin.FILTER_FIELDS,
        )

    family = django_filters.MultipleChoiceFilter(
        label=_("Address Family"),
        choices=IPAddressFamilyChoices,
        field_name="ip_range__start_address",
        lookup_expr="family",
    )
    ip_range_id = django_filters.ModelMultipleChoiceFilter(
        queryset=IPRange.objects.all(),
        field_name="ip_range",
        label=_("IP Range ID"),
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)
