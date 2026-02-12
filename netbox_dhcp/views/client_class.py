from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from netbox.views import generic
from utilities.views import register_model_view, ViewTab

from netbox_dhcp.models import (
    ClientClass,
    Option,
    OptionDefinition,
    DHCPServer,
    SharedNetwork,
    Subnet,
    PDPool,
    Pool,
    HostReservation,
)
from netbox_dhcp.filtersets import (
    ClientClassFilterSet,
    OptionFilterSet,
    OptionDefinitionFilterSet,
    SharedNetworkFilterSet,
    SubnetFilterSet,
    PDPoolFilterSet,
    PoolFilterSet,
    HostReservationFilterSet,
)
from netbox_dhcp.forms import (
    ClientClassForm,
    ClientClassFilterForm,
    ClientClassImportForm,
    ClientClassBulkEditForm,
)
from netbox_dhcp.tables import (
    ClientClassTable,
    ChildOptionTable,
    OptionDefinitionTable,
    ParentSharedNetworkTable,
    ParentSubnetTable,
    ParentPDPoolTable,
    ParentPoolTable,
    ParentHostReservationTable,
    ParentOptionTable,
)

__all__ = ()


@register_model_view(ClientClass, "list", path="", detail=False)
class ClientClassListView(generic.ObjectListView):
    queryset = ClientClass.objects.all()
    table = ClientClassTable
    filterset = ClientClassFilterSet
    filterset_form = ClientClassFilterForm


@register_model_view(ClientClass)
class ClientClassView(generic.ObjectView):
    queryset = ClientClass.objects.all()


@register_model_view(ClientClass, "add", detail=False)
@register_model_view(ClientClass, "edit")
class ClientClassEditView(generic.ObjectEditView):
    queryset = ClientClass.objects.all()
    form = ClientClassForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if not obj.pk:
            if "dhcp_server" in request.GET:
                obj.dhcp_server = get_object_or_404(
                    DHCPServer, pk=request.GET.get("dhcp_server")
                )

            obj.user = request.user

        return obj


@register_model_view(ClientClass, "delete")
class ClientClassDeleteView(generic.ObjectDeleteView):
    queryset = ClientClass.objects.all()


@register_model_view(ClientClass, "bulk_import", detail=False)
class ClientClassBulkImportView(generic.BulkImportView):
    queryset = ClientClass.objects.all()
    model_form = ClientClassImportForm
    table = ClientClassTable


@register_model_view(ClientClass, "bulk_edit", path="edit", detail=False)
class ClientClassBulkEditView(generic.BulkEditView):
    queryset = ClientClass.objects.all()
    filterset = ClientClassFilterSet
    table = ClientClassTable
    form = ClientClassBulkEditForm


@register_model_view(ClientClass, "bulk_delete", path="delete", detail=False)
class ClientClassBulkDeleteView(generic.BulkDeleteView):
    queryset = ClientClass.objects.all()
    filterset = ClientClassFilterSet
    table = ClientClassTable


@register_model_view(ClientClass, "options")
class ClientClassOptionListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = Option
    table = ChildOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/clientclass/options.html"

    tab = ViewTab(
        label=_("Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.options.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.options.restrict(request.user, "view")


@register_model_view(ClientClass, "option_definitions")
class ClientClassOptionDefinitionListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = OptionDefinition
    table = OptionDefinitionTable
    filterset = OptionDefinitionFilterSet
    template_name = "netbox_dhcp/clientclass/option_definitions.html"

    tab = ViewTab(
        label=_("Option Definitions"),
        permission="netbox_dhcp.view_optiondefinition",
        badge=lambda obj: obj.option_definitions.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.option_definitions.restrict(request.user, "view")


@register_model_view(ClientClass, "parent_options")
class ClientClassParentOptionListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = Option
    table = ParentOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/clientclass/parent_options.html"
    actions = {"export": {"view"}}

    tab = ViewTab(
        label=_("Parent Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.option_set.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.option_set.restrict(request.user, "view")


@register_model_view(ClientClass, "parent_shared_networks")
class ClientClassParentSharedNetworkListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = SharedNetwork
    table = ParentSharedNetworkTable
    filterset = SharedNetworkFilterSet
    template_name = "netbox_dhcp/clientclass/parent_shared_networks.html"
    actions = {"export": {"view"}}

    tab = ViewTab(
        label=_("Parent Shared Networks"),
        permission="netbox_dhcp.view_sharednetwork",
        badge=lambda obj: obj.sharednetwork_set.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.sharednetwork_set.restrict(request.user, "view")


@register_model_view(ClientClass, "parent_subnets")
class ClientClassParentSubnetListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = Subnet
    table = ParentSubnetTable
    filterset = SubnetFilterSet
    template_name = "netbox_dhcp/clientclass/parent_subnets.html"
    actions = {"export": {"view"}}

    tab = ViewTab(
        label=_("Parent Subnets"),
        permission="netbox_dhcp.view_subnet",
        badge=lambda obj: obj.subnet_set.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.subnet_set.restrict(request.user, "view")


@register_model_view(ClientClass, "parent_pd_pools")
class ClientClassParentPDPoolListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = PDPool
    table = ParentPDPoolTable
    filterset = PDPoolFilterSet
    template_name = "netbox_dhcp/clientclass/parent_pd_pools.html"
    actions = {"export": {"view"}}

    tab = ViewTab(
        label=_("Parent Prefix Delegation Pools"),
        permission="netbox_dhcp.view_pdpool",
        badge=lambda obj: obj.pdpool_set.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.pdpool_set.restrict(request.user, "view")


@register_model_view(ClientClass, "parent_pools")
class ClientClassParentPoolListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = Pool
    table = ParentPoolTable
    filterset = PoolFilterSet
    template_name = "netbox_dhcp/clientclass/parent_pools.html"
    actions = {"export": {"view"}}

    tab = ViewTab(
        label=_("Parent Pools"),
        permission="netbox_dhcp.view_pool",
        badge=lambda obj: obj.pool_set.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.pool_set.restrict(request.user, "view")


@register_model_view(ClientClass, "parent_host_reservations")
class ClientClassParentHostReservationListView(generic.ObjectChildrenView):
    queryset = ClientClass.objects.all()
    child_model = HostReservation
    table = ParentHostReservationTable
    filterset = HostReservationFilterSet
    template_name = "netbox_dhcp/clientclass/parent_host_reservations.html"
    actions = {"export": {"view"}}

    tab = ViewTab(
        label=_("Parent Host Reservations"),
        permission="netbox_dhcp.view_hostreservation",
        badge=lambda obj: obj.hostreservation_set.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.hostreservation_set.restrict(request.user, "view")
