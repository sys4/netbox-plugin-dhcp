import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset
from utilities.filters import MultiValueCharFilter
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import OptionDefinition, ClientClass
from netbox_dhcp.choices import OptionSpaceChoices, OptionTypeChoices

from .mixins import (
    DHCPServerFilterMixin,
    ClientClassFilterMixin,
)

__all__ = ("OptionDefinitionFilterSet",)


@register_filterset
class OptionDefinitionFilterSet(
    DHCPServerFilterMixin,
    ClientClassFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = OptionDefinition

        fields = (
            "id",
            "name",
            "code",
            "description",
            "encapsulate",
            "array",
            "standard",
        )

    family = django_filters.MultipleChoiceFilter(
        label=_("Address Family"),
        choices=IPAddressFamilyChoices,
    )
    space = django_filters.MultipleChoiceFilter(
        label=_("Space"),
        choices=OptionSpaceChoices,
    )
    type = django_filters.MultipleChoiceFilter(
        label=_("Type"),
        choices=OptionTypeChoices,
    )
    record_types = MultiValueCharFilter(
        method="filter_record_types",
        label=_("Record Types"),
    )

    client_class = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="client_class__name",
        to_field_name="name",
        label=_("Client Class"),
    )
    client_class_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="client_class",
        label=_("Client Class ID"),
    )

    def filter_record_types(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(record_types__overlap=value)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = Q(Q(name__icontains=value) | Q(space__icontains=value))
        try:
            value = int(value)
            qs_filter |= Q(code=value)
        except ValueError:
            pass

        return queryset.filter(qs_filter)
