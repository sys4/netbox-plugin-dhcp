from netbox_dhcp.models import ClientClass
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
    TestObjects,
)
from utilities.testing import APIViewTestCases


class ClientClassAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = ClientClass

    brief_fields = [
        "description",
        "display",
        "id",
        "name",
        "template_test",
        "test",
        "url",
        "weight",
    ]

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()

        client_classs = (
            ClientClass(
                dhcp_server=dhcp_servers[0],
                name="test-client-class-1",
                description="Test Client Class 1",
            ),
            ClientClass(
                dhcp_server=dhcp_servers[0],
                name="test-client-class-2",
                description="Test Client Class 2",
            ),
            ClientClass(
                dhcp_server=dhcp_servers[0],
                name="test-client-class-3",
                description="Test Client Class 3",
            ),
        )
        ClientClass.objects.bulk_create(client_classs)

        cls.create_data = [
            {
                "name": "test-client-class-4",
                "description": "Test Client Class 4",
                "dhcp_server": dhcp_servers[1].pk,
                "test": "substring(option[61].hex,0,3) == 'foo'",
                "only_in_additional_list": False,
            },
            {
                "name": "test-client-class-5",
                "description": "Test Client Class 5",
                "dhcp_server": dhcp_servers[1].pk,
                "template_test": "substring(option[61].hex,0,3)",
                "only_in_additional_list": True,
            },
            {
                "name": "test-client-class-6",
                "description": "Test Client Class 6",
                "dhcp_server": dhcp_servers[1].pk,
                "test": "substring(option[61].hex,0,3) == 'baz'",
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "test": "",
            "template_test": "",
            "only_in_additional_list": False,
        }
