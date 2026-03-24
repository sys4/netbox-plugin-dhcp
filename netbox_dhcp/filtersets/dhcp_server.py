import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet
from utilities.filtersets import register_filterset
from dcim.models import Device, Interface
from virtualization.models import VirtualMachine, VMInterface
from utilities.filters import MultiValueCharFilter

from netbox_dhcp.models import DHCPServer, DHCPCluster, ClientClass, DHCPServerInterface
from netbox_dhcp.choices import (
    DHCPServerStatusChoices,
    DHCPServerIDTypeChoices,
    HostReservationIdentifierChoices,
)
from .mixins import (
    BOOTPFilterMixin,
    LifetimeFilterMixin,
    LeaseFilterMixin,
    DDNSUpdateFilterMixin,
    ChildSubnetFilterMixin,
    ChildSharedNetworkFilterMixin,
    ChildHostReservationFilterMixin,
)

__all__ = (
    "DHCPServerFilterSet",
    "DHCPServerInterfaceFilterSet",
)


class DHCPServerInterfaceFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = DHCPServerInterface

        fields = (
            "id",
            "device_interface",
            "virtual_machine_interface",
        )

    name = django_filters.CharFilter(
        method="filter_string",
    )
    parent_name = django_filters.CharFilter(
        method="filter_string",
    )

    def filter_string(self, queryset, name, value):
        if value in (None, ""):
            return queryset

        return queryset.filter(**{name: value})


@register_filterset
class DHCPServerFilterSet(
    BOOTPFilterMixin,
    LifetimeFilterMixin,
    LeaseFilterMixin,
    DDNSUpdateFilterMixin,
    ChildSubnetFilterMixin,
    ChildSharedNetworkFilterMixin,
    ChildHostReservationFilterMixin,
    PrimaryModelFilterSet,
):
    class Meta:
        model = DHCPServer

        fields = (
            "id",
            "name",
            "description",
            "server_id",
            "host_reservation_identifiers",
            "echo_client_id",
            "relay_supplied_options",
            "status",
            "dhcp_cluster",
            "device",
            "device_interfaces",
            "virtual_machine",
            "virtual_machine_interfaces",
            "decline_probation_period",
            *BOOTPFilterMixin.FILTER_FIELDS,
            *LifetimeFilterMixin.FILTER_FIELDS,
            *LeaseFilterMixin.FILTER_FIELDS,
            *DDNSUpdateFilterMixin.FILTER_FIELDS,
            *ChildSubnetFilterMixin.FILTER_FIELDS,
            *ChildSharedNetworkFilterMixin.FILTER_FIELDS,
            *ChildHostReservationFilterMixin.FILTER_FIELDS,
        )

    status = django_filters.MultipleChoiceFilter(
        choices=DHCPServerStatusChoices,
    )
    server_id = django_filters.MultipleChoiceFilter(
        choices=DHCPServerIDTypeChoices,
    )

    dhcp_cluster_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DHCPCluster.objects.all(),
    )
    dhcp_cluster = django_filters.ModelMultipleChoiceFilter(
        queryset=DHCPCluster.objects.all(),
        field_name="dhcp_cluster__name",
        to_field_name="name",
    )

    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name="device",
    )
    device = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        field_name="device__name",
        to_field_name="name",
    )
    device_interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Interface.objects.all(),
        field_name="device_interfaces",
    )
    device_interface = django_filters.ModelMultipleChoiceFilter(
        queryset=Interface.objects.all(),
        field_name="device_interfaces__name",
        to_field_name="name",
    )
    virtual_machine_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualMachine.objects.all(),
        field_name="virtual_machine",
    )
    virtual_machine = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualMachine.objects.all(),
        field_name="virtual_machine__name",
        to_field_name="name",
    )
    virtual_machine_interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VMInterface.objects.all(),
        field_name="virtual_machine_interfaces",
    )
    virtual_machine_interface = django_filters.ModelMultipleChoiceFilter(
        queryset=VMInterface.objects.all(),
        field_name="virtual_machine_interfaces__name",
        to_field_name="name",
    )
    interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DHCPServerInterface.objects.all(),
        field_name="interfaces",
    )
    host_reservation_identifiers = django_filters.MultipleChoiceFilter(
        choices=HostReservationIdentifierChoices,
        method="filter_host_reservation_identifiers",
    )
    relay_supplied_options = MultiValueCharFilter(
        method="filter_relay_supplied_options",
    )

    client_class = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="client_class_definition_set__name",
        to_field_name="name",
        distinct=True,
    )
    client_class_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ClientClass.objects.all(),
        field_name="client_class_definition_set",
    )

    def filter_host_reservation_identifiers(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(host_reservation_identifiers__overlap=value)

    def filter_relay_supplied_options(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(relay_supplied_options__overlap=value)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(dhcp_cluster__name__icontains=value)
            | Q(device__name__icontains=value)
            | Q(virtual_machine__name__icontains=value)
        )
        return queryset.filter(qs_filter)
