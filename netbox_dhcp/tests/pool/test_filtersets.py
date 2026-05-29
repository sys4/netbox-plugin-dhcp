from django.test import TestCase

from ipam.choices import IPAddressFamilyChoices
from netbox_dhcp.filtersets import PoolFilterSet
from netbox_dhcp.models import Pool, Subnet
from netbox_dhcp.tests.custom import (
    DDNSUpdateFilterSetTests,
    OptionFilterSetTests,
    TestObjects,
)
from utilities.testing import ChangeLoggedFilterSetTests


class PoolFilterSetTestCase(
    DDNSUpdateFilterSetTests,
    TestCase,
    ChangeLoggedFilterSetTests,
    OptionFilterSetTests,
):
    queryset = Pool.objects.all()
    filterset = PoolFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )
        cls.ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        cls.ipv4_ranges = TestObjects.get_ipv4_ranges()
        cls.ipv6_ranges = TestObjects.get_ipv6_ranges()

        cls.ipv4_subnets = (
            Subnet(
                name="test-ipv4-subnet-1",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[0],
            ),
            Subnet(
                name="test-ipv4-subnet-2",
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv4_prefixes[1],
            ),
            Subnet(
                name="test-ipv4-subnet-3",
                dhcp_server=cls.dhcp_servers[2],
                prefix=cls.ipv4_prefixes[2],
            ),
        )
        for subnet in cls.ipv4_subnets:
            subnet.save()

        cls.ipv6_subnets = (
            Subnet(
                name="test-ipv6-subnet-1",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[0],
            ),
            Subnet(
                name="test-ipv6-subnet-2",
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv6_prefixes[1],
            ),
            Subnet(
                name="test-ipv6-subnet-3",
                dhcp_server=cls.dhcp_servers[2],
                prefix=cls.ipv6_prefixes[2],
            ),
        )
        for subnet in cls.ipv6_subnets:
            subnet.save()

        pools = (
            Pool(
                name="test-pool-1",
                description="Test Pool 1",
                weight=90,
                subnet=cls.ipv4_subnets[0],
                ip_range=cls.ipv4_ranges[0],
                pool_id=23,
                **DDNSUpdateFilterSetTests.DATA[0],
            ),
            Pool(
                name="test-pool-2",
                description="Test Pool 2",
                weight=100,
                subnet=cls.ipv4_subnets[1],
                ip_range=cls.ipv4_ranges[1],
                pool_id=42,
                **DDNSUpdateFilterSetTests.DATA[1],
            ),
            Pool(
                name="test-pool-3",
                description="Test Pool 3",
                weight=90,
                subnet=cls.ipv6_subnets[0],
                ip_range=cls.ipv6_ranges[0],
                pool_id=1337,
                **DDNSUpdateFilterSetTests.DATA[2],
            ),
            Pool(
                name="test-pool-4",
                description="Test Pool 4",
                weight=100,
                subnet=cls.ipv6_subnets[1],
                ip_range=cls.ipv6_ranges[1],
                pool_id=4711,
            ),
        )
        Pool.objects.bulk_create(pools)

        cls.add_test_options(pools)

        for number in range(4):
            pools[number].client_classes.add(cls.client_classes[(number + 1) % 3])
            pools[number].evaluate_additional_classes.add(
                cls.client_classes[(number + 2) % 3]
            )

    def test_name(self):
        params = {"name": ["test-pool-1", "test-pool-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["test-pool-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_description(self):
        params = {"description": ["Test Pool 1", "Test Pool 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"description": ["Test Pool 3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_pool_id(self):
        params = {"pool_id": [42]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ip_range(self):
        params = {"ip_range_id": [self.ipv6_ranges[0].pk, self.ipv4_ranges[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_start_address(self):
        params = {
            "start_address": [
                self.ipv6_ranges[0].start_address.ip,
                self.ipv4_ranges[0].start_address.ip,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_end_address(self):
        params = {
            "end_address": [
                self.ipv6_ranges[0].end_address,
                self.ipv4_ranges[0].end_address,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_contains_address(self):
        params = {
            "contains_address": [
                self.ipv6_ranges[0].end_address,
                self.ipv4_ranges[0].end_address,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "contains_address": [
                self.ipv6_ranges[0].start_address,
                self.ipv4_ranges[0].start_address,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "contains_address": [
                "198.18.2.5",
                "198.18.2.19/24",
                "2001:db8:0:1::beef/64",
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_subnet(self):
        params = {"subnet_id": [self.ipv6_subnets[0].pk, self.ipv6_subnets[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"subnet": [self.ipv6_subnets[0].name, self.ipv6_subnets[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_client_classes(self):
        params = {
            "client_class_id": [
                self.client_classes[0].pk,
                self.client_classes[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {
            "client_class": [
                self.client_classes[0].name,
                self.client_classes[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_evaluate_additional_classes(self):
        params = {
            "evaluate_additional_class_id": [
                self.client_classes[0].pk,
                self.client_classes[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "evaluate_additional_class": [
                self.client_classes[0].name,
                self.client_classes[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_weight(self):
        params = {"weight": [100]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"weight": [80, 90]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_family(self):
        params = {"family": [IPAddressFamilyChoices.FAMILY_4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"family": [IPAddressFamilyChoices.FAMILY_6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
