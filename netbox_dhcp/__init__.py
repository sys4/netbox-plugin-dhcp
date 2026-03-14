from django.utils.translation import gettext_lazy as _

from netbox.plugins import PluginConfig

__version__ = "0.1.5"


class DHCPConfig(PluginConfig):
    name = "netbox_dhcp"
    verbose_name = _("NetBox DHCP")
    description = _("NetBox plugin for DHCP")
    min_version = "4.5.0"
    version = __version__
    author = "Peter Eckel, sys4 AG"
    author_email = "pe@sys4.de"
    required_settings = []
    default_settings = {}
    base_url = "netbox-dhcp"

    def ready(self):
        super().ready()

        from netbox_dhcp.signals import dhcp_server  # noqa: F401


#
# Initialize plugin config
#
config = DHCPConfig
