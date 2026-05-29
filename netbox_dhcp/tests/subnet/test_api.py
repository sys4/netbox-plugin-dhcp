from netbox_dhcp.models import Subnet
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
    TestObjects,
)
from utilities.testing import APIViewTestCases


class SubnetAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Subnet

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

        subnets = (
            Subnet(
                name="test-subnet-1",
                description="Test Subnet 1",
                dhcp_server=dhcp_servers[0],
                prefix=ipv4_prefixes[0],
            ),
            Subnet(
                name="test-subnet-2",
                dhcp_server=dhcp_servers[0],
                description="Test Subnet 2",
                prefix=ipv4_prefixes[1],
            ),
            Subnet(
                name="test-subnet-3",
                dhcp_server=dhcp_servers[0],
                description="Test Subnet 3",
                prefix=ipv4_prefixes[2],
            ),
        )
        for subnet in subnets:
            subnet.save()

        cls.create_data = [
            {
                "name": "test-subnet-4",
                "description": "Test Subnet 4",
                "dhcp_server": dhcp_servers[1].pk,
                "prefix": ipv6_prefixes[0].pk,
                "client_classes": [
                    client_class.pk for client_class in client_classes[0:2]
                ],
                "evaluate_additional_classes": [
                    client_class.pk for client_class in client_classes[0:2]
                ],
            },
            {
                "name": "test-subnet-5",
                "description": "Test Subnet 5",
                "dhcp_server": dhcp_servers[1].pk,
                "prefix": ipv6_prefixes[1].pk,
                "client_classes": [
                    client_class.pk for client_class in client_classes[1:3]
                ],
                "evaluate_additional_classes": [
                    client_class.pk for client_class in client_classes[0:2]
                ],
            },
            {
                "name": "test-subnet-6",
                "description": "Test Subnet 6",
                "dhcp_server": dhcp_servers[1].pk,
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
