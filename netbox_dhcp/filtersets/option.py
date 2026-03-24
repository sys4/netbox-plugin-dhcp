import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import PrimaryModelFilterSet
from utilities.filtersets import register_filterset
from utilities.filters import MultiValueCharFilter, MultiValueNumberFilter
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import Option, OptionDefinition
from netbox_dhcp.choices import OptionSpaceChoices
from .mixins import ClientClassFilterMixin

__all__ = ("OptionFilterSet",)


@register_filterset
class OptionFilterSet(
    ClientClassFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = Option

        fields = (
            "id",
            "description",
            "weight",
            "data",
            "csv_format",
            "send_option",
            *ClientClassFilterMixin.FILTER_FIELDS,
        )

    family = django_filters.MultipleChoiceFilter(
        label=_("Address Family"),
        field_name="definition__family",
        choices=IPAddressFamilyChoices,
    )
    space = django_filters.MultipleChoiceFilter(
        label=_("Space"),
        field_name="definition__space",
        choices=OptionSpaceChoices,
    )
    name = MultiValueCharFilter(
        label=_("Name"),
        field_name="definition__name",
    )
    code = MultiValueNumberFilter(
        label=_("Code"),
        field_name="definition__code",
    )
    data = django_filters.CharFilter(
        label=_("Data"),
    )
    definition = django_filters.ModelMultipleChoiceFilter(
        queryset=OptionDefinition.objects.all(),
        field_name="definition__name",
        to_field_name="name",
        label=_("Option Definition"),
    )
    definition_id = django_filters.ModelMultipleChoiceFilter(
        queryset=OptionDefinition.objects.all(),
        label=_("Option Definition ID"),
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(definition__name__icontains=value) | Q(data__icontains=value)
        return queryset.filter(qs_filter)
