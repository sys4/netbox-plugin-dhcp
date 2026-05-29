# from django.utils.translation import gettext_lazy as _

from ipam.choices import IPAddressFamilyChoices
from netbox.plugins import PluginTemplateExtension
from netbox_dhcp.tables import (
    RelatedHostReservationTable,
    RelatedPDPoolTable,
    RelatedPoolTable,
    RelatedSharedNetworkTable,
    RelatedSubnetTable,
)


class RelatedHostReservations(PluginTemplateExtension):
    models = ("ipam.ipaddress",)

    def right_page(self):
        ip_address = self.context.get("object")
        request = self.context.get("request")

        if ip_address.family == IPAddressFamilyChoices.FAMILY_4:
            host_reservations = ip_address.netbox_dhcp_ipv4_host_reservations.all()
        else:
            host_reservations = ip_address.netbox_dhcp_ipv6_host_reservations.all()

        if host_reservations:
            host_reservation_table = RelatedHostReservationTable(
                data=host_reservations,
            )
            host_reservation_table.configure(request)
        else:
            host_reservation_table = None

        return self.render(
            "netbox_dhcp/hostreservation/related.html",
            extra_context={
                "host_reservations": host_reservation_table,
            },
        )


class RelatedMACAddressHostReservations(PluginTemplateExtension):
    models = ("dcim.macaddress",)

    def right_page(self):
        hw_address = self.context.get("object")
        request = self.context.get("request")

        host_reservations = hw_address.netbox_dhcp_host_reservations.all()

        if host_reservations:
            host_reservation_table = RelatedHostReservationTable(
                data=host_reservations,
            )
            host_reservation_table.configure(request)
        else:
            host_reservation_table = None

        return self.render(
            "netbox_dhcp/hostreservation/related.html",
            extra_context={
                "host_reservations": host_reservation_table,
            },
        )


class RelatedSharedNetworks(PluginTemplateExtension):
    models = ("ipam.prefix",)

    def right_page(self):
        prefix = self.context.get("object")
        request = self.context.get("request")

        if shared_networks := prefix.netbox_dhcp_shared_networks.all():
            shared_network_table = RelatedSharedNetworkTable(
                data=shared_networks,
            )
            shared_network_table.configure(request)
        else:
            shared_network_table = None

        return self.render(
            "netbox_dhcp/sharednetwork/related.html",
            extra_context={
                "shared_networks": shared_network_table,
            },
        )


class RelatedSubnets(PluginTemplateExtension):
    models = ("ipam.prefix",)

    def right_page(self):
        prefix = self.context.get("object")
        request = self.context.get("request")

        if subnets := prefix.netbox_dhcp_subnets.all():
            subnet_table = RelatedSubnetTable(
                data=subnets,
            )
            subnet_table.configure(request)
        else:
            subnet_table = None

        return self.render(
            "netbox_dhcp/subnet/related.html",
            extra_context={
                "subnets": subnet_table,
            },
        )


class RelatedPools(PluginTemplateExtension):
    models = ("ipam.iprange",)

    def right_page(self):
        ip_range = self.context.get("object")
        request = self.context.get("request")

        if pools := ip_range.netbox_dhcp_pools.all():
            pool_table = RelatedPoolTable(
                data=pools,
            )
            pool_table.configure(request)
        else:
            pool_table = None

        return self.render(
            "netbox_dhcp/pool/related.html",
            extra_context={
                "pools": pool_table,
            },
        )


class RelatedPDPools(PluginTemplateExtension):
    models = ("ipam.prefix",)

    def right_page(self):
        prefix = self.context.get("object")
        request = self.context.get("request")

        if pd_pools := prefix.netbox_dhcp_pd_pools.all():
            pd_pool_table = RelatedPDPoolTable(
                data=pd_pools,
            )
            pd_pool_table.configure(request)
        else:
            pd_pool_table = None

        return self.render(
            "netbox_dhcp/pdpool/related.html",
            extra_context={
                "pd_pools": pd_pool_table,
            },
        )


template_extensions = [
    RelatedHostReservations,
    RelatedMACAddressHostReservations,
    RelatedSharedNetworks,
    RelatedSubnets,
    RelatedPools,
    RelatedPDPools,
]
