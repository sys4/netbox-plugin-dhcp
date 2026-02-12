from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from utilities.views import register_model_view, ViewTab

from netbox_dhcp.models import OptionDefinition, Option
from netbox_dhcp.filtersets import OptionDefinitionFilterSet, OptionFilterSet
from netbox_dhcp.forms import (
    OptionDefinitionForm,
    OptionDefinitionFilterForm,
    OptionDefinitionImportForm,
    OptionDefinitionBulkEditForm,
)
from netbox_dhcp.tables import (
    OptionDefinitionTable,
    StandardOptionDefinitionTable,
    ChildOptionTable,
)

__all__ = (
    "OptionDefinitionView",
    "OptionDefinitionListView",
    "OptionDefinitionEditView",
    "OptionDefinitionDeleteView",
    "OptionDefinitionBulkImportView",
    "OptionDefinitionBulkEditView",
    "OptionDefinitionBulkDeleteView",
    "StandardOptionDefinitionListView",
    "OptionDefinitionOptionsListView",
)


@register_model_view(OptionDefinition, "list_standard", path="standard", detail=False)
class StandardOptionDefinitionListView(generic.ObjectListView):
    queryset = OptionDefinition.objects.filter(standard=True)
    table = StandardOptionDefinitionTable
    filterset = OptionDefinitionFilterSet
    filterset_form = OptionDefinitionFilterForm
    actions = {"export": {"view"}}
    template_name = "netbox_dhcp/optiondefinition/standard.html"


@register_model_view(OptionDefinition, "list", path="custom", detail=False)
class OptionDefinitionListView(generic.ObjectListView):
    queryset = OptionDefinition.objects.filter(standard=False)
    table = OptionDefinitionTable
    filterset = OptionDefinitionFilterSet
    filterset_form = OptionDefinitionFilterForm
    template_name = "netbox_dhcp/optiondefinition/custom.html"


@register_model_view(OptionDefinition)
class OptionDefinitionView(generic.ObjectView):
    queryset = OptionDefinition.objects.all()


@register_model_view(OptionDefinition, "add", detail=False)
@register_model_view(OptionDefinition, "edit")
class OptionDefinitionEditView(generic.ObjectEditView):
    queryset = OptionDefinition.objects.all()
    form = OptionDefinitionForm


@register_model_view(OptionDefinition, "delete")
class OptionDefinitionDeleteView(generic.ObjectDeleteView):
    queryset = OptionDefinition.objects.all()


@register_model_view(OptionDefinition, "bulk_import", detail=False)
class OptionDefinitionBulkImportView(generic.BulkImportView):
    queryset = OptionDefinition.objects.all()
    model_form = OptionDefinitionImportForm
    table = OptionDefinitionTable


@register_model_view(OptionDefinition, "bulk_edit", path="edit", detail=False)
class OptionDefinitionBulkEditView(generic.BulkEditView):
    queryset = OptionDefinition.objects.all()
    filterset = OptionDefinitionFilterSet
    table = OptionDefinitionTable
    form = OptionDefinitionBulkEditForm


@register_model_view(OptionDefinition, "bulk_delete", path="delete", detail=False)
class OptionDefinitionBulkDeleteView(generic.BulkDeleteView):
    queryset = OptionDefinition.objects.all()
    filterset = OptionDefinitionFilterSet
    table = OptionDefinitionTable


@register_model_view(OptionDefinition, "options")
class OptionDefinitionOptionsListView(generic.ObjectChildrenView):
    queryset = OptionDefinition.objects.all()
    child_model = Option
    table = ChildOptionTable
    filterset = OptionFilterSet
    template_name = "netbox_dhcp/optiondefinition/options.html"

    tab = ViewTab(
        label=_("Options"),
        permission="netbox_dhcp.view_option",
        badge=lambda obj: obj.options.count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return parent.options.restrict(request.user, "view")
