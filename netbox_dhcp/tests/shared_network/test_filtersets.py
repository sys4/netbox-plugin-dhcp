from django.test import TestCase

from ipam.choices import IPAddressFamilyChoices
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_dhcp.models import SharedNetwork, Subnet
from netbox_dhcp.filtersets import SharedNetworkFilterSet
from netbox_dhcp.tests.custom import (
    TestObjects,
    BOOTPFilterSetTests,
    ValidLifetimeFilterSetTests,
    OfferLifetimeFilterSetTests,
    PreferredLifetimeFilterSetTests,
    LeaseFilterSetTests,
    DDNSUpdateFilterSetTests,
)


class SharedNetworkFilterSetTestCase(
    BOOTPFilterSetTests,
    ValidLifetimeFilterSetTests,
    OfferLifetimeFilterSetTests,
    PreferredLifetimeFilterSetTests,
    LeaseFilterSetTests,
    DDNSUpdateFilterSetTests,
    TestCase,
    ChangeLoggedFilterSetTests,
):
    queryset = SharedNetwork.objects.all()
    filterset = SharedNetworkFilterSet

    # +
    # This is a dirty hack and does not work for all models.
    #
    # What really needs to be fixed is the get_m2m_filter_name() method in
    # netbox/utilities/testing/filtersets.py, which returns a filter name
    # based on the target model verbose name instead of the field name.
    #
    # Obviously this fails if there are multiple m2m relations to the same
    # class.
    # -
    filter_name_map = {
        "dhcp_server_interface": "server_interface",
    }

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )

        shared_networks = (
            SharedNetwork(
                name="test-shared-network-1",
                description="Test Shared Network 1",
                weight=90,
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[0],
                **DDNSUpdateFilterSetTests.DATA[0],
                **BOOTPFilterSetTests.DATA[0],
                **ValidLifetimeFilterSetTests.DATA[0],
                **OfferLifetimeFilterSetTests.DATA[0],
                **LeaseFilterSetTests.DATA[0],
            ),
            SharedNetwork(
                name="test-shared-network-2",
                description="Test Shared Network 2",
                weight=100,
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv4_prefixes[1],
                **BOOTPFilterSetTests.DATA[1],
                **OfferLifetimeFilterSetTests.DATA[1],
            ),
            SharedNetwork(
                name="test-shared-network-3",
                description="Test Shared Network 3",
                weight=110,
                dhcp_server=cls.dhcp_servers[2],
                prefix=cls.ipv4_prefixes[2],
                **BOOTPFilterSetTests.DATA[2],
                **DDNSUpdateFilterSetTests.DATA[1],
                **ValidLifetimeFilterSetTests.DATA[1],
                **OfferLifetimeFilterSetTests.DATA[2],
                **LeaseFilterSetTests.DATA[1],
            ),
            SharedNetwork(
                name="test-shared-network-4",
                description="Test Shared Network 4",
                weight=90,
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[0],
                **PreferredLifetimeFilterSetTests.DATA[0],
            ),
            SharedNetwork(
                name="test-shared-network-5",
                description="Test Shared Network 5",
                weight=100,
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv6_prefixes[1],
                **DDNSUpdateFilterSetTests.DATA[2],
                **ValidLifetimeFilterSetTests.DATA[2],
                **PreferredLifetimeFilterSetTests.DATA[1],
                **LeaseFilterSetTests.DATA[2],
            ),
            SharedNetwork(
                name="test-shared-network-6",
                description="Test Shared Network 6",
                weight=110,
                dhcp_server=cls.dhcp_servers[2],
                prefix=cls.ipv6_prefixes[2],
                **PreferredLifetimeFilterSetTests.DATA[2],
            ),
        )
        SharedNetwork.objects.bulk_create(shared_networks)

        cls.ipv4_subnets = (
            Subnet(
                name="test-ipv4-subnet-1",
                shared_network=shared_networks[0],
                prefix=cls.ipv4_prefixes[0],
            ),
            Subnet(
                name="test-ipv4-subnet-2",
                shared_network=shared_networks[1],
                prefix=cls.ipv4_prefixes[1],
            ),
            Subnet(
                name="test-ipv4-subnet-3",
                shared_network=shared_networks[2],
                prefix=cls.ipv4_prefixes[2],
            ),
        )
        for subnet in cls.ipv4_subnets:
            subnet.save()

        cls.ipv6_subnets = (
            Subnet(
                name="test-ipv6-subnet-1",
                shared_network=shared_networks[3],
                prefix=cls.ipv6_prefixes[0],
            ),
            Subnet(
                name="test-ipv6-subnet-2",
                shared_network=shared_networks[4],
                prefix=cls.ipv6_prefixes[1],
            ),
            Subnet(
                name="test-ipv6-subnet-3",
                shared_network=shared_networks[5],
                prefix=cls.ipv6_prefixes[2],
            ),
        )
        for subnet in cls.ipv6_subnets:
            subnet.save()

        for number in range(4):
            shared_networks[number].client_classes.add(cls.client_classes[number % 3])
            shared_networks[number].evaluate_additional_classes.add(
                cls.client_classes[(number + 2) % 3]
            )

    def test_name(self):
        params = {"name": ["test-shared-network-1", "test-shared-network-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["test-shared-network-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_description(self):
        params = {"description": ["Test Shared Network 1", "Test Shared Network 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"description": ["Test Shared Network 3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_prefix(self):
        params = {"prefix_id": [self.ipv6_prefixes[1].pk, self.ipv6_prefixes[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"prefix__iregex": r"2001:db8:0:[12]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"prefix_id": [self.ipv4_prefixes[0].pk, self.ipv4_prefixes[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"prefix__iregex": r"198\.18\.[01]\..*/24"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_child_subnet(self):
        params = {"child_subnet_id": [self.ipv6_subnets[0].pk, self.ipv6_subnets[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"child_subnet__iregex": r"ipv6-subnet-[23]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"child_subnet_id": [self.ipv4_subnets[0].pk, self.ipv4_subnets[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"child_subnet__iregex": r"ipv4-subnet-[23]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_client_classes(self):
        params = {
            "client_class_id": [
                self.client_classes[0].pk,
                self.client_classes[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
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
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_weight(self):
        params = {"weight": [100]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_family(self):
        params = {"family": [IPAddressFamilyChoices.FAMILY_4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"family": [IPAddressFamilyChoices.FAMILY_6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
