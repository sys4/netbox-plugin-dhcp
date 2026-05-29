from netbox_dhcp.models import HostReservation, Subnet
from netbox_dhcp.tests.custom import ModelViewTestCase, TestObjects
from utilities.testing import ViewTestCases


class HostReservationViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = HostReservation

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()
        mac_addresses = TestObjects.get_mac_addresses()
        ipv4_addresses = TestObjects.get_ipv4_addresses()
        ipv6_addresses = TestObjects.get_ipv6_addresses()
        ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])

        subnets = (
            Subnet(
                name="test-subnet-1",
                dhcp_server=dhcp_servers[0],
                prefix=ipv6_prefixes[0],
            ),
            Subnet(
                name="test-subnet-2",
                dhcp_server=dhcp_servers[1],
                prefix=ipv6_prefixes[1],
            ),
            Subnet(
                name="test-subnet-3",
                dhcp_server=dhcp_servers[2],
                prefix=ipv6_prefixes[2],
            ),
            Subnet(
                name="test-subnet-4",
                dhcp_server=dhcp_servers[0],
                prefix=ipv4_prefixes[0],
            ),
        )
        for subnet in subnets:
            subnet.save()

        host_reservations = (
            HostReservation(
                name="test-host-reservation-1",
                description="Test Host Reservation 1",
                dhcp_server=dhcp_servers[0],
                hw_address=mac_addresses[1],
                next_server="192.0.2.1",
                server_hostname="tftp.example.com",
                ipv4_address=ipv4_addresses[1],
            ),
            HostReservation(
                name="test-host-reservation-2",
                description="Test Host Reservation 2",
                dhcp_server=dhcp_servers[1],
                duid="00:02:00:00:3e:20:ff:00:00:00:00:01",
            ),
            HostReservation(
                name="test-host-reservation-3",
                subnet=subnets[0],
                description="Test Host Reservation 3",
                duid="00:02:00:00:3e:20:ff:00:00:00:00:02",
            ),
        )
        HostReservation.objects.bulk_create(host_reservations)

        host_reservations[0].client_classes.set([client_classes[0]])

        host_reservations[1].ipv6_addresses.set([ipv6_addresses[1], ipv6_addresses[2]])
        host_reservations[1].ipv6_prefixes.set([ipv6_prefixes[0], ipv6_prefixes[1]])
        host_reservations[1].client_classes.set([client_classes[2]])

        host_reservations[2].ipv6_addresses.set([ipv6_addresses[0]])
        host_reservations[2].ipv6_prefixes.set([ipv6_prefixes[0], ipv6_prefixes[1]])
        host_reservations[2].excluded_ipv6_prefixes.set([ipv6_prefixes[2]])
        host_reservations[2].client_classes.set([client_classes[2]])

        cls.form_data = {
            "name": "test-host-reservation-7",
            "description": "Test Host Reservation 7",
            "subnet": subnets[3].pk,
            "hw_address": mac_addresses[2].pk,
            "next_server": "19.0.2.1",
            "server_hostname": "tftp.example.com",
            "boot_file_name": "/tftpboot/file1.img",
            "ipv4_address": ipv4_addresses[0].pk,
            "client_classes": [client_classes[0].pk],
        }

        cls.bulk_edit_data = {
            "description": "Test Description Bulk Update",
            "subnet": subnets[1].pk,
            "circuit_id": "ge0/0/0:vlan42",
            "flex_id": "0x42424242",
            "next_server": "192.0.2.2",
            "server_hostname": "tftp2.example.com",
            "boot_file_name": "/tftpboot/file2.img",
            "ipv6_prefixes": [ipv6_prefixes[1].pk],
            "excluded_ipv6_prefixes": [ipv6_prefixes[2].pk],
            "client_classes": [client_classes[1].pk],
            "_nullify": "dhcp_server",
        }

        cls.csv_data = (
            "name,dhcp_server,subnet,description,hw_address",
            f"test-host-reservation-4,{dhcp_servers[2].name},,Test Host Reservation 4),{mac_addresses[0].mac_address}",
            f"test-host-reservation-5,{dhcp_servers[1].name},,Test Host Reservation 5),{mac_addresses[0].mac_address}",
            f"test-host-reservation-6,,{subnets[0].name},Test Host Reservation 6),{mac_addresses[0].mac_address}",
        )

        cls.csv_update_data = (
            "id,dhcp_server,subnet,description,hw_address",
            f"{host_reservations[0].pk},{dhcp_servers[0].name},,Test Host Reservation 1 (updated),{mac_addresses[0].mac_address}",
            f"{host_reservations[1].pk},{dhcp_servers[1].name},,Test Host Reservation 2 (updated),{mac_addresses[1].mac_address}",
            f"{host_reservations[2].pk},,{subnets[0].name},Test Host Reservation 3 (updated),{mac_addresses[2].mac_address}",
        )

    maxDiff = None
