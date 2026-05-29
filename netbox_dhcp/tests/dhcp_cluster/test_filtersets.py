from django.test import TestCase

from netbox_dhcp.choices import DHCPClusterStatusChoices
from netbox_dhcp.filtersets import DHCPClusterFilterSet
from netbox_dhcp.models import DHCPCluster
from utilities.testing import ChangeLoggedFilterSetTests


class DHCPClusterFilterSetTestCase(
    TestCase,
    ChangeLoggedFilterSetTests,
):
    queryset = DHCPCluster.objects.all()
    filterset = DHCPClusterFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_clusters = (
            DHCPCluster(
                name="test-cluster-1",
                status=DHCPClusterStatusChoices.STATUS_ACTIVE,
                description="Test Cluster 1",
            ),
            DHCPCluster(
                name="test-cluster-2",
                status=DHCPClusterStatusChoices.STATUS_INACTIVE,
                description="Test Cluster 2",
            ),
            DHCPCluster(
                name="test-cluster-3",
                status=DHCPClusterStatusChoices.STATUS_ACTIVE,
                description="Test Cluster 3",
            ),
        )
        DHCPCluster.objects.bulk_create(cls.dhcp_clusters)

    def test_name(self):
        params = {"name": ["test-cluster-1", "test-cluster-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_description(self):
        params = {"description": ["Test Cluster 1", "Test Cluster 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_status(self):
        params = {"status": [DHCPClusterStatusChoices.STATUS_ACTIVE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"status": [DHCPClusterStatusChoices.STATUS_INACTIVE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
