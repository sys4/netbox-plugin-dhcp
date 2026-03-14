from utilities.testing import ViewTestCases

from netbox_dhcp.tests.custom import TestObjects, ModelViewTestCase
from netbox_dhcp.models import PDPool, Subnet


class PDPoolViewTestCase(
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
    model = PDPool

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
                prefix=ipv6_prefixes[1],
                delegated_length=64,
                excluded_prefix=ipv6_prefixes[1],
            ),
            PDPool(
                name="test-pd-pool-2",
                description="Test Prefix Delegation Pool 2",
                subnet=subnet,
                prefix=ipv6_prefixes[2],
                delegated_length=64,
            ),
            PDPool(
                name="test-pd-pool-3",
                description="Test Prefix Delegation Pool 3",
                subnet=subnet,
                prefix=ipv6_prefixes[3],
                delegated_length=64,
            ),
        )
        PDPool.objects.bulk_create(pd_pools)

        cls.form_data = {
            "name": "test-pd-pool-7",
            "description": "Test Prefix Delegation Pool 7",
            "weight": 100,
            "subnet": subnet.pk,
            "prefix": ipv6_prefixes[1].pk,
            "delegated_length": 96,
            "excluded_prefix": ipv6_prefixes[6].pk,
            "client_classes": [client_class.pk for client_class in client_classes[1:3]],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[1:3]
            ],
        }

        cls.bulk_edit_data = {
            "description": "Test Description Bulk Update",
            "weight": 100,
            "subnet": subnet.pk,
            "delegated_length": 72,
            #           "excluded_prefix": None,
            "client_classes": [client_class.pk for client_class in client_classes[1:3]],
            "evaluate_additional_classes": [
                client_class.pk for client_class in client_classes[1:3]
            ],
        }

        cls.csv_data = (
            "name,description,weight,subnet,prefix,delegated_length,excluded_prefix,client_classes,evaluate_additional_classes",  # noqa: E501
            f'test-pd-pool-4,Test Prefix Delegation Pool 4,42,{subnet.name},{ipv6_prefixes[0].prefix},64,,"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'test-pd-pool-5,Test Prefix Delegation Pool 5,23,{subnet.name},{ipv6_prefixes[1].prefix},64,{ipv6_prefixes[4].prefix},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'test-pd-pool-6,Test Prefix Delegation Pool 6,100,{subnet.name},{ipv6_prefixes[2].prefix},64,{ipv6_prefixes[6].prefix},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description,weight,prefix,delegated_length,excluded_prefix,client_classes,evaluate_additional_classes",  # noqa: E501
            f'{pd_pools[0].pk},Test Prefix Delegation Pool 4,100,{ipv6_prefixes[0].prefix},64,{ipv6_prefixes[1].prefix},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'{pd_pools[1].pk},Test Prefix Delegation Pool 5,23,{ipv6_prefixes[1].prefix},64,{ipv6_prefixes[5].prefix},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
            f'{pd_pools[2].pk},Test Prefix Delegation Pool 6,42,{ipv6_prefixes[2].prefix},64,{ipv6_prefixes[7].prefix},"{client_classes[0].name},{client_classes[1].name}","{client_classes[1].name},{client_classes[2].name}"',  # noqa: E501
        )

    maxDiff = None
