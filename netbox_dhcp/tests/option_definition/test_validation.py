from django.test import TestCase
from django.core.exceptions import ValidationError

from netbox_dhcp.models import OptionDefinition
from netbox_dhcp.tests.custom import TestObjects
from netbox_dhcp.choices import OptionSpaceChoices, OptionTypeChoices


class OptionDefinitionValidationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )

    def test_standard_and_global_definition_fail(self):
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=True,
                dhcp_server=self.dhcp_servers[0],
                space=OptionSpaceChoices.DHCPV4,
                name="name1",
                code=250,
                type=OptionTypeChoices.TYPE_EMPTY,
            )

    def test_standard_and_client_class_definition_fail(self):
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=True,
                client_class=self.client_classes[0],
                space=OptionSpaceChoices.DHCPV4,
                name="name1",
                code=250,
                type=OptionTypeChoices.TYPE_EMPTY,
            )

    def test_global_and_client_class_definition_fail(self):
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=False,
                dhcp_server=self.dhcp_servers[0],
                client_class=self.client_classes[0],
                space=OptionSpaceChoices.DHCPV4,
                name="name1",
                code=250,
                type=OptionTypeChoices.TYPE_EMPTY,
            )

    def test_unique_standard_definition(self):
        OptionDefinition.objects.create(
            standard=True,
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=True,
            space=OptionSpaceChoices.DHCPV4,
            name="name2",
            code=251,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=True,
            space=OptionSpaceChoices.DHCPV6,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )

        self.assertEqual(OptionDefinition.objects.filter(code__gte=250).count(), 3)

    def test_standard_and_global_definition_unique(self):
        OptionDefinition.objects.create(
            standard=True,
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )

    def test_standard_and_client_class_definition_unique(self):
        OptionDefinition.objects.create(
            standard=True,
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[1],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )

    def test_global_and_client_class_definition_unique(self):
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[1],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )

    def test_standard_definition_duplicate_name_fail(self):
        OptionDefinition.objects.create(
            standard=True,
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=True,
                space=OptionSpaceChoices.DHCPV4,
                name="name1",
                code=251,
                type=OptionTypeChoices.TYPE_EMPTY,
            ).full_clean()

    def test_standard_definition_duplicate_code_fail(self):
        OptionDefinition.objects.create(
            standard=True,
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=True,
                space=OptionSpaceChoices.DHCPV4,
                name="name2",
                code=250,
                type=OptionTypeChoices.TYPE_EMPTY,
            ).full_clean()

    def test_unique_global_definition(self):
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[1],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name2",
            code=251,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[0],
            space=OptionSpaceChoices.DHCPV6,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )

        self.assertEqual(OptionDefinition.objects.filter(code__gte=250).count(), 4)

    def test_global_definition_duplicate_name_fail(self):
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=False,
                dhcp_server=self.dhcp_servers[0],
                space=OptionSpaceChoices.DHCPV4,
                name="name1",
                code=251,
                type=OptionTypeChoices.TYPE_EMPTY,
            )

    def test_global_definition_duplicate_code_fail(self):
        OptionDefinition.objects.create(
            standard=False,
            dhcp_server=self.dhcp_servers[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=False,
                dhcp_server=self.dhcp_servers[0],
                space=OptionSpaceChoices.DHCPV4,
                name="name2",
                code=250,
                type=OptionTypeChoices.TYPE_EMPTY,
            )

    def test_unique_client_class_definition(self):
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[1],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name2",
            code=251,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[0],
            space=OptionSpaceChoices.DHCPV6,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )

        self.assertEqual(OptionDefinition.objects.filter(code__gte=250).count(), 4)

    def test_client_class_definition_duplicate_name_fail(self):
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=False,
                client_class=self.client_classes[0],
                space=OptionSpaceChoices.DHCPV4,
                name="name1",
                code=251,
                type=OptionTypeChoices.TYPE_EMPTY,
            )

    def test_client_class_definition_duplicate_code_fail(self):
        OptionDefinition.objects.create(
            standard=False,
            client_class=self.client_classes[0],
            space=OptionSpaceChoices.DHCPV4,
            name="name1",
            code=250,
            type=OptionTypeChoices.TYPE_EMPTY,
        )
        with self.assertRaises(ValidationError):
            OptionDefinition.objects.create(
                standard=False,
                client_class=self.client_classes[0],
                space=OptionSpaceChoices.DHCPV4,
                name="name2",
                code=250,
                type=OptionTypeChoices.TYPE_EMPTY,
            )
