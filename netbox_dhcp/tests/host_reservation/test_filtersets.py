from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTests

from netbox_dhcp.models import HostReservation, Subnet
from netbox_dhcp.filtersets import HostReservationFilterSet
from netbox_dhcp.tests.custom import TestObjects, BOOTPFilterSetTests


class HostReservationFilterSetTestCase(
    BOOTPFilterSetTests,
    TestCase,
    ChangeLoggedFilterSetTests,
):
    queryset = HostReservation.objects.all()
    filterset = HostReservationFilterSet

    ignore_fields = (
        "ipv6_addresses",
        "ipv6_prefixes",
        "excluded_ipv6_prefixes",
    )

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.mac_addresses = TestObjects.get_mac_addresses()
        cls.ipv4_addresses = TestObjects.get_ipv4_addresses()
        cls.ipv6_addresses = TestObjects.get_ipv6_addresses()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )

        cls.subnets = (
            Subnet(
                name="test-subnet-1",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[0],  # 2001:db8:0::/32
            ),
            Subnet(
                name="test-subnet-2",
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv6_prefixes[1],  # 2001:db8:0:1:/64
            ),
            Subnet(
                name="test-subnet-3",
                dhcp_server=cls.dhcp_servers[2],
                prefix=cls.ipv6_prefixes[2],  # 2001:db8:0:2:/64
            ),
        )
        for subnet in cls.subnets:
            subnet.save()

        cls.host_reservations = (
            HostReservation(
                name="test-host-reservation-1",
                description="Test Host Reservation 1",
                dhcp_server=cls.dhcp_servers[0],
                circuit_id="ge0/0/0:vlan42",
                client_id="sample.client.1",
                duid="00:02:00:00:3e:20:ff:00:00:00:00:01",
                hw_address=cls.mac_addresses[0],
                flex_id="0x42424242",
                hostname="host1.zone1.example.com",
                ipv4_address=cls.ipv4_addresses[0],
                **BOOTPFilterSetTests.DATA[0],
            ),
            HostReservation(
                name="test-host-reservation-2",
                description="Test Host Reservation 2",
                dhcp_server=cls.dhcp_servers[1],
                circuit_id="ge0/0/1:vlan42",
                client_id="sample.client.2",
                duid="00:02:00:00:3e:20:ff:00:00:00:00:02",
                hw_address=cls.mac_addresses[1],
                flex_id="0x2323232323",
                hostname="host2.zone1.example.com",
                ipv4_address=cls.ipv4_addresses[1],
                **BOOTPFilterSetTests.DATA[1],
            ),
            HostReservation(
                name="test-host-reservation-3",
                description="Test Host Reservation 3",
                dhcp_server=cls.dhcp_servers[2],
                circuit_id="ge0/0/2:vlan43",
                client_id="sample.client.3",
                duid="00:02:00:00:3e:20:ff:00:00:00:00:03",
                hw_address=cls.mac_addresses[2],
                flex_id="0x42424242",
                hostname="host3.zone1.example.com",
                ipv4_address=cls.ipv4_addresses[2],
                **BOOTPFilterSetTests.DATA[2],
            ),
            HostReservation(
                name="test-host-reservation-4",
                description="Test Host Reservation 4",
                subnet=cls.subnets[0],
            ),
            HostReservation(
                name="test-host-reservation-5",
                description="Test Host Reservation 5",
                subnet=cls.subnets[1],
            ),
            HostReservation(
                name="test-host-reservation-6",
                description="Test Host Reservation 6",
                subnet=cls.subnets[2],
            ),
        )
        HostReservation.objects.bulk_create(cls.host_reservations)

        cls.host_reservations[0].ipv6_addresses.set(cls.ipv6_addresses[0:2])
        cls.host_reservations[1].ipv6_addresses.set(cls.ipv6_addresses[1:3])
        cls.host_reservations[2].ipv6_addresses.set(
            [cls.ipv6_addresses[0], cls.ipv6_addresses[2]]
        )

        cls.host_reservations[0].ipv6_prefixes.set(cls.ipv6_prefixes[0:2])
        cls.host_reservations[1].ipv6_prefixes.set(cls.ipv6_prefixes[1:3])
        cls.host_reservations[2].ipv6_prefixes.set(
            [cls.ipv6_prefixes[0], cls.ipv6_prefixes[2]]
        )

        cls.host_reservations[0].excluded_ipv6_prefixes.set(cls.ipv6_prefixes[0:2])
        cls.host_reservations[1].excluded_ipv6_prefixes.set(cls.ipv6_prefixes[1:3])
        cls.host_reservations[2].excluded_ipv6_prefixes.set(
            [cls.ipv6_prefixes[0], cls.ipv6_prefixes[2]]
        )

        cls.host_reservations[0].client_classes.set(cls.client_classes[0:2])
        cls.host_reservations[1].client_classes.set(cls.client_classes[1:3])
        cls.host_reservations[2].client_classes.set(
            [cls.client_classes[0], cls.client_classes[2]]
        )

    def test_name(self):
        params = {"name": ["test-host-reservation-1", "test-host-reservation-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["test-host-reservation-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_description(self):
        params = {"description": ["Test Host Reservation 1", "Test Host Reservation 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"description": ["Test Host Reservation 3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_circuit_id(self):
        params = {"circuit_id": ["ge0/0/0:vlan42", "ge0/0/1:vlan42"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"circuit_id": ["ge0/0/1:vlan42"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_client_id(self):
        params = {"client_id": ["sample.client.2", "sample.client.3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"client_id": ["sample.client.1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_duid(self):
        params = {
            "duid": [
                "00:02:00:00:3e:20:ff:00:00:00:00:02",
                "00:02:00:00:3e:20:ff:00:00:00:00:03",
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"duid": ["00:02:00:00:3e:20:ff:00:00:00:00:01"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_hw_address(self):
        params = {
            "hw_address__iregex": rf"({self.mac_addresses[0].mac_address}|{self.mac_addresses[1].mac_address})"
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"hw_address_id": [self.mac_addresses[0].pk, self.mac_addresses[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ipv4_address(self):
        params = {
            "ipv4_address__iregex": rf"({self.ipv4_addresses[0].address}|{self.ipv4_addresses[1].address})"
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "ipv4_address_id": [self.ipv4_addresses[0].pk, self.ipv4_addresses[1].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ipv6_address(self):
        params = {"ipv6_address": self.ipv6_addresses[0].address}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"ipv6_address_id": [self.ipv6_addresses[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ipv6_prefix(self):
        params = {"ipv6_prefix__iregex": r"db8:0:[12]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {
            "ipv6_prefix_id": [self.ipv6_prefixes[0].pk, self.ipv6_prefixes[1].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_excluded_ipv6_prefix(self):
        params = {"excluded_ipv6_prefix": self.ipv6_prefixes[0].prefix}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"excluded_ipv6_prefix_id": [self.ipv6_prefixes[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_dhcp_server(self):
        params = {"dhcp_server__iregex": r"server-[12]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"dhcp_server_id": [self.dhcp_servers[0].pk, self.dhcp_servers[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_subnet(self):
        params = {"subnet__iregex": r"subnet-[12]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"subnet_id": [self.subnets[0].pk, self.subnets[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
