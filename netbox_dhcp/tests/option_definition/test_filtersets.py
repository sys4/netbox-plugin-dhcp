from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTests
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.models import OptionDefinition
from netbox_dhcp.filtersets import OptionDefinitionFilterSet
from netbox_dhcp.choices import OptionTypeChoices, OptionSpaceChoices
from netbox_dhcp.tests.custom import TestObjects


class OptionDefinitionFilterSetTestCase(
    TestCase,
    ChangeLoggedFilterSetTests,
):
    queryset = OptionDefinition.objects.all()
    filterset = OptionDefinitionFilterSet

    def _get_queryset(self):
        return self.model.objects.filter(standard=False)

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )

        cls.option_definitions = (
            OptionDefinition(
                name="test-option-definition-1",
                description="Test Option Definition 1",
                code=251,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_STRING,
                space=OptionSpaceChoices.DHCPV4,
                array=False,
                dhcp_server=cls.dhcp_servers[0],
            ),
            OptionDefinition(
                name="test-option-definition-2",
                description="Test Option Definition 2",
                code=252,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_IPV4_ADDRESS,
                space=OptionSpaceChoices.DHCPV4,
                encapsulate="xxx",
                array=True,
                dhcp_server=cls.dhcp_servers[0],
            ),
            OptionDefinition(
                name="test-option-definition-3",
                description="Test Option Definition 3",
                code=252,
                family=IPAddressFamilyChoices.FAMILY_6,
                type=OptionTypeChoices.TYPE_IPV6_ADDRESS,
                space=OptionSpaceChoices.DHCPV6,
                encapsulate="isc",
                array=True,
                dhcp_server=cls.dhcp_servers[1],
            ),
            OptionDefinition(
                name="test-option-definition-4",
                description="Test Option Definition 4",
                code=253,
                family=IPAddressFamilyChoices.FAMILY_6,
                type=OptionTypeChoices.TYPE_RECORD,
                record_types=[
                    OptionTypeChoices.TYPE_INT32,
                    OptionTypeChoices.TYPE_IPV6_ADDRESS,
                ],
                space=OptionSpaceChoices.DHCPV6,
                encapsulate="isc",
                client_class=cls.client_classes[0],
            ),
            OptionDefinition(
                name="test-option-definition-5",
                description="Test Option Definition 5",
                code=254,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_RECORD,
                record_types=[
                    OptionTypeChoices.TYPE_INT32,
                    OptionTypeChoices.TYPE_IPV4_ADDRESS,
                ],
                space=OptionSpaceChoices.DHCPV4,
                client_class=cls.client_classes[0],
            ),
        )
        OptionDefinition.objects.bulk_create(cls.option_definitions)

    def test_name(self):
        params = {
            "standard": False,
            "name__iregex": ["test-option-definition-1", "test-option-definition-2"],
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_description(self):
        params = {
            "standard": False,
            "description": ["Test Option Definition 1", "Test Option Definition 2"],
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_family(self):
        params = {"standard": False, "family": [IPAddressFamilyChoices.FAMILY_4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"standard": False, "family": [IPAddressFamilyChoices.FAMILY_6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_space(self):
        params = {"standard": False, "space": [OptionSpaceChoices.DHCPV4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"standard": False, "space": [OptionSpaceChoices.DHCPV6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_code(self):
        params = {"standard": False, "code": [252]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"standard": False, "code": [253, 254]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"standard": False, "code": [252, 253, 254]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 4)

    def test_type(self):
        params = {
            "standard": False,
            "type": [OptionTypeChoices.TYPE_RECORD, OptionTypeChoices.TYPE_STRING],
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {
            "standard": False,
            "type": [
                OptionTypeChoices.TYPE_IPV4_ADDRESS,
                OptionTypeChoices.TYPE_IPV6_ADDRESS,
            ],
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_record_types(self):
        params = {
            "standard": False,
            "record_types": [
                OptionTypeChoices.TYPE_INT16,
                OptionTypeChoices.TYPE_INT32,
            ],
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"standard": False, "type": [OptionTypeChoices.TYPE_IPV4_ADDRESS]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_encapsulate(self):
        params = {"standard": False, "encapsulate": ["isc"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_array(self):
        params = {"standard": False, "array": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"standard": False, "array": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_dhcp_server(self):
        params = {"dhcp_server_id": [self.dhcp_servers[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"dhcp_server": [self.dhcp_servers[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_client_class(self):
        params = {"client_class_id": [self.client_classes[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"client_class": [self.client_classes[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
