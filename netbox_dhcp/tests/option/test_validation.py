from django.test import TestCase
from django.core.exceptions import ValidationError

from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import (
    SharedNetwork,
    Subnet,
    Pool,
    PDPool,
    OptionDefinition,
    Option,
    HostReservation,
    ClientClass,
)
from netbox_dhcp.tests.custom import TestObjects
from netbox_dhcp.choices import OptionTypeChoices


class OptionValidationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        cls.ipv4_ranges = TestObjects.get_ipv4_ranges()
        cls.ipv6_ranges = TestObjects.get_ipv6_ranges()

        cls.shared_networks = (
            SharedNetwork(
                name="test-ipv4-shared-network",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv4_prefixes[0],  # 198.18.0.0/24
            ),
            SharedNetwork(
                name="test-ipv6-subnet",
                dhcp_server=cls.dhcp_servers[0],
                prefix=cls.ipv6_prefixes[0],  # 2001:db8::/32
            ),
        )
        SharedNetwork.objects.bulk_create(cls.shared_networks)

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

        cls.pools = (
            Pool(
                name="test-ipv4-pool",
                subnet=cls.subnets[0],
                ip_range=cls.ipv4_ranges[0],
            ),
            Pool(
                name="test-ipv6-pool",
                subnet=cls.subnets[1],
                ip_range=cls.ipv6_ranges[0],
            ),
        )
        Pool.objects.bulk_create(cls.pools)

        cls.pd_pool = PDPool.objects.create(
            name="test-pdpool",
            subnet=cls.subnets[1],
            prefix=cls.ipv6_prefixes[1],
            delegated_length=96,
        )

        cls.option_definitions = (
            OptionDefinition.objects.filter(
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_EMPTY,
            ).first(),
            OptionDefinition.objects.filter(
                family=IPAddressFamilyChoices.FAMILY_6,
                type=OptionTypeChoices.TYPE_EMPTY,
            ).first(),
        )

    def test_option_shared_network(self):
        ipv4_shared_network = self.shared_networks[0]
        ipv6_shared_network = self.shared_networks[1]

        ipv4_option = Option.objects.create(
            definition=self.option_definitions[0],
            assigned_object=ipv4_shared_network,
        )
        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=ipv6_shared_network,
        )

        self.assertTrue(ipv4_option in ipv4_shared_network.options.all())
        self.assertTrue(ipv6_option in ipv6_shared_network.options.all())

    def test_option_shared_network_family_mismatch_fail(self):
        ipv4_shared_network = self.shared_networks[0]
        ipv6_shared_network = self.shared_networks[1]

        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[0],
                assigned_object=ipv6_shared_network,
            )
        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[1],
                assigned_object=ipv4_shared_network,
            )

        self.assertFalse(ipv4_shared_network.options.exists())
        self.assertFalse(ipv6_shared_network.options.exists())

    def test_option_subnet(self):
        ipv4_subnet = self.subnets[0]
        ipv6_subnet = self.subnets[1]

        ipv4_option = Option.objects.create(
            definition=self.option_definitions[0],
            assigned_object=ipv4_subnet,
        )
        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=ipv6_subnet,
        )

        self.assertTrue(ipv4_option in ipv4_subnet.options.all())
        self.assertTrue(ipv6_option in ipv6_subnet.options.all())

    def test_option_subnet_family_mismatch_fail(self):
        ipv4_subnet = self.subnets[0]
        ipv6_subnet = self.subnets[1]

        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[0],
                assigned_object=ipv6_subnet,
            )
        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[1],
                assigned_object=ipv4_subnet,
            )

        self.assertFalse(ipv4_subnet.options.exists())
        self.assertFalse(ipv6_subnet.options.exists())

    def test_option_pool(self):
        ipv4_pool = self.pools[0]
        ipv6_pool = self.pools[1]

        ipv4_option = Option.objects.create(
            definition=self.option_definitions[0],
            assigned_object=ipv4_pool,
        )
        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=ipv6_pool,
        )

        self.assertTrue(ipv4_option in ipv4_pool.options.all())
        self.assertTrue(ipv6_option in ipv6_pool.options.all())

    def test_option_pool_family_mismatch_fail(self):
        ipv4_pool = self.pools[0]
        ipv6_pool = self.pools[1]

        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[0],
                assigned_object=ipv6_pool,
            )
        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[1],
                assigned_object=ipv4_pool,
            )

        self.assertFalse(ipv4_pool.options.exists())
        self.assertFalse(ipv6_pool.options.exists())

    def test_option_prefix_delegation_pool(self):
        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=self.pd_pool,
        )

        self.assertTrue(ipv6_option in self.pd_pool.options.all())

    def test_option_prefix_delegation_pool_ipv4_option_fail(self):
        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[0],
                assigned_object=self.pd_pool,
            )

        self.assertFalse(self.pd_pool.options.exists())

    def test_option_dhcp_server(self):
        dhcp_server = self.dhcp_servers[0]

        ipv4_option = Option.objects.create(
            definition=self.option_definitions[0],
            assigned_object=dhcp_server,
        )
        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=dhcp_server,
        )

        self.assertTrue(ipv4_option in dhcp_server.options.all())
        self.assertTrue(ipv6_option in dhcp_server.options.all())

    def test_option_host_reservation(self):
        host_reservation = HostReservation.objects.create(
            name="test-host-reservation",
            dhcp_server=self.dhcp_servers[0],
        )

        ipv4_option = Option.objects.create(
            definition=self.option_definitions[0],
            assigned_object=host_reservation,
        )
        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=host_reservation,
        )

        self.assertTrue(ipv4_option in host_reservation.options.all())
        self.assertTrue(ipv6_option in host_reservation.options.all())

    def test_option_ipv4_subnet_host_reservation(self):
        host_reservation = HostReservation.objects.create(
            name="test-host-reservation",
            subnet=self.subnets[0],
        )

        ipv4_option = Option.objects.create(
            definition=self.option_definitions[0],
            assigned_object=host_reservation,
        )

        self.assertTrue(ipv4_option in host_reservation.options.all())

    def test_option_ipv4_subnet_host_reservation_family_mismatch_fail(self):
        host_reservation = HostReservation.objects.create(
            name="test-host-reservation",
            subnet=self.subnets[0],
        )

        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[1],
                assigned_object=host_reservation,
            )

        self.assertFalse(host_reservation.options.exists())

    def test_option_ipv6_subnet_host_reservation(self):
        host_reservation = HostReservation.objects.create(
            name="test-host-reservation",
            subnet=self.subnets[1],
        )

        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=host_reservation,
        )

        self.assertTrue(ipv6_option in host_reservation.options.all())

    def test_option_ipv6_subnet_host_reservation_family_mismatch_fail(self):
        host_reservation = HostReservation.objects.create(
            name="test-host-reservation",
            subnet=self.subnets[1],
        )

        with self.assertRaises(ValidationError):
            Option.objects.create(
                definition=self.option_definitions[0],
                assigned_object=host_reservation,
            )

        self.assertFalse(host_reservation.options.exists())

    def test_option_client_class(self):
        client_class = ClientClass.objects.create(
            name="test-client-class",
            dhcp_server=self.dhcp_servers[0],
        )

        ipv4_option = Option.objects.create(
            definition=self.option_definitions[0],
            assigned_object=client_class,
        )
        ipv6_option = Option.objects.create(
            definition=self.option_definitions[1],
            assigned_object=client_class,
        )

        self.assertTrue(ipv4_option in client_class.options.all())
        self.assertTrue(ipv6_option in client_class.options.all())
