import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _
from netaddr import AddrFormatError, IPNetwork

from ipam.choices import IPAddressFamilyChoices
from ipam.models import IPRange
from netbox.filtersets import PrimaryModelFilterSet
from netbox_dhcp.models import Pool
from utilities.filters import MultiValueCharFilter
from utilities.filtersets import register_filterset

from .mixins import (
    ClientClassFilterMixin,
    DDNSUpdateFilterMixin,
    EvaluateClientClassFilterMixin,
    OptionFilterMixin,
    SubnetFilterMixin,
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
    start_address = MultiValueCharFilter(
        method="filter_ip_range",
        label=_("Pool Start Address"),
    )
    end_address = MultiValueCharFilter(
        method="filter_ip_range",
        label=_("Pool End Address"),
    )
    contains_address = MultiValueCharFilter(
        method="filter_ip_range",
        label=_("Pool Contains"),
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)

    def filter_ip_range(self, queryset, name, value):
        if not value:
            return queryset

        match name:
            case "start_address" | "end_address":
                query = Q()
                for address in value:
                    try:
                        address = IPNetwork(address).ip
                    except AddrFormatError:
                        continue
                    query |= Q(**{f"{name}__net_host_contained": address})
            case "contains_address":
                query = Q()
                for address in value:
                    try:
                        address = IPNetwork(address).ip
                    except AddrFormatError:
                        continue
                    query |= Q(
                        start_address__net_host_lte=address,
                        end_address__net_host_gte=address,
                    )
            case _:
                return queryset

        return queryset.filter(ip_range__in=IPRange.objects.filter(query)).distinct()
