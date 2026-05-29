from django.contrib.contenttypes.models import ContentType

from netbox_dhcp.choices import OptionSendChoices, OptionSpaceChoices
from netbox_dhcp.models import DHCPServer, Option, OptionDefinition
from netbox_dhcp.tests.custom import ModelViewTestCase, TestObjects
from utilities.testing import ViewTestCases


class OptionViewTestCase(
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
    model = Option

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()
        cls.client_classes = TestObjects.get_client_classes(
            dhcp_server=cls.dhcp_servers[0]
        )
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
                assigned_object=cls.dhcp_servers[0],
                data="true",
            ),
            Option(
                description="Test Option 2",
                definition=cls.option_definitions[2],
                assigned_object=cls.dhcp_servers[0],
                data="1480",
                send_option=OptionSendChoices.NEVER_SEND,
            ),
            Option(
                description="Test Option 3",
                definition=cls.option_definitions[2],
                assigned_object=cls.dhcp_servers[0],
                data="1320",
                send_option=OptionSendChoices.ALWAYS_SEND,
            ),
        )
        Option.objects.bulk_create(cls.options)

        cls.form_data = {
            "definition": cls.option_definitions[0].pk,
            "description": "Test Option 4",
            "data": "192.0.2.1, 192.0.2.2",
            "weight": 100,
            "send_option": OptionSendChoices.ALWAYS_SEND,
            "client_classes": [
                client_class.pk for client_class in cls.client_classes[0:2]
            ],
            "assigned_object_id": cls.dhcp_servers[0].pk,
            "assigned_object_type": cls.dhcp_server_type.pk,
        }

        cls.bulk_edit_data = {
            "definition": cls.option_definitions[1].pk,
            "description": "Test Description Update",
            "data": "192.0.2.1, 192.0.2.2",
            "weight": 50,
            "client_classes": [
                client_class.pk for client_class in cls.client_classes[1:3]
            ],
        }

        cls.csv_data = (
            "description,space,name,code,data,weight,dhcp_server,send_option,csv_format,client_classes",  # noqa: E501
            f'Test Option 1,dhcp4,routers,,"192.0.2.1,192.0.2.2",100,{cls.dhcp_servers[0].name},,true,"{cls.client_classes[0].name},{cls.client_classes[2].name}"',  # noqa: E501
            f'Test Option 2,dhcp4,,3,"192.0.2.3,192.0.2.4",120,{cls.dhcp_servers[1].name},{OptionSendChoices.NEVER_SEND},false,"{cls.client_classes[1].name},{cls.client_classes[2].name}"',  # noqa: E501
            f'Test Option 3,dhcp4,domain-name-servers,,"192.0.2.5,192.0.2.6",,{cls.dhcp_servers[2].name},{OptionSendChoices.ALWAYS_SEND},false,"{cls.client_classes[0].name},{cls.client_classes[1].name}"',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description,weight",
            f"{cls.options[0].pk},Test Option 1 (updated),50",
            f"{cls.options[1].pk},Test Option 2 (updated),30",
            f"{cls.options[2].pk},Test Potion 3 (updated),20",
        )

    maxDiff = None
