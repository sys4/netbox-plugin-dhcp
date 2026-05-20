from netbox_dhcp.choices import DHCPClusterStatusChoices
from netbox_dhcp.models import DHCPCluster
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
)
from utilities.testing import APIViewTestCases


class DHCPClusterAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = DHCPCluster

    brief_fields = [
        "description",
        "display",
        "id",
        "name",
        "status",
        "url",
    ]

    @classmethod
    def setUpTestData(cls):
        dhcp_clusters = (
            DHCPCluster(
                name="test-cluster-1",
            ),
            DHCPCluster(
                name="test-cluster-2",
            ),
            DHCPCluster(
                name="test-cluster-3",
            ),
        )
        DHCPCluster.objects.bulk_create(dhcp_clusters)

        cls.create_data = [
            {
                "name": "test-cluster-4",
            },
            {
                "name": "test-cluster-5",
            },
            {
                "name": "test-cluster-6",
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "status": DHCPClusterStatusChoices.STATUS_INACTIVE,
        }
