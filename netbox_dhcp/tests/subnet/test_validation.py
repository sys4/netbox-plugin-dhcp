from django.test import TestCase
from django.core.exceptions import ValidationError

from netbox_dhcp.models import Subnet, SharedNetwork
from netbox_dhcp.tests.custom import TestObjects


class SharedNetworkValidationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()

        cls.shared_networks = (
            SharedNetwork(
                name="test-ipv4-shared-network-1",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[0],  # 198.18.0.0/16
            ),
            SharedNetwork(
                name="test-ipv4-shared-network-2",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[1],  # 198.18.1.0/24
            ),
            SharedNetwork(
                name="test-ipv6-shared-network-1",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[0],  # 2001:db8::/32
            ),
            SharedNetwork(
                name="test-ipv6-shared-network-2",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[1],  # 2001:db8::0:1::/32
            ),
        )
        SharedNetwork.objects.bulk_create(cls.shared_networks)

    def test_create_subnet_in_shared_network(self):
        Subnet.objects.create(
            name="test-ipv4-subnet",
            shared_network=self.shared_networks[0],
            prefix=self.ipv4_prefixes[1],
        )
        Subnet.objects.create(
            name="test-ipv6-subnet",
            shared_network=self.shared_networks[2],
            prefix=self.ipv6_prefixes[1],
        )

        self.assertTrue(Subnet.objects.filter(name="test-ipv4-subnet").exists())
        self.assertTrue(Subnet.objects.filter(name="test-ipv6-subnet").exists())

    def test_create_subnet_outside_shared_network_fail(self):
        with self.assertRaises(ValidationError):
            Subnet.objects.create(
                name="test-ipv4-subnet",
                shared_network=self.shared_networks[1],
                prefix=self.ipv4_prefixes[2],
            )
        with self.assertRaises(ValidationError):
            Subnet.objects.create(
                name="test-ipv6-subnet",
                shared_network=self.shared_networks[3],
                prefix=self.ipv6_prefixes[2],
            )

        self.assertFalse(Subnet.objects.filter(name="test-ipv4-subnet").exists())
        self.assertFalse(Subnet.objects.filter(name="test-ipv6-subnet").exists())
