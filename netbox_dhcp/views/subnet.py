from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from utilities.views import register_model_view, ViewTab

from netbox_dhcp.models import Subnet, Pool, PDPool, HostReservation, Option
from netbox_dhcp.filtersets import (
    SubnetFilterSet,
    PoolFilterSet,
    PDPoolFilterSet,
    HostReservationFilterSet,
    OptionFilterSet,
)
from netbox_dhcp.forms import (
    SubnetForm,
    SubnetFilterForm,
    SubnetImportForm,
    SubnetBulkEditForm,
)
from netbox_dhcp.tables import (
    SubnetTable,
    PoolTable,
    PDPoolTable,
    HostReservationTable,
    ChildOptionTable,
)

__all__ = (
    "SubnetView",
    "SubnetListView",
    "SubnetEditView",
    "SubnetDeleteView",
    "SubnetBulkImportView",
    "SubnetBulkEditView",
    "SubnetBulkDeleteView",
    "SubnetChildPoolListView",
    "SubnetChildPDPoolListView",
    "SubnetChildHostReservationListView",
    "SubnetOptionsListView",
)


@register_model_view(Subnet, "list", path="", detail=False)
class SubnetListView(generic.ObjectListView):
    queryset = Subnet.objects.all()
    table = SubnetTable
    filterset = SubnetFilterSet
    filterset_form = SubnetFilterForm


@register_model_view(Subnet)
class SubnetView(generic.ObjectView):
    queryset = Subnet.objects.all()


@register_model_view(Subnet, "add", detail=False)
@register_model_view(Subnet, "edit")
class SubnetEditView(generic.ObjectEditView):
    queryset = Subnet.objects.all()
    form = SubnetForm


@register_model_view(Subnet, "delete")
class SubnetDeleteView(generic.ObjectDeleteView):
    queryset = Subnet.objects.all()


@register_model_view(Subnet, "bulk_import", detail=False)
class SubnetBulkImportView(generic.BulkImportView):
    queryset = Subnet.objects.all()
    model_form = SubnetImportForm
    table = SubnetTable


@register_model_view(Subnet, "bulk_edit", path="edit", detail=False)
class SubnetBulkEditView(generic.BulkEditView):
    queryset = Subnet.objects.all()
    filterset = SubnetFilterSet
    table = SubnetTable
    form = SubnetBulkEditForm


@register_model_view(Subnet, "bulk_delete", path="delete", detail=False)
class SubnetBulkDeleteView(generic.BulkDeleteView):
    queryset = Subnet.objects.all()
    filterset = SubnetFilterSet
    table = SubnetTable


@register_model_view(Subnet, "child_pools")
class SubnetChildPoolListView(generic.ObjectChildrenView):
    queryset = Subnet.objects.all()
    child_model = Pool
    table = PoolTable
    filterset = PoolFilterSet
    template_name = "netbox_dhcp/subnet/child_pools.html"

    tab = ViewTab(
        label=_("Pools"),
        permission="netbox_dhcp.view_pool",
        badge=lambda obj: obj.child_pools.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.child_pools.restrict(request.user, "view")


@register_model_view(Subnet, "child_pd_pools")
class SubnetChildPDPoolListView(generic.ObjectChildrenView):
    queryset = Subnet.objects.all()
    child_model = PDPool
    table = PDPoolTable
    filterset = PDPoolFilterSet
    template_name = "netbox_dhcp/subnet/child_pd_pools.html"

    tab = ViewTab(
        label=_("Prefix Delegation Pools"),
        permission="netbox_dhcp.view_pdpool",
        badge=lambda obj: obj.child_pd_pools.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.child_pd_pools.restrict(request.user, "view")


@register_model_view(Subnet, "child_host_reservations")
class SubnetChildHostReservationListView(generic.ObjectChildrenView):
    queryset = Subnet.objects.all()
    child_model = HostReservation
    table = HostReservationTable
    filterset = HostReservationFilterSet
    template_name = "netbox_dhcp/subnet/child_host_reservations.html"

    tab = ViewTab(
        label=_("Host Reservations"),
        permission="netbox_dhcp.view_hostreservation",
        badge=lambda obj: obj.child_host_reservations.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.child_host_reservations.restrict(request.user, "view")


@register_model_view(Subnet, "options")
class SubnetOptionsListView(generic.ObjectChildrenView):
    queryset = Subnet.objects.all()
    child_model = Option
    table = ChildOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/subnet/options.html"

    tab = ViewTab(
        label=_("Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.options.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.options.restrict(request.user, "view")
