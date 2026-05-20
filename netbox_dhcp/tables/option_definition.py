import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import PrimaryModelTable, TemplateColumn
from netbox_dhcp.models import OptionDefinition

from .mixins import NetBoxDHCPTableMixin

__all__ = (
    "OptionDefinitionTable",
    "StandardOptionDefinitionTable",
)


class OptionDefinitionTable(NetBoxDHCPTableMixin, PrimaryModelTable):
    class Meta(PrimaryModelTable.Meta):
        model = OptionDefinition

        fields = (
            "name",
            "space",
            "family",
            "code",
            "description",
            "type",
            "record_types",
            "encapsulate",
            "array",
        )

        default_columns = (
            "name",
            "space",
            "family",
            "code",
        )

    dhcp_server = tables.Column(
        verbose_name=_("DHCP Server"),
        linkify=True,
    )
    client_class = tables.Column(
        verbose_name=_("Client Class"),
        linkify=True,
    )

    code = tables.Column(
        verbose_name=_("Option Code"),
    )
    record_types = TemplateColumn(
        verbose_name=_("Record Types"),
        template_code="{% for record_type in value %}{{ record_type }}&nbsp;{% endfor %}",
    )


class StandardOptionDefinitionTable(OptionDefinitionTable):
    class Meta(OptionDefinitionTable.Meta):
        pass

    actions = None
