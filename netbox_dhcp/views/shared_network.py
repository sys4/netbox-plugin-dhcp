from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from utilities.views import register_model_view, ViewTab

from netbox_dhcp.models import SharedNetwork, Subnet, Option
from netbox_dhcp.filtersets import (
    SharedNetworkFilterSet,
    SubnetFilterSet,
    OptionFilterSet,
)
from netbox_dhcp.forms import (
    SharedNetworkForm,
    SharedNetworkFilterForm,
    SharedNetworkImportForm,
    SharedNetworkBulkEditForm,
)
from netbox_dhcp.tables import SharedNetworkTable, SubnetTable, ChildOptionTable

__all__ = (
    "SharedNetworkView",
    "SharedNetworkListView",
    "SharedNetworkEditView",
    "SharedNetworkDeleteView",
    "SharedNetworkBulkImportView",
    "SharedNetworkBulkEditView",
    "SharedNetworkBulkDeleteView",
    "SharedNetworkChildSubnetListView",
    "SharedNetworkOptionsListView",
)


@register_model_view(SharedNetwork, "list", path="", detail=False)
class SharedNetworkListView(generic.ObjectListView):
    queryset = SharedNetwork.objects.all()
    table = SharedNetworkTable
    filterset = SharedNetworkFilterSet
    filterset_form = SharedNetworkFilterForm


@register_model_view(SharedNetwork)
class SharedNetworkView(generic.ObjectView):
    queryset = SharedNetwork.objects.all()


@register_model_view(SharedNetwork, "add", detail=False)
@register_model_view(SharedNetwork, "edit")
class SharedNetworkEditView(generic.ObjectEditView):
    queryset = SharedNetwork.objects.all()
    form = SharedNetworkForm


@register_model_view(SharedNetwork, "delete")
class SharedNetworkDeleteView(generic.ObjectDeleteView):
    queryset = SharedNetwork.objects.all()


@register_model_view(SharedNetwork, "bulk_import", detail=False)
class SharedNetworkBulkImportView(generic.BulkImportView):
    queryset = SharedNetwork.objects.all()
    model_form = SharedNetworkImportForm
    table = SharedNetworkTable


@register_model_view(SharedNetwork, "bulk_edit", path="edit", detail=False)
class SharedNetworkBulkEditView(generic.BulkEditView):
    queryset = SharedNetwork.objects.all()
    filterset = SharedNetworkFilterSet
    table = SharedNetworkTable
    form = SharedNetworkBulkEditForm


@register_model_view(SharedNetwork, "bulk_delete", path="delete", detail=False)
class SharedNetworkBulkDeleteView(generic.BulkDeleteView):
    queryset = SharedNetwork.objects.all()
    filterset = SharedNetworkFilterSet
    table = SharedNetworkTable


@register_model_view(SharedNetwork, "child_subnets")
class SharedNetworkChildSubnetListView(generic.ObjectChildrenView):
    queryset = SharedNetwork.objects.all()
    child_model = Subnet
    table = SubnetTable
    filterset = SubnetFilterSet
    template_name = "netbox_dhcp/sharednetwork/child_subnets.html"

    tab = ViewTab(
        label=_("Child Subnets"),
        permission="netbox_dhcp.view_subnet",
        badge=lambda obj: obj.child_subnets.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.child_subnets.restrict(request.user, "view")


@register_model_view(SharedNetwork, "options")
class SharedNetworkOptionsListView(generic.ObjectChildrenView):
    queryset = SharedNetwork.objects.all()
    child_model = Option
    table = ChildOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/sharednetwork/options.html"

    tab = ViewTab(
        label=_("Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.options.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.options.restrict(request.user, "view")
