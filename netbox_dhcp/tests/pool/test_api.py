from utilities.testing import APIViewTestCases

from netbox_dhcp.tests.custom import (
    TestObjects,
    APITestCase,
    NetBoxDHCPGraphQLMixin,
)
from netbox_dhcp.models import Pool, Subnet


class IPv4PoolAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Pool

    brief_fields = [
        "description",
        "display",
        "id",
        "name",
        "url",
        "weight",
    ]

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])
        ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        ipv4_ranges = TestObjects.get_ipv4_ranges()

        ipv4_subnet = Subnet.objects.create(
            name="test-ipv4-subnet-1",
            dhcp_server=dhcp_servers[0],
            prefix=ipv4_prefixes[0],
        )

        pools = (
            Pool(
                name="test-pool-1",
                description="Test Pool 1",
                subnet=ipv4_subnet,
                ip_range=ipv4_ranges[0],
            ),
            Pool(
                name="test-pool-2",
                description="Test Pool 2",
                subnet=ipv4_subnet,
                ip_range=ipv4_ranges[1],
            ),
            Pool(
                name="test-pool-3",
                description="Test Pool 3",
                subnet=ipv4_subnet,
                ip_range=ipv4_ranges[2],
            ),
        )
        Pool.objects.bulk_create(pools)

        cls.create_data = [
            {
                "name": "test-pool-5",
                "description": "Test Pool 5",
                "subnet": ipv4_subnet.pk,
                "ip_range": ipv4_ranges[2].pk,
                "client_classes": [client_class.pk for client_class in client_classes],
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "client_classes": [client_class.pk for client_class in client_classes[1:3]],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[0:2]
            ],
        }


class IPv6PoolAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Pool

    brief_fields = [
        "description",
        "display",
        "id",
        "name",
        "url",
        "weight",
    ]

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])
        ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        ipv6_ranges = TestObjects.get_ipv6_ranges()

        ipv6_subnet = Subnet.objects.create(
            name="test-ipv6-subnet-1",
            dhcp_server=dhcp_servers[0],
            prefix=ipv6_prefixes[0],
        )

        pools = (
            Pool(
                name="test-pool-1",
                description="Test Pool 1",
                subnet=ipv6_subnet,
                ip_range=ipv6_ranges[0],
            ),
            Pool(
                name="test-pool-2",
                description="Test Pool 2",
                subnet=ipv6_subnet,
                ip_range=ipv6_ranges[1],
            ),
            Pool(
                name="test-pool-3",
                description="Test Pool 3",
                subnet=ipv6_subnet,
                ip_range=ipv6_ranges[2],
            ),
        )
        Pool.objects.bulk_create(pools)

        cls.create_data = [
            {
                "name": "test-pool-4",
                "description": "Test Pool 4",
                "subnet": ipv6_subnet.pk,
                "ip_range": ipv6_ranges[2].pk,
                "client_classes": [client_class.pk for client_class in client_classes],
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "client_classes": [client_class.pk for client_class in client_classes[1:3]],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[0:2]
            ],
        }
