from netbox_dhcp.models import Subnet
from netbox_dhcp.tests.custom import (
    ModelViewTestCase,
    TestObjects,
)
from utilities.testing import ViewTestCases


class SubnetViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    #   ViewTestCases.CreateObjectViewTestCase,
    #   ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = Subnet

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()
        ipv4_prefixes = TestObjects.get_ipv4_prefixes()
        ipv6_prefixes = TestObjects.get_ipv6_prefixes()
        client_classes = TestObjects.get_client_classes(dhcp_server=dhcp_servers[0])

        subnets = (
            Subnet(
                name="test-subnet-1",
                dhcp_server=dhcp_servers[0],
                description="Test Subnet 1",
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

        cls.form_data = {
            "name": "test-subnet-4",
            "description": "Test Subnet 4",
            "weight": 100,
            "dhcp_server": dhcp_servers[0].pk,
            "prefix": ipv6_prefixes[0].pk,
            "client_classes": [client_class.pk for client_class in client_classes[0:2]],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[0:2]
            ],
        }

        cls.bulk_edit_data = {
            "description": "Test Description Update",
            "weight": 100,
            "client_classes": [client_classes[0].pk],
            "evaluate_additional_classes": [client_classes[2].pk],
        }

        cls.csv_data = (
            "name,dhcp_server,description,weight,prefix,client_classes,evaluate_additional_classes",  # noqa: E501
            f'test-shared-network-4,{dhcp_servers[1].name},Test Subnet 4,100,{ipv4_prefixes[0].prefix},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'test-shared-network-5,{dhcp_servers[1].name},Test Subnet 5,23,{ipv4_prefixes[1].prefix},"{client_classes[1].name},{client_classes[2].name}","{client_classes[2].name},{client_classes[0].name}"',  # noqa: E501
            f'test-shared-network-6,{dhcp_servers[1].name},Test Subnet 6,42,{ipv4_prefixes[2].prefix},"{client_classes[2].name},{client_classes[0].name}","{client_classes[0].name},{client_classes[1].name}"',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description,weight,client_classes,evaluate_additional_classes",  # noqa: E501
            f'{subnets[0].pk},Test Subnet 1 (updated),23,"{client_classes[1].name},{client_classes[2].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'{subnets[1].pk},Test Subnet 2 (updated),100,"{client_classes[2].name},{client_classes[0].name}","{client_classes[2].name},{client_classes[0].name}"',  # noqa: E501
            f'{subnets[2].pk},Test Subnet 3 (updated),42,"{client_classes[0].name},{client_classes[1].name}","{client_classes[0].name},{client_classes[1].name}"',  # noqa: E501
        )
