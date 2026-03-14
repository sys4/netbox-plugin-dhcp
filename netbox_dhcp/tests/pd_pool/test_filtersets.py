from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTests

from netbox_dhcp.models import PDPool, Subnet
from netbox_dhcp.filtersets import PDPoolFilterSet
from netbox_dhcp.tests.custom import TestObjects


class PDPoolFilterSetTestCase(
    TestCase,
    ChangeLoggedFilterSetTests,
):
    queryset = PDPool.objects.all()
    filterset = PDPoolFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )

        cls.ipv6_subnets = (
            Subnet(
                name="test-subnet-1",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[0],
            ),
            Subnet(
                name="test-subnet-2",
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv6_prefixes[1],
            ),
            Subnet(
                name="test-subnet-3",
                dhcp_server=cls.dhcp_servers[2],
                prefix=cls.ipv6_prefixes[2],
            ),
        )
        for subnet in cls.ipv6_subnets:
            subnet.save()

        cls.pd_pools = (
            PDPool(
                name="test-pd-pool-1",
                description="Test Prefix Delegation Pool 1",
                weight=90,
                subnet=cls.ipv6_subnets[0],
                prefix=cls.ipv6_prefixes[0],
                delegated_length=64,
                pool_id=42,
                excluded_prefix=cls.ipv6_prefixes[2],
            ),
            PDPool(
                name="test-pd-pool-2",
                description="Test Prefix Delegation Pool 2",
                weight=100,
                subnet=cls.ipv6_subnets[0],
                prefix=cls.ipv6_prefixes[1],
                delegated_length=64,
                pool_id=23,
                excluded_prefix=cls.ipv6_prefixes[4],
            ),
            PDPool(
                name="test-pd-pool-3",
                description="Test Prefix Delegation Pool 3",
                weight=110,
                subnet=cls.ipv6_subnets[2],
                prefix=cls.ipv6_prefixes[2],
                delegated_length=56,
                pool_id=1337,
                excluded_prefix=cls.ipv6_prefixes[6],
            ),
        )
        PDPool.objects.bulk_create(cls.pd_pools)

        for number in range(3):
            cls.pd_pools[number].client_classes.add(
                cls.client_classes[(number + 1) % 3]
            )
            cls.pd_pools[number].evaluate_additional_classes.add(
                cls.client_classes[(number + 2) % 3]
            )

    def test_name(self):
        params = {"name": ["test-pd-pool-1", "test-pd-pool-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["test-pd-pool-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_description(self):
        params = {
            "description": [
                "Test Prefix Delegation Pool 1",
                "Test Prefix Delegation Pool 2",
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"description": ["Test Prefix Delegation Pool 3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_pool_id(self):
        params = {"pool_id": [42]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"pool_id": [1337]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_prefix(self):
        params = {"prefix_id": [self.ipv6_prefixes[0].pk, self.ipv6_prefixes[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"prefix__iregex": r"2001:db8:0:[12]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_delegated_length(self):
        params = {"delegated_length": [64]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"delegated_length": [56]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_excluded_prefix(self):
        params = {
            "excluded_prefix_id": [self.ipv6_prefixes[4].pk, self.ipv6_prefixes[6].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"excluded_prefix__iregex": r"2001:db8:0:[12]:0:1"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_subnet(self):
        params = {"subnet_id": [self.ipv6_subnets[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"subnet__iregex": r"subnet-[23]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_client_classes(self):
        params = {
            "client_class_id": [
                self.client_classes[0].pk,
                self.client_classes[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"client_class__iregex": r"client-class-[23]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_evaluate_additional_classes(self):
        params = {
            "evaluate_additional_class_id": [
                self.client_classes[0].pk,
                self.client_classes[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"evaluate_additional_class__iregex": r"client-class-[23]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_weight(self):
        params = {"weight": [100]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"weight": [90]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
