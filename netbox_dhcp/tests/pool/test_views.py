from utilities.testing import ViewTestCases

from netbox_dhcp.tests.custom import TestObjects, ModelViewTestCase
from netbox_dhcp.models import Pool, Subnet


class IPv4PoolViewTestCase(
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
    model = Pool

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])
        ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        ipv4_ranges = TestObjects.get_ipv4_ranges()

        ipv4_subnets = (
            Subnet(
                name="test-ipv4-subnet-1",
                dhcp_server=dhcp_servers[0],
                prefix=ipv4_prefixes[0],  # 198.18.0.0/16
            ),
            Subnet(
                name="test-ipv4-subnet-2",
                dhcp_server=dhcp_servers[0],
                prefix=ipv4_prefixes[3],  # 198.18.2.0/24
            ),
        )
        for subnet in ipv4_subnets:
            subnet.save()

        pools = (
            Pool(
                name="test-pool-1",
                description="Test Pool 1",
                subnet=ipv4_subnets[0],  # 198.18.0.0/16
                ip_range=ipv4_ranges[0],  # 198.18.2.1/24 - 198.18.2.16/24
            ),
            Pool(
                name="test-pool-2",
                description="Test Pool 2",
                subnet=ipv4_subnets[0],  # 198.18.0.0/16
                ip_range=ipv4_ranges[1],  # 198.18.2.17/24 - 198.18.2.32/24
            ),
            Pool(
                name="test-pool-3",
                description="Test Pool 3",
                subnet=ipv4_subnets[0],  # 198.18.0.0/16
                ip_range=ipv4_ranges[2],  # 198.18.2.33/24 - 198.18.2.64/24
            ),
        )
        Pool.objects.bulk_create(pools)

        cls.form_data = {
            "name": "test-pool-4",
            "description": "Test Pool 4",
            "weight": 100,
            "subnet": ipv4_subnets[0].pk,
            "ip_range": ipv4_ranges[2].pk,
            "client_classes": [client_class.pk for client_class in client_classes],
        }

        cls.bulk_edit_data = {
            "description": "Test Description Update",
            "weight": 100,
            "subnet": ipv4_subnets[1].pk,
            "client_class": client_classes[2].pk,
            "client_classes": [],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[0:2]
            ],
        }

        cls.csv_data = (
            "name,description,weight,subnet,ip_range,client_classes,evaluate_additional_classes",  # noqa: E501
            f'test-pool-6,Test Pool 6,100,{ipv4_subnets[0].name},{ipv4_ranges[0].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'test-pool-7,Test Pool 7,23,{ipv4_subnets[1].name},{ipv4_ranges[1].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description,weight,ip_range,client_classes,evaluate_additional_classes",  # noqa: E501
            f'{pools[0].pk},Test Pool 1 (updated),42,{ipv4_ranges[0].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'{pools[1].pk},Test Pool 2 (updated),23,{ipv4_ranges[1].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
        )

    maxDiff = None


class IPv6PoolViewTestCase(
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
    model = Pool

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])
        ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        ipv6_ranges = TestObjects.get_ipv6_ranges()

        ipv6_subnets = (
            Subnet(
                name="test-ipv6-subnet-1",
                dhcp_server=dhcp_servers[0],
                prefix=ipv6_prefixes[0],  # 2001:db8::/32
            ),
            Subnet(
                name="test-ipv6-subnet-2",
                dhcp_server=dhcp_servers[0],
                prefix=ipv6_prefixes[1],  # 2001:db8:0:1::/64
            ),
        )
        for subnet in ipv6_subnets:
            subnet.save()

        pools = (
            Pool(
                name="test-pool-1",
                description="Test Pool 1",
                subnet=ipv6_subnets[0],
                ip_range=ipv6_ranges[0],
            ),
            Pool(
                name="test-pool-2",
                description="Test Pool 2",
                subnet=ipv6_subnets[0],
                ip_range=ipv6_ranges[1],
            ),
            Pool(
                name="test-pool-3",
                description="Test Pool 3",
                subnet=ipv6_subnets[0],
                ip_range=ipv6_ranges[2],
            ),
        )
        Pool.objects.bulk_create(pools)

        cls.form_data = {
            "name": "test-pool-5",
            "description": "Test Pool 5",
            "weight": 100,
            "subnet": ipv6_subnets[1].pk,
            "ip_range": ipv6_ranges[2].pk,
            "client_classes": [client_class.pk for client_class in client_classes],
        }

        cls.bulk_edit_data = {
            "description": "Test Description Update",
            "weight": 100,
            "subnet": ipv6_subnets[0].pk,
            "client_class": client_classes[2].pk,
            "client_classes": [],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[0:2]
            ],
        }

        cls.csv_data = (
            "name,description,weight,subnet,ip_range,client_classes,evaluate_additional_classes",  # noqa: E501
            f'test-pool-6,Test Pool 6,100,{ipv6_subnets[1].name},{ipv6_ranges[0].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'test-pool-7,Test Pool 7,23,{ipv6_subnets[1].name},{ipv6_ranges[1].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description,weight,ip_range,client_classes,evaluate_additional_classes",  # noqa: E501
            f'{pools[0].pk},Test Pool 1 (updated),42,{ipv6_ranges[0].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'{pools[1].pk},Test Pool 2 (updated),23,{ipv6_ranges[1].pk},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
        )

    maxDiff = None
