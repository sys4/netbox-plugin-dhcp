from netaddr import IPNetwork

from django.test import TestCase
from django.core.exceptions import ValidationError

from ipam.models import IPRange

from netbox_dhcp.models import Pool, Subnet
from netbox_dhcp.tests.custom import TestObjects


class PoolValidationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()

        cls.subnets = (
            Subnet(
                name="test-ipv4-subnet",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[1],  # 198.18.0.0/24
            ),
            Subnet(
                name="test-ipv6-subnet",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[1],  # 2001:db8:0:1::64
            ),
        )
        for subnet in cls.subnets:
            subnet.save()

    def test_create_pool_in_subnet(self):
        ipv4_range = IPRange.objects.create(
            start_address=IPNetwork("198.18.0.128/24"),
            end_address=IPNetwork("198.18.0.191/24"),
        )
        ipv6_range = IPRange.objects.create(
            start_address=IPNetwork("2001:db8:0:1::128/64"),
            end_address=IPNetwork("2001:db8:0:1::191/64"),
        )

        Pool.objects.create(
            name="test-ipv4-pool",
            subnet=self.subnets[0],
            ip_range=ipv4_range,
        )
        Pool.objects.create(
            name="test-ipv6-pool",
            subnet=self.subnets[1],
            ip_range=ipv6_range,
        )

        self.assertTrue(Pool.objects.filter(name="test-ipv4-pool").exists())
        self.assertTrue(Pool.objects.filter(name="test-ipv6-pool").exists())

    def test_create_pool_outside_subnet_fail(self):
        ipv4_range = IPRange.objects.create(
            start_address=IPNetwork("198.18.1.128/24"),
            end_address=IPNetwork("198.18.1.191/24"),
        )
        ipv6_range = IPRange.objects.create(
            start_address=IPNetwork("2001:db8:0:2::128/64"),
            end_address=IPNetwork("2001:db8:0:2::191/64"),
        )

        with self.assertRaises(ValidationError):
            Pool.objects.create(
                name="test-ipv4-pool",
                subnet=self.subnets[0],
                ip_range=ipv4_range,
            )
        with self.assertRaises(ValidationError):
            Pool.objects.create(
                name="test-ipv6-pool",
                subnet=self.subnets[1],
                ip_range=ipv6_range,
            )

        self.assertFalse(Pool.objects.filter(name="test-ipv4-pool").exists())
        self.assertFalse(Pool.objects.filter(name="test-ipv6-pool").exists())
