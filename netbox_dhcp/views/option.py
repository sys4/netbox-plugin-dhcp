from netbox.views import generic
from utilities.views import register_model_view

from netbox_dhcp.models import (
    Option,
    DHCPServer,
    Subnet,
    SharedNetwork,
    Pool,
    PDPool,
    HostReservation,
    ClientClass,
)
from netbox_dhcp.filtersets import OptionFilterSet
from netbox_dhcp.forms import (
    OptionForm,
    OptionFilterForm,
    OptionImportForm,
    OptionBulkEditForm,
)
from netbox_dhcp.tables import OptionTable

__all__ = (
    "OptionView",
    "OptionListView",
    "OptionEditView",
    "OptionDeleteView",
    "OptionBulkImportView",
    "OptionBulkEditView",
    "OptionBulkDeleteView",
)


@register_model_view(Option, "list", path="", detail=False)
class OptionListView(generic.ObjectListView):
    queryset = Option.objects.all()
    table = OptionTable
    actions = {
        "export": {"view"},
        "bulk_import": {"change"},
        "bulk_edit": {"change"},
        "bulk_delete": {"delete"},
    }
    filterset = OptionFilterSet
    filterset_form = OptionFilterForm


@register_model_view(Option)
class OptionView(generic.ObjectView):
    queryset = Option.objects.all()


@register_model_view(Option, "add", detail=False)
@register_model_view(Option, "edit")
class OptionEditView(generic.ObjectEditView):
    queryset = Option.objects.all()
    form = OptionForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if "dhcp_server" in request.GET:
            try:
                obj.assigned_object = DHCPServer.objects.get(
                    pk=request.GET["dhcp_server"]
                )
            except (ValueError, DHCPServer.DoesNotExist):
                pass

        if "subnet" in request.GET:
            try:
                obj.assigned_object = Subnet.objects.get(pk=request.GET["subnet"])
            except (ValueError, Subnet.DoesNotExist):
                pass

        if "shared_network" in request.GET:
            try:
                obj.assigned_object = SharedNetwork.objects.get(
                    pk=request.GET["shared_network"]
                )
            except (ValueError, SharedNetwork.DoesNotExist):
                pass

        if "pool" in request.GET:
            try:
                obj.assigned_object = Pool.objects.get(pk=request.GET["pool"])
            except (ValueError, Pool.DoesNotExist):
                pass

        if "pd_pool" in request.GET:
            try:
                obj.assigned_object = PDPool.objects.get(pk=request.GET["pd_pool"])
            except (ValueError, PDPool.DoesNotExist):
                pass

        if "host_reservation" in request.GET:
            try:
                obj.assigned_object = HostReservation.objects.get(
                    pk=request.GET["host_reservation"]
                )
            except (ValueError, HostReservation.DoesNotExist):
                pass

        if "client_class" in request.GET:
            try:
                obj.assigned_object = ClientClass.objects.get(
                    pk=request.GET["client_class"]
                )
            except (ValueError, ClientClass.DoesNotExist):
                pass

        return obj

    def get_extra_addanother_params(self, request):
        for parameter in (
            "dhcp_server",
            "subnet",
            "shared_network",
            "pool",
            "pd_pool",
            "host_reservation",
            "client_class",
        ):
            if parameter in request.GET:
                return {parameter: request.GET[parameter]}

        return {}


@register_model_view(Option, "delete")
class OptionDeleteView(generic.ObjectDeleteView):
    queryset = Option.objects.all()


@register_model_view(Option, "bulk_import", detail=False)
class OptionBulkImportView(generic.BulkImportView):
    queryset = Option.objects.all()
    model_form = OptionImportForm
    table = OptionTable


@register_model_view(Option, "bulk_edit", path="edit", detail=False)
class OptionBulkEditView(generic.BulkEditView):
    queryset = Option.objects.all()
    filterset = OptionFilterSet
    table = OptionTable
    form = OptionBulkEditForm


@register_model_view(Option, "bulk_delete", path="delete", detail=False)
class OptionBulkDeleteView(generic.BulkDeleteView):
    queryset = Option.objects.all()
    filterset = OptionFilterSet
    table = OptionTable
