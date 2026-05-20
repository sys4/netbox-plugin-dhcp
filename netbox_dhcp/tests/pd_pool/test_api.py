from netbox_dhcp.models import PDPool, Subnet
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
    TestObjects,
)
from utilities.testing import APIViewTestCases


class PDPoolAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = PDPool

    brief_fields = [
        "delegated_length",
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
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])
        ipv6_prefixes = TestObjects.get_ipv6_prefixes()

        subnet = Subnet.objects.create(
            name="test-subnet-1",
            dhcp_server=dhcp_servers[0],
            prefix=ipv6_prefixes[0],
        )

        pd_pools = (
            PDPool(
                name="test-pd-pool-1",
                description="Test Prefix Delegation Pool 1",
                subnet=subnet,
                prefix=ipv6_prefixes[0],
                delegated_length=64,
            ),
            PDPool(
                name="test-pd-pool-2",
                description="Test Prefix Delegation Pool 2",
                subnet=subnet,
                prefix=ipv6_prefixes[1],
                delegated_length=64,
            ),
            PDPool(
                name="test-pd-pool-3",
                description="Test Prefix Delegation Pool 3",
                subnet=subnet,
                prefix=ipv6_prefixes[2],
                delegated_length=64,
            ),
        )
        PDPool.objects.bulk_create(pd_pools)

        cls.create_data = [
            {
                "name": "test-pd-pool-4",
                "description": "Test Prefix Delegation Pool 4",
                "subnet": subnet.pk,
                "prefix": ipv6_prefixes[0].pk,
                "delegated_length": 64,
                "excluded_prefix": ipv6_prefixes[1].pk,
                "client_classes": [
                    client_class.pk for client_class in client_classes[1:3]
                ],
            },
            {
                "name": "test-pd-pool-5",
                "description": "Test Prefix Delegation Pool 5",
                "subnet": subnet.pk,
                "prefix": ipv6_prefixes[1].pk,
                "delegated_length": 64,
            },
            {
                "name": "test-pd-pool-6",
                "description": "Test Prefix Delegation Pool 6",
                "subnet": subnet.pk,
                "prefix": ipv6_prefixes[2].pk,
                "delegated_length": 64,
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "client_classes": [client_class.pk for client_class in client_classes],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[0:2]
            ],
        }
