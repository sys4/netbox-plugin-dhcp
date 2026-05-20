import django_filters
from django.db.models import Q

from netbox.filtersets import PrimaryModelFilterSet
from netbox_dhcp.choices import DHCPClusterStatusChoices
from netbox_dhcp.models import DHCPCluster
from utilities.filtersets import register_filterset

__all__ = ("DHCPClusterFilterSet",)


@register_filterset
class DHCPClusterFilterSet(PrimaryModelFilterSet):
    class Meta:
        model = DHCPCluster

        fields = (
            "id",
            "name",
            "description",
            "status",
        )

    status = django_filters.MultipleChoiceFilter(
        choices=DHCPClusterStatusChoices,
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)
