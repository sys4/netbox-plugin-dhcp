from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTests
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import Subnet, SharedNetwork, HostReservation
from netbox_dhcp.filtersets import SubnetFilterSet
from netbox_dhcp.tests.custom import (
    TestObjects,
    BOOTPFilterSetTests,
    ValidLifetimeFilterSetTests,
    OfferLifetimeFilterSetTests,
    PreferredLifetimeFilterSetTests,
    LeaseFilterSetTests,
    DDNSUpdateFilterSetTests,
)


class SubnetFilterSetTestCase(
    BOOTPFilterSetTests,
    ValidLifetimeFilterSetTests,
    OfferLifetimeFilterSetTests,
    PreferredLifetimeFilterSetTests,
    LeaseFilterSetTests,
    DDNSUpdateFilterSetTests,
    TestCase,
    ChangeLoggedFilterSetTests,
):
    queryset = Subnet.objects.all()
    filterset = SubnetFilterSet

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
        "pool": "child_pool",
        "prefix_delegation_pool": "child_pd_pool",
        "host_reservation": "child_host_reservation",
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

        cls.shared_networks = (
            SharedNetwork(
                name="test-ipv4-shared-network-1",
                description="Test Shared Network 1",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[0],
            ),
            SharedNetwork(
                name="test-ipv4-shared-network-2",
                description="Test Shared Network 2",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[1],
            ),
            SharedNetwork(
                name="test-ipv6-shared-network-1",
                description="Test Shared Network 3",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[2],
            ),
            SharedNetwork(
                name="test-ipv6-shared-network-2",
                description="Test Shared Network 4",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[3],
            ),
        )
        SharedNetwork.objects.bulk_create(cls.shared_networks)

        cls.ipv4_subnets = (
            Subnet(
                name="test-subnet-1",
                description="Test Subnet 1",
                weight=90,
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[0],
                **DDNSUpdateFilterSetTests.DATA[0],
                **BOOTPFilterSetTests.DATA[0],
                **ValidLifetimeFilterSetTests.DATA[0],
                **OfferLifetimeFilterSetTests.DATA[0],
                **LeaseFilterSetTests.DATA[0],
            ),
            Subnet(
                name="test-subnet-2",
                description="Test Subnet 2",
                weight=100,
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv4_prefixes[1],
                **BOOTPFilterSetTests.DATA[1],
                **OfferLifetimeFilterSetTests.DATA[1],
            ),
            Subnet(
                name="test-subnet-3",
                description="Test Subnet 3",
                weight=110,
                shared_network=cls.shared_networks[0],
                prefix=cls.ipv4_prefixes[2],
                **BOOTPFilterSetTests.DATA[2],
                **DDNSUpdateFilterSetTests.DATA[1],
                **ValidLifetimeFilterSetTests.DATA[1],
                **OfferLifetimeFilterSetTests.DATA[2],
                **LeaseFilterSetTests.DATA[1],
            ),
        )
        for subnet in cls.ipv4_subnets:
            subnet.save()

        cls.ipv6_subnets = (
            Subnet(
                name="test-subnet-4",
                description="Test Subnet 4",
                weight=90,
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[0],
                **PreferredLifetimeFilterSetTests.DATA[0],
            ),
            Subnet(
                name="test-subnet-5",
                description="Test Subnet 5",
                weight=100,
                dhcp_server=cls.dhcp_servers[1],
                prefix=cls.ipv6_prefixes[1],
                **DDNSUpdateFilterSetTests.DATA[2],
                **ValidLifetimeFilterSetTests.DATA[2],
                **PreferredLifetimeFilterSetTests.DATA[1],
                **LeaseFilterSetTests.DATA[2],
            ),
            Subnet(
                name="test-subnet-6",
                description="Test Subnet 6",
                weight=110,
                shared_network=cls.shared_networks[2],
                prefix=cls.ipv6_prefixes[2],
                **PreferredLifetimeFilterSetTests.DATA[2],
            ),
        )
        for subnet in cls.ipv6_subnets:
            subnet.save()

        cls.host_reservations = (
            HostReservation(
                name="test-host-reservation-1",
                subnet=cls.ipv4_subnets[0],
            ),
            HostReservation(
                name="test-host-reservation-2",
                subnet=cls.ipv4_subnets[1],
            ),
            HostReservation(
                name="test-host-reservation-3",
                subnet=cls.ipv4_subnets[2],
            ),
        )
        HostReservation.objects.bulk_create(cls.host_reservations)

        for number in range(3):
            cls.ipv4_subnets[number].client_classes.add(cls.client_classes[number])
            cls.ipv4_subnets[number].evaluate_additional_classes.add(
                cls.client_classes[2 - number]
            )

    def test_name(self):
        params = {"name": ["test-subnet-1", "test-subnet-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["test-subnet-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_description(self):
        params = {"description": ["Test Subnet 1", "Test Subnet 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"description": ["Test Subnet 3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_prefix(self):
        params = {"prefix_id": [self.ipv6_prefixes[0].pk, self.ipv6_prefixes[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"prefix__iregex": r"2001:db8:0"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"prefix_id": [self.ipv4_prefixes[0].pk, self.ipv4_prefixes[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"prefix__iregex": r"198\.18\.0"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_child_host_reservations(self):
        params = {
            "child_host_reservation_id": [
                self.host_reservations[0].pk,
                self.host_reservations[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"child_host_reservation__iregex": r"host-reservation-[23]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_shared_network(self):
        params = {
            "shared_network_id": [
                self.shared_networks[0].pk,
                self.shared_networks[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"shared_network__iregex": r"ipv[46]-shared-network-[12]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_dhcp_server(self):
        params = {
            "dhcp_server_id": [
                self.dhcp_servers[0].pk,
                self.dhcp_servers[1].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 4)
        params = {"dhcp_server__iregex": r"test-server-[12]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 4)

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
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_family(self):
        params = {"family": [IPAddressFamilyChoices.FAMILY_4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"family": [IPAddressFamilyChoices.FAMILY_6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
