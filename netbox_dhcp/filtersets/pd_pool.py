import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset
from ipam.models import Prefix

from netbox_dhcp.models import PDPool

from .mixins import (
    SubnetFilterMixin,
    PrefixFilterMixin,
    ClientClassFilterMixin,
    EvaluateClientClassFilterMixin,
    OptionFilterMixin,
)

__all__ = ("PDPoolFilterSet",)


@register_filterset
class PDPoolFilterSet(
    SubnetFilterMixin,
    PrefixFilterMixin,
    ClientClassFilterMixin,
    EvaluateClientClassFilterMixin,
    OptionFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = PDPool

        fields = (
            "id",
            "name",
            "description",
            "weight",
            "pool_id",
            "delegated_length",
        )

    excluded_prefix = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
        field_name="excluded_prefix__prefix",
        to_field_name="prefix",
        label=_("Excluded Prefix"),
    )
    excluded_prefix_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.all(),
        field_name="excluded_prefix",
        label=_("Excluded Prefix"),
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)
