from netbox_dhcp.models import SharedNetwork
from netbox_dhcp.tests.custom import (
    ModelViewTestCase,
    TestObjects,
)
from utilities.testing import ViewTestCases


class SharedNetworkViewTestCase(
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
    model = SharedNetwork

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

        cls.form_data = {
            "name": "test-shared-network-4",
            "description": "Test Shared Network 4",
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
            "prefix": ipv6_prefixes[1].pk,
            "client_classes": [client_classes[0].pk],
            "evaluate_additional_classes": [client_classes[2].pk],
        }

        cls.csv_data = (
            "name,description,weight,dhcp_server,prefix,client_classes,evaluate_additional_classes",  # noqa: E501
            f'test-shared-network-4,Test Shared Network 4,23,{dhcp_servers[0].name},{ipv4_prefixes[0].prefix},{client_classes[0].name},"{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'test-shared-network-5,Test Shared Network 5,42,{dhcp_servers[1].name},{ipv4_prefixes[1].prefix},{client_classes[1].name},"{client_classes[2].name},{client_classes[0].name}"',  # noqa: E501
            f'test-shared-network-6,Test Shared Network 6,100,{dhcp_servers[2].name},{ipv4_prefixes[2].prefix},{client_classes[2].name},"{client_classes[0].name},{client_classes[1].name}"',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description,weight,client_classes,evaluate_additional_classes",  # noqa: E501
            f'{shared_networks[0].pk},Test Shared Network 1 (updated),100,{client_classes[1].name},"{client_classes[2].name},{client_classes[0].name}"',  # noqa: E501
            f'{shared_networks[1].pk},Test Shared Network 2 (updated),23,{client_classes[2].name},"{client_classes[0].name},{client_classes[1].name}"',  # noqa: E501
            f'{shared_networks[2].pk},Test Shared Network 3 (updated),42,{client_classes[0].name},"{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
        )

    maxDiff = None
