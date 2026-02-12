from netbox.views import generic
from utilities.views import register_model_view

from netbox_dhcp.models import DHCPCluster
from netbox_dhcp.filtersets import DHCPClusterFilterSet
from netbox_dhcp.forms import (
    DHCPClusterForm,
    DHCPClusterFilterForm,
    DHCPClusterImportForm,
    DHCPClusterBulkEditForm,
)
from netbox_dhcp.tables import DHCPClusterTable

__all__ = (
    "DHCPClusterView",
    "DHCPClusterListView",
    "DHCPClusterEditView",
    "DHCPClusterDeleteView",
    "DHCPClusterBulkImportView",
    "DHCPClusterBulkEditView",
    "DHCPClusterBulkDeleteView",
)


@register_model_view(DHCPCluster, "list", path="", detail=False)
class DHCPClusterListView(generic.ObjectListView):
    queryset = DHCPCluster.objects.all()
    table = DHCPClusterTable
    filterset = DHCPClusterFilterSet
    filterset_form = DHCPClusterFilterForm


@register_model_view(DHCPCluster)
class DHCPClusterView(generic.ObjectView):
    queryset = DHCPCluster.objects.all()


@register_model_view(DHCPCluster, "add", detail=False)
@register_model_view(DHCPCluster, "edit")
class DHCPClusterEditView(generic.ObjectEditView):
    queryset = DHCPCluster.objects.all()
    form = DHCPClusterForm


@register_model_view(DHCPCluster, "delete")
class DHCPClusterDeleteView(generic.ObjectDeleteView):
    queryset = DHCPCluster.objects.all()


@register_model_view(DHCPCluster, "bulk_import", detail=False)
class DHCPClusterBulkImportView(generic.BulkImportView):
    queryset = DHCPCluster.objects.all()
    model_form = DHCPClusterImportForm
    table = DHCPClusterTable


@register_model_view(DHCPCluster, "bulk_edit", path="edit", detail=False)
class DHCPClusterBulkEditView(generic.BulkEditView):
    queryset = DHCPCluster.objects.all()
    filterset = DHCPClusterFilterSet
    table = DHCPClusterTable
    form = DHCPClusterBulkEditForm


@register_model_view(DHCPCluster, "bulk_delete", path="delete", detail=False)
class DHCPClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = DHCPCluster.objects.all()
    filterset = DHCPClusterFilterSet
    table = DHCPClusterTable
