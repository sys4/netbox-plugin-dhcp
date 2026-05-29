from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from netbox_dhcp.filtersets import OptionFilterSet, PoolFilterSet
from netbox_dhcp.forms import (
    PoolBulkEditForm,
    PoolFilterForm,
    PoolForm,
    PoolImportForm,
)
from netbox_dhcp.models import Option, Pool
from netbox_dhcp.tables import ChildOptionTable, PoolTable
from utilities.views import ViewTab, register_model_view

__all__ = (
    "PoolView",
    "PoolListView",
    "PoolEditView",
    "PoolDeleteView",
    "PoolBulkImportView",
    "PoolBulkEditView",
    "PoolOptionsListView",
)


@register_model_view(Pool, "list", path="", detail=False)
class PoolListView(generic.ObjectListView):
    queryset = Pool.objects.all()
    table = PoolTable
    filterset = PoolFilterSet
    filterset_form = PoolFilterForm


@register_model_view(Pool)
class PoolView(generic.ObjectView):
    queryset = Pool.objects.all()


@register_model_view(Pool, "add", detail=False)
@register_model_view(Pool, "edit")
class PoolEditView(generic.ObjectEditView):
    queryset = Pool.objects.all()
    form = PoolForm


@register_model_view(Pool, "delete")
class PoolDeleteView(generic.ObjectDeleteView):
    queryset = Pool.objects.all()


@register_model_view(Pool, "bulk_import", detail=False)
class PoolBulkImportView(generic.BulkImportView):
    queryset = Pool.objects.all()
    model_form = PoolImportForm
    table = PoolTable


@register_model_view(Pool, "bulk_edit", path="edit", detail=False)
class PoolBulkEditView(generic.BulkEditView):
    queryset = Pool.objects.all()
    filterset = PoolFilterSet
    table = PoolTable
    form = PoolBulkEditForm


@register_model_view(Pool, "bulk_delete", path="delete", detail=False)
class PoolBulkDeleteView(generic.BulkDeleteView):
    queryset = Pool.objects.all()
    filterset = PoolFilterSet
    table = PoolTable


@register_model_view(Pool, "options")
class PoolOptionsListView(generic.ObjectChildrenView):
    queryset = Pool.objects.all()
    child_model = Option
    table = ChildOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/pool/options.html"

    tab = ViewTab(
        label=_("Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.options.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.options.restrict(request.user, "view")
