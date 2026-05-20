import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from dcim.models import MACAddress
from ipam.choices import IPAddressFamilyChoices
from ipam.models import IPAddress, Prefix
from netbox.filtersets import PrimaryModelFilterSet
from netbox_dhcp.models import HostReservation
from utilities.filters import MultiValueMACAddressFilter
from utilities.filtersets import register_filterset

from .mixins import (
    BOOTPFilterMixin,
    ClientClassFilterMixin,
    DHCPServerFilterMixin,
    OptionFilterMixin,
    SubnetFilterMixin,
)

__all__ = ("HostReservationFilterSet",)


@register_filterset
class HostReservationFilterSet(
    DHCPServerFilterMixin,
    SubnetFilterMixin,
    ClientClassFilterMixin,
    BOOTPFilterMixin,
    OptionFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = HostReservation

        fields = (
            "id",
            "name",
            "description",
            "duid",
            "circuit_id",
            "client_id",
            "flex_id",
            "hostname",
            *ClientClassFilterMixin.FILTER_FIELDS,
            *BOOTPFilterMixin.FILTER_FIELDS,
        )

    hw_address = MultiValueMACAddressFilter(
        field_name="hw_address__mac_address",
        label=_("Hardware Address"),
    )
    hw_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=MACAddress.objects.all(),
        field_name="hw_address",
        label=_("Hardware Address ID"),
    )
    ipv4_address = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_4
        ),
        field_name="ipv4_address__address",
        to_field_name="address",
        label=_("IPv4 Address"),
    )
    ipv4_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_4
        ),
        field_name="ipv4_address",
        label=_("IPv4 Address ID"),
    )
    ipv6_address = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_6
        ),
        field_name="ipv6_addresses__address",
        to_field_name="address",
        distinct=True,
        label=_("IPv6 Address"),
    )
    ipv6_address_id = django_filters.ModelMultipleChoiceFilter(
        queryset=IPAddress.objects.filter(
            address__family=IPAddressFamilyChoices.FAMILY_6
        ),
        field_name="ipv6_addresses",
        label=_("IPv6 Address ID"),
    )
    ipv6_prefix = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        field_name="ipv6_prefixes__prefix",
        to_field_name="prefix",
        distinct=True,
        label=_("IPv6 Prefix"),
    )
    ipv6_prefix_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        field_name="ipv6_prefixes",
        label=_("IPv6 Prefix ID"),
    )
    excluded_ipv6_prefix = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        field_name="excluded_ipv6_prefixes__prefix",
        to_field_name="prefix",
        distinct=True,
        label=_("Excluded IPv6 Prefix"),
    )
    excluded_ipv6_prefix_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Prefix.objects.filter(prefix__family=IPAddressFamilyChoices.FAMILY_6),
        field_name="excluded_ipv6_prefixes",
        label=_("Excluded IPv6 Prefix ID"),
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)
