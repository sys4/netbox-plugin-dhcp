from django.utils.translation import gettext_lazy as _

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem
from netbox.plugins.utils import get_plugin_config

menu_name = get_plugin_config("netbox_dhcp", "menu_name")
top_level_menu = get_plugin_config("netbox_dhcp", "top_level_menu")

dhcp_server_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:dhcpserver_list",
    link_text=_("DHCP Servers"),
    permissions=["netbox_dhcp.view_dhcpserver"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:dhcpserver_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_dhcpserver"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:dhcpserver_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_dhcpserver"],
        ),
    ),
)

dhcp_cluster_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:dhcpcluster_list",
    link_text=_("DHCP Clusters"),
    permissions=["netbox_dhcp.view_dhcpcluster"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:dhcpcluster_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_dhcpcluster"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:dhcpcluster_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_dhcpcluster"],
        ),
    ),
)

ddns_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:ddns_list",
    link_text=_("Dynamic DNS"),
    permissions=["netbox_dhcp.view_ddns"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:ddns_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_ddns"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:ddns_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_ddns"],
        ),
    ),
)

custom_option_definition_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:optiondefinition_list",
    link_text=_("Custom Option Definitions"),
    permissions=["netbox_dhcp.view_optiondefinition"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:optiondefinition_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_optiondefinition"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:optiondefinition_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_optiondefinition"],
        ),
    ),
)

standard_option_definition_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:optiondefinition_list_standard",
    link_text=_("Standard Option Definitions"),
    permissions=["netbox_dhcp.view_optiondefinition"],
)

option_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:option_list",
    link_text=_("Options"),
    permissions=["netbox_dhcp.option_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:option_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_option"],
        ),
    ),
)

client_class_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:clientclass_list",
    link_text=_("Client Classes"),
    permissions=["netbox_dhcp.view_clientclass"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:clientclass_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_clientclass"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:clientclass_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_clientclass"],
        ),
    ),
)

host_reservation_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:hostreservation_list",
    link_text=_("Host Reservations"),
    permissions=["netbox_dhcp.view_hostreservation"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:hostreservation_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_hostreservation"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:hostreservation_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_hostreservation"],
        ),
    ),
)

shared_netwok_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:sharednetwork_list",
    link_text=_("Shared Networks"),
    permissions=["netbox_dhcp.view_sharednetwork"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:sharednetwork_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_sharednetwork"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:sharednetwork_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_sharednetwork"],
        ),
    ),
)

subnet_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:subnet_list",
    link_text=_("Subnets"),
    permissions=["netbox_dhcp.view_subnet"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:subnet_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_subnet"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:subnet_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_subnet"],
        ),
    ),
)

pd_pool_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:pdpool_list",
    link_text=_("Prefix Delegation Pools"),
    permissions=["netbox_dhcp.view_pdpool"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:pdpool_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_pdpool"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:pdpool_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_pdpool"],
        ),
    ),
)

pool_menu_item = PluginMenuItem(
    link="plugins:netbox_dhcp:pool_list",
    link_text=_("Pools"),
    permissions=["netbox_dhcp.view_pool"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dhcp:pool_add",
            _("Add"),
            "mdi mdi-plus-thick",
            permissions=["netbox_dhcp.add_pool"],
        ),
        PluginMenuButton(
            "plugins:netbox_dhcp:pool_bulk_import",
            _("Import"),
            "mdi mdi-upload",
            permissions=["netbox_dhcp.add_pool"],
        ),
    ),
)


menu = PluginMenu(
    label=_("DHCP"),
    groups=(
        (
            _("Global"),
            (
                dhcp_server_menu_item,
                dhcp_cluster_menu_item,
            ),
        ),
        (
            _("Options"),
            (
                option_menu_item,
                standard_option_definition_menu_item,
                custom_option_definition_menu_item,
            ),
        ),
        (
            _("Network"),
            (
                shared_netwok_menu_item,
                subnet_menu_item,
                pd_pool_menu_item,
                pool_menu_item,
            ),
        ),
        (
            _("Clients"),
            (
                host_reservation_menu_item,
                client_class_menu_item,
            ),
        ),
    ),
    icon_class="mdi mdi-ethernet",
)
