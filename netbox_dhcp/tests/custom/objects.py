from netaddr import IPNetwork

from ipam.models import IPAddress, IPRange, Prefix
from dcim.models import Device, Manufacturer, DeviceRole, DeviceType, Site, MACAddress
from virtualization.models import VirtualMachine, Cluster, ClusterType

from netbox_dhcp.models import DHCPCluster, DHCPServer, ClientClass

__all__ = ("TestObjects",)


class TestObjects:
    @staticmethod
    def get_ipv4_addresses():
        ipv4_addresses = (
            IPAddress(address="198.18.0.1/24"),
            IPAddress(address="198.18.0.2/24"),
            IPAddress(address="198.18.0.3/24"),
        )
        IPAddress.objects.bulk_create(ipv4_addresses)

        return ipv4_addresses

    @staticmethod
    def get_ipv6_addresses():
        ipv6_addresses = (
            IPAddress(address="2001:db8::1/64"),
            IPAddress(address="2001:db8::2/64"),
            IPAddress(address="2001:db8::3/64"),
        )
        IPAddress.objects.bulk_create(ipv6_addresses)

        return ipv6_addresses

    @staticmethod
    def get_ipv4_prefixes(offset=0):
        ipv4_prefixes = (
            Prefix(prefix=IPNetwork("198.18.0.0/16")),
            Prefix(prefix=IPNetwork(f"198.18.{offset}.0/24")),
            Prefix(prefix=IPNetwork(f"198.18.{1 + offset}.0/24")),
            Prefix(prefix=IPNetwork(f"198.18.{2 + offset}.0/24")),
        )
        Prefix.objects.bulk_create(ipv4_prefixes)

        return ipv4_prefixes

    @staticmethod
    def get_ipv6_prefixes(offset=0):
        ipv6_prefixes = (
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}::/32")),
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}:1::/64")),
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}:2::/64")),
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}:3::/64")),
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}:1:0:1::/96")),
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}:1:0:2::/96")),
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}:2:0:1::/96")),
            Prefix(prefix=IPNetwork(f"2001:db8:{offset}:2:0:2::/96")),
        )
        Prefix.objects.bulk_create(ipv6_prefixes)

        return ipv6_prefixes

    @staticmethod
    def get_ipv4_ranges():
        ipv4_ranges = (
            IPRange(
                start_address=IPNetwork("198.18.2.1/24"),
                end_address=IPNetwork("198.18.2.16/24"),
                size=16,
            ),
            IPRange(
                start_address=IPNetwork("198.18.2.17/24"),
                end_address=IPNetwork("198.18.2.32/24"),
                size=16,
            ),
            IPRange(
                start_address=IPNetwork("198.18.2.33/24"),
                end_address=IPNetwork("198.18.2.64/24"),
                size=32,
            ),
        )
        IPRange.objects.bulk_create(ipv4_ranges)

        return ipv4_ranges

    @staticmethod
    def get_ipv6_ranges():
        ipv6_ranges = (
            IPRange(
                start_address=IPNetwork("2001:db8:0:1::1/64"),
                end_address=IPNetwork("2001:db8:0:1::ffff/64"),
                size=65535,
            ),
            IPRange(
                start_address=IPNetwork("2001:db8:0:1::1:1/64"),
                end_address=IPNetwork("2001:db8:0:1::1:ffff/64"),
                size=65535,
            ),
            IPRange(
                start_address=IPNetwork("2001:db8:0:1::2:1/64"),
                end_address=IPNetwork("2001:db8:0:1::3:ffff/64"),
                size=131071,
            ),
        )
        IPRange.objects.bulk_create(ipv6_ranges)

        return ipv6_ranges

    @staticmethod
    def get_devices():
        site = Site.objects.create(name="test-site")
        manufacturer = Manufacturer.objects.create(name="ACME")
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model="ACME 42", slug="acme-42"
        )
        device_role = DeviceRole.objects.create(name="Null Device")

        devices = (
            Device(
                name="device-1",
                role=device_role,
                device_type=device_type,
                site=site,
            ),
            Device(
                name="device-2",
                role=device_role,
                device_type=device_type,
                site=site,
            ),
            Device(
                name="device-3",
                role=device_role,
                device_type=device_type,
                site=site,
            ),
        )

        Device.objects.bulk_create(devices)

        return devices

    @staticmethod
    def get_virtual_machines():
        cluster_type = ClusterType.objects.create(name="cluster-type-1")
        cluster = Cluster.objects.create(name="cluster-1", type=cluster_type)

        virtual_machines = (
            VirtualMachine(name="virtual-machine-1", cluster=cluster),
            VirtualMachine(name="virtual-machine-2", cluster=cluster),
            VirtualMachine(name="virtual-machine-3", cluster=cluster),
        )
        VirtualMachine.objects.bulk_create(virtual_machines)

        return virtual_machines

    @staticmethod
    def get_mac_addresses():
        mac_addresses = (
            MACAddress(mac_address="08:00:2b:00:00:01"),
            MACAddress(mac_address="08:00:2b:00:00:02"),
            MACAddress(mac_address="08:00:2b:00:00:03"),
        )

        MACAddress.objects.bulk_create(mac_addresses)

        return mac_addresses

    @staticmethod
    def get_client_classes(dhcp_server):
        client_classes = (
            ClientClass(dhcp_server=dhcp_server, name="client-class-1"),
            ClientClass(dhcp_server=dhcp_server, name="client-class-2"),
            ClientClass(dhcp_server=dhcp_server, name="client-class-3"),
        )

        ClientClass.objects.bulk_create(client_classes)

        return client_classes

    @staticmethod
    def get_dhcp_clusters():
        dhcp_clusters = (
            DHCPCluster(name="test-cluster-1"),
            DHCPCluster(name="test-cluster-2"),
            DHCPCluster(name="test-cluster-3"),
        )

        DHCPCluster.objects.bulk_create(dhcp_clusters)

        return dhcp_clusters

    @staticmethod
    def get_dhcp_servers():
        dhcp_servers = (
            DHCPServer(name="test-server-1"),
            DHCPServer(name="test-server-2"),
            DHCPServer(name="test-server-3"),
        )

        DHCPServer.objects.bulk_create(dhcp_servers)

        return dhcp_servers
