from django.test import TestCase
from django.core.exceptions import ValidationError

from netbox_dhcp.models import PDPool, Subnet
from netbox_dhcp.tests.custom import TestObjects


class PDPoolValidationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        cls.ipv4_prefixes = TestObjects.get_ipv4_prefixes()

        cls.ipv6_subnet = Subnet.objects.create(
            name="test-ipv6-subnet-1",
            dhcp_server=cls.dhcp_servers[0],
            prefix=cls.ipv6_prefixes[0],
        )

        cls.ipv4_subnet = Subnet.objects.create(
            name="test-ipv4-subnet-1",
            dhcp_server=cls.dhcp_servers[0],
            prefix=cls.ipv4_prefixes[0],
        )

    def test_create_pdpool(self):
        PDPool.objects.create(
            name="test-prefix-delegation-pool",
            subnet=self.ipv6_subnet,
            prefix=self.ipv6_prefixes[1],
            delegated_length=80,
            excluded_prefix=self.ipv6_prefixes[4],
        )

        self.assertTrue(
            PDPool.objects.filter(name="test-prefix-delegation-pool").exists()
        )

    def test_create_pdpool_ipv4_subnet_fail(self):
        with self.assertRaises(ValidationError):
            PDPool.objects.create(
                name="test-prefix-delegation-pool",
                subnet=self.ipv4_subnet,
                prefix=self.ipv6_prefixes[1],
                delegated_length=80,
                excluded_prefix=self.ipv6_prefixes[4],
            )

        self.assertFalse(
            PDPool.objects.filter(name="test-prefix-delegation-pool").exists()
        )

    def test_create_pdpool_ipv4_prefix_fail(self):
        with self.assertRaises(ValidationError):
            PDPool.objects.create(
                name="test-prefix-delegation-pool",
                subnet=self.ipv6_subnet,
                prefix=self.ipv4_prefixes[1],
                delegated_length=80,
                excluded_prefix=self.ipv6_prefixes[4],
            )

        self.assertFalse(
            PDPool.objects.filter(name="test-prefix-delegation-pool").exists()
        )

    def test_create_pdpool_ipv4_excluded_prefix_fail(self):
        with self.assertRaises(ValidationError):
            PDPool.objects.create(
                name="test-prefix-delegation-pool",
                subnet=self.ipv6_subnet,
                prefix=self.ipv6_prefixes[1],
                delegated_length=80,
                excluded_prefix=self.ipv4_prefixes[3],
            )

        self.assertFalse(
            PDPool.objects.filter(name="test-prefix-delegation-pool").exists()
        )

    def test_create_pdpool_excluded_prefix_no_subprefix_fail(self):
        with self.assertRaises(ValidationError):
            PDPool.objects.create(
                name="test-prefix-delegation-pool",
                subnet=self.ipv6_subnet,
                prefix=self.ipv6_prefixes[1],
                delegated_length=80,
                excluded_prefix=self.ipv6_prefixes[6],
            )

        self.assertFalse(
            PDPool.objects.filter(name="test-prefix-delegation-pool").exists()
        )

    def test_create_pdpool_short_delegation_length_fail(self):
        with self.assertRaises(ValidationError):
            PDPool.objects.create(
                name="test-prefix-delegation-pool",
                subnet=self.ipv6_subnet,
                prefix=self.ipv6_prefixes[1],
                delegated_length=16,
                excluded_prefix=self.ipv6_prefixes[6],
            )

        self.assertFalse(
            PDPool.objects.filter(name="test-prefix-delegation-pool").exists()
        )
