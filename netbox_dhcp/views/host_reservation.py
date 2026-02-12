from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from utilities.views import register_model_view, ViewTab

from netbox_dhcp.models import HostReservation, Option
from netbox_dhcp.filtersets import HostReservationFilterSet, OptionFilterSet
from netbox_dhcp.forms import (
    HostReservationForm,
    HostReservationFilterForm,
    HostReservationImportForm,
    HostReservationBulkEditForm,
)
from netbox_dhcp.tables import HostReservationTable, ChildOptionTable

__all__ = (
    "HostReservationView",
    "HostReservationListView",
    "HostReservationEditView",
    "HostReservationDeleteView",
    "HostReservationBulkImportView",
    "HostReservationBulkEditView",
    "HostReservationBulkDeleteView",
    "HostReservationOptionsListView",
)


@register_model_view(HostReservation, "list", path="", detail=False)
class HostReservationListView(generic.ObjectListView):
    queryset = HostReservation.objects.all()
    table = HostReservationTable
    filterset = HostReservationFilterSet
    filterset_form = HostReservationFilterForm


@register_model_view(HostReservation)
class HostReservationView(generic.ObjectView):
    queryset = HostReservation.objects.all()


@register_model_view(HostReservation, "add", detail=False)
@register_model_view(HostReservation, "edit")
class HostReservationEditView(generic.ObjectEditView):
    queryset = HostReservation.objects.all()
    form = HostReservationForm


@register_model_view(HostReservation, "delete")
class HostReservationDeleteView(generic.ObjectDeleteView):
    queryset = HostReservation.objects.all()


@register_model_view(HostReservation, "bulk_import", detail=False)
class HostReservationBulkImportView(generic.BulkImportView):
    queryset = HostReservation.objects.all()
    model_form = HostReservationImportForm
    table = HostReservationTable


@register_model_view(HostReservation, "bulk_edit", path="edit", detail=False)
class HostReservationBulkEditView(generic.BulkEditView):
    queryset = HostReservation.objects.all()
    filterset = HostReservationFilterSet
    table = HostReservationTable
    form = HostReservationBulkEditForm


@register_model_view(HostReservation, "bulk_delete", path="delete", detail=False)
class HostReservationBulkDeleteView(generic.BulkDeleteView):
    queryset = HostReservation.objects.all()
    filterset = HostReservationFilterSet
    table = HostReservationTable


@register_model_view(HostReservation, "options")
class HostReservationOptionsListView(generic.ObjectChildrenView):
    queryset = HostReservation.objects.all()
    child_model = Option
    table = ChildOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/hostreservation/options.html"

    tab = ViewTab(
        label=_("Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.options.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.options.restrict(request.user, "view")
