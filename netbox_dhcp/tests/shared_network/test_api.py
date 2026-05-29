from netbox_dhcp.models import SharedNetwork
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
    TestObjects,
)
from utilities.testing import APIViewTestCases


class SharedNetworkAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = SharedNetwork

    brief_fields = [
        "description",
        "display",
        "id",
        "name",
        "prefix_display",
        "url",
        "weight",
    ]

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()
        ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])

        shared_networks = (
            SharedNetwork(
                name="test-shared-network-1",
                description="Test Shared Network 1",
                dhcp_server=dhcp_servers[0],
                prefix=ipv4_prefixes[0],
            ),
            SharedNetwork(
                name="test-shared-network-2",
                description="Test Shared Network 2",
                dhcp_server=dhcp_servers[0],
                prefix=ipv4_prefixes[1],
            ),
            SharedNetwork(
                name="test-shared-network-3",
                description="Test Shared Network 3",
                dhcp_server=dhcp_servers[0],
                prefix=ipv4_prefixes[2],
            ),
        )
        SharedNetwork.objects.bulk_create(shared_networks)

        cls.create_data = [
            {
                "name": "test-shared-network-4",
                "description": "Test Shared Network 4",
                "dhcp_server": dhcp_servers[0].pk,
                "prefix": ipv6_prefixes[0].pk,
                "client_classes": [
                    client_class.pk for client_class in client_classes[0:2]
                ],
                "evaluate_additional_classes": [
                    client_class.pk for client_class in client_classes[0:2]
                ],
            },
            {
                "name": "test-shared-network-5",
                "description": "Test Shared Network 5",
                "dhcp_server": dhcp_servers[0].pk,
                "prefix": ipv6_prefixes[1].pk,
                "client_classes": [
                    client_class.pk for client_class in client_classes[1:3]
                ],
                "evaluate_additional_classes": [
                    client_class.pk for client_class in client_classes[0:2]
                ],
            },
            {
                "name": "test-shared-network-6",
                "description": "Test Shared Network 6",
                "dhcp_server": dhcp_servers[0].pk,
                "prefix": ipv6_prefixes[2].pk,
                "client_classes": [
                    client_class.pk for client_class in client_classes[0:3]
                ],
                "evaluate_additional_classes": [
                    client_class.pk for client_class in client_classes[1:2]
                ],
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "prefix": ipv6_prefixes[1].pk,
            "client_classes": [client_classes[0].pk],
            "evaluate_additional_classes": [client_classes[2].pk],
        }
