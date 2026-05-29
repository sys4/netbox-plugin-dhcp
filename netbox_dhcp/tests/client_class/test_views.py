from netbox_dhcp.models import ClientClass
from netbox_dhcp.tests.custom import (
    ModelViewTestCase,
    TestObjects,
)
from utilities.testing import ViewTestCases


class ClientClassViewTestCase(
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
    model = ClientClass

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()

        client_classes = (
            ClientClass(
                name="test-client-class-1",
                description="Test Client Class 1",
                dhcp_server=dhcp_servers[0],
            ),
            ClientClass(
                name="test-client-class-2",
                description="Test Client Class 2",
                dhcp_server=dhcp_servers[0],
            ),
            ClientClass(
                name="test-client-class-3",
                description="Test Client Class 3",
                dhcp_server=dhcp_servers[0],
            ),
        )
        ClientClass.objects.bulk_create(client_classes)

        cls.form_data = {
            "name": "test-client-class-4",
            "description": "Test Client Class 4",
            "weight": 100,
            "dhcp_server": dhcp_servers[1].pk,
            "test": "substring(option[61].hex,0,3) == 'foo'",
            "only_in_additional_list": False,
        }

        cls.bulk_edit_data = {
            "description": "Test Description Update",
            "test": "substring(option[61].hex,0,3) == 'bar'",
            "weight": 30,
            "dhcp_server": dhcp_servers[1].pk,
            "template_test": "",
            "only_in_additional_list": False,
        }

        cls.csv_data = (
            "name,description,weight,dhcp_server,test,template_test,only_in_additional_list",
            f"test-client-class-5,Test Client Class 5,42,{dhcp_servers[2].name},\"substring(option[42].hex,0,3) == 'baz'\",,true",
            f"test-client-class-6,Test Client Class 6,23,{dhcp_servers[0].name},\"substring(option[23].hex,0,3) == 'foo'\",,false",
            f'test-client-class-7,Test Client Class 7,100,{dhcp_servers[1].name},,"substring(option[23].hex,0,3)",true',
        )

        cls.csv_update_data = (
            "id,name,description,weight,dhcp_server,test,template_test,only_in_additional_list",
            f"{client_classes[0].pk},test-client-class-5,Test Client Class 5,100,{dhcp_servers[1].name},\"substring(option[42].hex,0,3) == 'baz'\",,true",  # noqa: E501
            f"{client_classes[1].pk},test-client-class-6,Test Client Class 6,23,{dhcp_servers[1].name},\"substring(option[23].hex,0,3) == 'foo'\",,false",  # noqa: E501
            f'{client_classes[2].pk},test-client-class-7,Test Client Class 7,42,{dhcp_servers[1].name},,"substring(option[23].hex,0,3)",true',  # noqa: E501
        )

    maxDiff = None
