from utilities.testing import ViewTestCases
from ipam.choices import IPAddressFamilyChoices

from netbox_dhcp.tests.custom import ModelViewTestCase, TestObjects
from netbox_dhcp.models import OptionDefinition
from netbox_dhcp.choices import (
    OptionTypeChoices,
    OptionSpaceChoices,
)


class OptionDefinitionViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = OptionDefinition

    def _get_queryset(self):
        return self.model.objects.filter(standard=False)

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()

        option_definitions = (
            OptionDefinition(
                name="test-option-definition-1",
                description="Test Option Definition 1",
                code=251,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_STRING,
                space=OptionSpaceChoices.DHCPV4,
                dhcp_server=dhcp_servers[0],
            ),
            OptionDefinition(
                name="test-option-definition-2",
                description="Test Option Definition 2",
                code=252,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_IPV4_ADDRESS,
                space=OptionSpaceChoices.DHCPV4,
                dhcp_server=dhcp_servers[0],
            ),
            OptionDefinition(
                name="test-option-definition-3",
                description="Test Option Definition 3",
                code=253,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_IPV4_ADDRESS,
                space=OptionSpaceChoices.DHCPV4,
                dhcp_server=dhcp_servers[0],
            ),
        )
        OptionDefinition.objects.bulk_create(option_definitions)

        cls.form_data = {
            "name": "test-option_definition-7",
            "description": "Test Option Definition 7",
            "code": 254,
            "family": IPAddressFamilyChoices.FAMILY_4,
            "type": OptionTypeChoices.TYPE_STRING,
            "space": OptionSpaceChoices.DHCPV4,
            "dhcp_server": dhcp_servers[0].pk,
        }

        cls.bulk_edit_data = {
            "description": "Test Description Update",
        }

        cls.csv_data = (
            "name,description,space,family,code,type,record_types,array,dhcp_server",
            f"test-option_definition-4,Test Option Definition 4,{OptionSpaceChoices.DHCPV4},{IPAddressFamilyChoices.FAMILY_4},248,{OptionTypeChoices.TYPE_STRING},,false,{dhcp_servers[0].name}",  # noqa: E501
            f"test-option_definition-5,Test Option Definition 5,{OptionSpaceChoices.DHCPV4},{IPAddressFamilyChoices.FAMILY_4},249,{OptionTypeChoices.TYPE_IPV4_ADDRESS},,true,{dhcp_servers[0].name}",  # noqa: E501
            f'test-option_definition-6,Test Option Definition 6,{OptionSpaceChoices.DHCPV4},{IPAddressFamilyChoices.FAMILY_4},250,{OptionTypeChoices.TYPE_RECORD},"{OptionTypeChoices.TYPE_UINT32},{OptionTypeChoices.TYPE_STRING}",false,{dhcp_servers[0].name}',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description",
            f"{option_definitions[0].pk},Test Option Definition 1 (updated)",
            f"{option_definitions[1].pk},Test Option Definition 2 (updated)",
            f"{option_definitions[2].pk},Test Option Definition 3 (updated)",
        )

    maxDiff = None
