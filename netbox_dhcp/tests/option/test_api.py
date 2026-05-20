from django.contrib.contenttypes.models import ContentType

from netbox_dhcp.choices import OptionSendChoices, OptionSpaceChoices
from netbox_dhcp.models import DHCPServer, Option, OptionDefinition
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
    TestObjects,
)
from utilities.testing import APIViewTestCases


class OptionAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Option

    brief_fields = [
        "code",
        "data",
        "description",
        "display",
        "id",
        "name",
        "space",
        "url",
        "weight",
    ]

    user_permissions = ("netbox_dhcp.view_optiondefinition",)

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )
        cls.dhcp_server = cls.dhcp_servers[0]
        cls.dhcp_server_type = ContentType.objects.get_for_model(DHCPServer)
        cls.dhcp_server_contenttype = (
            f"{cls.dhcp_server_type.app_label}.{cls.dhcp_server_type.model}"
        )

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
        )

        cls.options = (
            Option(
                description="Test Option 1",
                definition=cls.option_definitions[3],
                assigned_object=cls.dhcp_server,
                data="true",
                send_option=None,
            ),
            Option(
                description="Test Option 2",
                definition=cls.option_definitions[2],
                assigned_object=cls.dhcp_server,
                data="1480",
                send_option=OptionSendChoices.NEVER_SEND,
            ),
            Option(
                description="Test Option 3",
                definition=cls.option_definitions[2],
                assigned_object=cls.dhcp_server,
                data="1320",
                send_option=OptionSendChoices.ALWAYS_SEND,
            ),
        )
        Option.objects.bulk_create(cls.options)

        cls.create_data = [
            {
                "definition": cls.option_definitions[0].pk,
                "description": "Test Option 4",
                "assigned_object_id": cls.dhcp_server.pk,
                "assigned_object_type": cls.dhcp_server_contenttype,
                "data": "192.0.2.1, 192.0.2.2",
                "send_option": OptionSendChoices.ALWAYS_SEND,
                "client_classes": [
                    client_class.pk for client_class in cls.client_classes[0:2]
                ],
            },
            {
                "definition": cls.option_definitions[1].pk,
                "description": "Test Option 4",
                "assigned_object_id": cls.dhcp_server.pk,
                "assigned_object_type": cls.dhcp_server_contenttype,
                "data": "192.0.2.3, 192.0.2.4",
                "client_classes": [cls.client_classes[2].pk],
            },
            {
                "definition": cls.option_definitions[2].pk,
                "description": "Test Option 4",
                "assigned_object_id": cls.dhcp_server.pk,
                "assigned_object_type": cls.dhcp_server_contenttype,
                "data": "1380",
                "send_option": OptionSendChoices.NEVER_SEND,
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "client_classes": [],
            "send_option": None,
        }
