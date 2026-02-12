from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from utilities.views import register_model_view, ViewTab

from netbox_dhcp.models import (
    DHCPServer,
    Subnet,
    SharedNetwork,
    HostReservation,
    ClientClass,
    Option,
    OptionDefinition,
)
from netbox_dhcp.filtersets import (
    DHCPServerFilterSet,
    SubnetFilterSet,
    SharedNetworkFilterSet,
    HostReservationFilterSet,
    ClientClassFilterSet,
    OptionFilterSet,
    OptionDefinitionFilterSet,
)
from netbox_dhcp.forms import (
    DHCPServerForm,
    DHCPServerFilterForm,
    DHCPServerImportForm,
    DHCPServerBulkEditForm,
)
from netbox_dhcp.tables import (
    DHCPServerTable,
    SubnetTable,
    SharedNetworkTable,
    HostReservationTable,
    ClientClassTable,
    ChildOptionTable,
    OptionDefinitionTable,
)

__all__ = (
    "DHCPServerView",
    "DHCPServerListView",
    "DHCPServerEditView",
    "DHCPServerDeleteView",
    "DHCPServerBulkImportView",
    "DHCPServerBulkEditView",
    "DHCPServerBulkDeleteView",
    "DHCPServerChildSubnetListView",
    "DHCPServerChildSharedNetworkListView",
    "DHCPServerChildHostReservationListView",
    "DHCPServerOptionListView",
    "DHCPServerOptionDefinitionListView",
)


@register_model_view(DHCPServer, "list", path="", detail=False)
class DHCPServerListView(generic.ObjectListView):
    queryset = DHCPServer.objects.all()
    table = DHCPServerTable
    filterset = DHCPServerFilterSet
    filterset_form = DHCPServerFilterForm


@register_model_view(DHCPServer)
class DHCPServerView(generic.ObjectView):
    queryset = DHCPServer.objects.all()


@register_model_view(DHCPServer, "add", detail=False)
@register_model_view(DHCPServer, "edit")
class DHCPServerEditView(generic.ObjectEditView):
    queryset = DHCPServer.objects.all()
    form = DHCPServerForm


@register_model_view(DHCPServer, "delete")
class DHCPServerDeleteView(generic.ObjectDeleteView):
    queryset = DHCPServer.objects.all()


@register_model_view(DHCPServer, "bulk_import", detail=False)
class DHCPServerBulkImportView(generic.BulkImportView):
    queryset = DHCPServer.objects.all()
    model_form = DHCPServerImportForm
    table = DHCPServerTable


@register_model_view(DHCPServer, "bulk_edit", path="edit", detail=False)
class DHCPServerBulkEditView(generic.BulkEditView):
    queryset = DHCPServer.objects.all()
    filterset = DHCPServerFilterSet
    table = DHCPServerTable
    form = DHCPServerBulkEditForm


@register_model_view(DHCPServer, "bulk_delete", path="delete", detail=False)
class DHCPServerBulkDeleteView(generic.BulkDeleteView):
    queryset = DHCPServer.objects.all()
    filterset = DHCPServerFilterSet
    table = DHCPServerTable


@register_model_view(DHCPServer, "child_subnets")
class DHCPServerChildSubnetListView(generic.ObjectChildrenView):
    queryset = DHCPServer.objects.all()
    child_model = Subnet
    table = SubnetTable
    filterset = SubnetFilterSet
    template_name = "netbox_dhcp/dhcpserver/child_subnets.html"

    tab = ViewTab(
        label=_("Subnets"),
        permission="netbox_dhcp.view_subnet",
        badge=lambda obj: obj.child_subnets.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.child_subnets.restrict(request.user, "view")


@register_model_view(DHCPServer, "child_shared_networks")
class DHCPServerChildSharedNetworkListView(generic.ObjectChildrenView):
    queryset = DHCPServer.objects.all()
    child_model = SharedNetwork
    table = SharedNetworkTable
    filterset = SharedNetworkFilterSet
    template_name = "netbox_dhcp/dhcpserver/child_shared_networks.html"

    tab = ViewTab(
        label=_("Shared Networks"),
        permission="netbox_dhcp.view_sharednetwork",
        badge=lambda obj: obj.child_shared_networks.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.child_shared_networks.restrict(request.user, "view")


@register_model_view(DHCPServer, "child_host_reservations")
class DHCPServerChildHostReservationListView(generic.ObjectChildrenView):
    queryset = DHCPServer.objects.all()
    child_model = HostReservation
    table = HostReservationTable
    filterset = HostReservationFilterSet
    template_name = "netbox_dhcp/dhcpserver/child_host_reservations.html"

    tab = ViewTab(
        label=_("Host Reservations"),
        permission="netbox_dhcp.view_hostreservation",
        badge=lambda obj: obj.child_host_reservations.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.child_host_reservations.restrict(request.user, "view")


@register_model_view(DHCPServer, "client_classes")
class DHCPServerClientClassListView(generic.ObjectChildrenView):
    queryset = DHCPServer.objects.all()
    child_model = ClientClass
    table = ClientClassTable
    filterset = ClientClassFilterSet
    template_name = "netbox_dhcp/dhcpserver/client_classes.html"

    tab = ViewTab(
        label=_("Client Classes"),
        permission="netbox_dhcp.view_clientclass",
        badge=lambda obj: obj.client_class_definition_set.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.client_class_definition_set.restrict(request.user, "view")


@register_model_view(DHCPServer, "options")
class DHCPServerOptionListView(generic.ObjectChildrenView):
    queryset = DHCPServer.objects.all()
    child_model = Option
    table = ChildOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/dhcpserver/options.html"

    tab = ViewTab(
        label=_("Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.options.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.options.restrict(request.user, "view")


@register_model_view(DHCPServer, "option_definitions")
class DHCPServerOptionDefinitionListView(generic.ObjectChildrenView):
    queryset = DHCPServer.objects.all()
    child_model = OptionDefinition
    table = OptionDefinitionTable
    filterset = OptionDefinitionFilterSet
    template_name = "netbox_dhcp/dhcpserver/option_definitions.html"

    tab = ViewTab(
        label=_("Option Definitions"),
        permission="netbox_dhcp.view_optiondefinition",
        badge=lambda obj: obj.option_definitions.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.option_definitions.restrict(request.user, "view")
