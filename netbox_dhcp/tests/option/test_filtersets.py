from django.test import TestCase

from ipam.choices import IPAddressFamilyChoices
from netbox_dhcp.choices import OptionSendChoices, OptionSpaceChoices
from netbox_dhcp.filtersets import OptionFilterSet
from netbox_dhcp.models import Option, OptionDefinition
from netbox_dhcp.tests.custom import TestObjects
from utilities.testing import ChangeLoggedFilterSetTests


class OptionFilterSetTestCase(
    TestCase,
    ChangeLoggedFilterSetTests,
):
    queryset = Option.objects.all()
    filterset = OptionFilterSet

    # +
    # Filtering by assigned object may turn out useful over time, but
    # currently I don't see the point and it's really complex because of the
    # GenericForeignKey relation.
    # -
    ignore_fields = (
        "assigned_object_id",
        "assigned_object_type",
    )

    @classmethod
    def setUpTestData(cls):
        cls.ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        cls.ipv6_prefixes = TestObjects.get_ipv6_prefixes()

        cls.option_definitions = (
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV4,
                name="routers",
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV4,
                name="domain-name-servers",
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV4,
                name="interface-mtu",
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV4,
                name="ip-forwarding",
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV6,
                name="dns-servers",
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV6,
                name="domain-search",
            ),
        )

        cls.options = (
            Option(
                definition=cls.option_definitions[0],
                description="Test Option 1",
                data="192.0.2.1,192.0.2.2",
                csv_format=True,
                send_option=OptionSendChoices.ALWAYS_SEND,
                assigned_object=cls.ipv4_prefixes[0],
            ),
            Option(
                definition=cls.option_definitions[0],
                description="Test Option 2",
                data="192.0.2.3,192.0.2.4",
                csv_format=True,
                send_option=OptionSendChoices.ALWAYS_SEND,
                assigned_object=cls.ipv4_prefixes[0],
            ),
            Option(
                definition=cls.option_definitions[1],
                description="Test Option 3",
                data="192.0.2.5,192.0.2.6",
                csv_format=True,
                assigned_object=cls.ipv4_prefixes[1],
            ),
            Option(
                definition=cls.option_definitions[2],
                description="Test Option 4",
                data="1380",
                send_option=OptionSendChoices.NEVER_SEND,
                assigned_object=cls.ipv4_prefixes[1],
                weight=50,
            ),
            Option(
                definition=cls.option_definitions[3],
                description="Test Option 5",
                data="true",
                csv_format=False,
                assigned_object=cls.ipv4_prefixes[2],
                weight=50,
            ),
            Option(
                definition=cls.option_definitions[4],
                description="Test Option 6",
                data="2001:db8:1::53,2001:db8:2::53",
                csv_format=True,
                send_option=OptionSendChoices.NEVER_SEND,
                assigned_object=cls.ipv6_prefixes[0],
                weight=200,
            ),
            Option(
                definition=cls.option_definitions[5],
                description="Test Option 7",
                data="example.com",
                csv_format=False,
                assigned_object=cls.ipv6_prefixes[1],
                weight=200,
            ),
        )
        Option.objects.bulk_create(cls.options)

    def test_description(self):
        params = {"description": ["Test Option 1", "Test Option 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_definition(self):
        params = {"definition_id": self.option_definitions[0:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {
            "definition": [
                self.option_definitions[0].name,
                self.option_definitions[1].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_name(self):
        params = {"name": ["routers"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["routers", "domain-name-servers"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_code(self):
        params = {"code": [3]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"code": [3, 6, 19, 23]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)

    def test_family(self):
        params = {"family": [IPAddressFamilyChoices.FAMILY_4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)
        params = {"family": [IPAddressFamilyChoices.FAMILY_6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_space(self):
        params = {"space": [OptionSpaceChoices.DHCPV4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)
        params = {"space": [OptionSpaceChoices.DHCPV6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_data(self):
        params = {"data__iregex": r"192\.0\.2\.[23]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"data": "1380"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_csv_format(self):
        params = {"csv_format": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 4)
        params = {"csv_format": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_send_option(self):
        params = {"send_option": OptionSendChoices.ALWAYS_SEND}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"send_option": OptionSendChoices.NEVER_SEND}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_weight(self):
        params = {"weight": [100]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"weight": [200]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
