from netbox_dhcp.choices import DHCPClusterStatusChoices
from netbox_dhcp.models import DHCPCluster
from netbox_dhcp.tests.custom import ModelViewTestCase
from utilities.testing import ViewTestCases


class DHCPClusterViewTestCase(
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
    model = DHCPCluster

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

        cls.form_data = {
            "name": "test-cluster-7",
            "description": "Test Description",
            "status": DHCPClusterStatusChoices.STATUS_ACTIVE,
        }

        cls.bulk_edit_data = {
            "description": "Test Description Update",
            "status": DHCPClusterStatusChoices.STATUS_INACTIVE,
        }

        cls.csv_data = (
            "name,description,status",
            f"test-cluster-4,Test Cluster 4,{DHCPClusterStatusChoices.STATUS_ACTIVE}",
            f"test-cluster-5,Test Cluster 5,{DHCPClusterStatusChoices.STATUS_INACTIVE}",
            f"test-cluster-6,Test Cluster 6,{DHCPClusterStatusChoices.STATUS_ACTIVE}",
        )

        cls.csv_update_data = (
            "id,description,status",
            f"{dhcp_clusters[0].pk},Test Cluster 1 (updated),{DHCPClusterStatusChoices.STATUS_INACTIVE}",
            f"{dhcp_clusters[1].pk},Test Cluster 2 (updated),{DHCPClusterStatusChoices.STATUS_INACTIVE}",
            f"{dhcp_clusters[2].pk},Test Cluster 3 (updated),{DHCPClusterStatusChoices.STATUS_INACTIVE}",
        )

    maxDiff = None
