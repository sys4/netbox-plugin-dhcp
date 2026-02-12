from django.db.models import Q

from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset

from ..models import ClientClass
from .mixins import (
    DHCPServerFilterMixin,
    BOOTPFilterMixin,
    LifetimeFilterMixin,
)

__all__ = ("ClientClassFilterSet",)


@register_filterset
class ClientClassFilterSet(
    DHCPServerFilterMixin,
    BOOTPFilterMixin,
    LifetimeFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = ClientClass

        fields = (
            "id",
            "name",
            "description",
            "weight",
            "test",
            "template_test",
            "only_in_additional_list",
            *DHCPServerFilterMixin.FILTER_FIELDS,
            *BOOTPFilterMixin.FILTER_FIELDS,
            *LifetimeFilterMixin.FILTER_FIELDS,
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(test__icontains=value)
            | Q(template_test__icontains=value)
            | Q(boot_file_name__icontains=value)
        )
        return queryset.filter(qs_filter)
