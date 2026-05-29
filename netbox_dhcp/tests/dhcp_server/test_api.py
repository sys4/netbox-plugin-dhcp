from netbox_dhcp.choices import (
    DHCPServerIDTypeChoices,
    DHCPServerStatusChoices,
    HostReservationIdentifierChoices,
)
from netbox_dhcp.models import DHCPServer
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
    TestObjects,
)
from utilities.testing import APIViewTestCases


class DHCPServerAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = DHCPServer

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
        dhcp_servers = (
            DHCPServer(
                name="test-server-1",
            ),
            DHCPServer(
                name="test-server-2",
            ),
            DHCPServer(
                name="test-server-3",
            ),
        )
        DHCPServer.objects.bulk_create(dhcp_servers)

        dhcp_clusters = TestObjects.get_dhcp_clusters()

        cls.create_data = [
            {
                "name": "test-server-4",
                "dhcp_cluster": dhcp_clusters[0].pk,
            },
            {
                "name": "test-server-5",
                "dhcp_cluster": dhcp_clusters[1].pk,
            },
            {
                "name": "test-server-6",
                "dhcp_cluster": dhcp_clusters[2].pk,
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "status": DHCPServerStatusChoices.STATUS_INACTIVE,
            "dhcp_cluster": dhcp_clusters[2].pk,
            "server_id": DHCPServerIDTypeChoices.ID_EN,
            "host_reservation_identifiers": [
                HostReservationIdentifierChoices.HW_ADDRESS,
                HostReservationIdentifierChoices.DUID,
            ],
            "echo_client_id": True,
            "relay_supplied_options": [110, 120, 130],
        }
