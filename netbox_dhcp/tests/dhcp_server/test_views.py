from netbox_dhcp.choices import (
    DHCPServerIDTypeChoices,
    DHCPServerStatusChoices,
    HostReservationIdentifierChoices,
)
from netbox_dhcp.models import (
    DHCPCluster,
    DHCPServer,
)
from netbox_dhcp.tests.custom import (
    ModelViewTestCase,
)
from utilities.testing import ViewTestCases


class DHCPServerViewTestCase(
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
    model = DHCPServer

    @classmethod
    def setUpTestData(cls):
        dhcp_cluster = DHCPCluster.objects.create(
            name="test-cluster-1",
        )

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

        cls.form_data = {
            "name": "test-server-7",
            "description": "Test Description",
            "status": DHCPServerStatusChoices.STATUS_ACTIVE,
            "dhcp_cluster": None,
            "server_id": DHCPServerIDTypeChoices.ID_LL,
            "host_reservation_identifiers": [
                HostReservationIdentifierChoices.HW_ADDRESS,
                HostReservationIdentifierChoices.CLIENT_ID,
            ],
            "echo_client_id": False,
        }

        cls.bulk_edit_data = {
            "description": "Test Description Update",
            "status": DHCPServerStatusChoices.STATUS_INACTIVE,
            "dhcp_cluster": dhcp_cluster.pk,
            "server_id": DHCPServerIDTypeChoices.ID_EN,
            "host_reservation_identifiers": [
                HostReservationIdentifierChoices.HW_ADDRESS,
                HostReservationIdentifierChoices.DUID,
            ],
            "echo_client_id": True,
            "relay_supplied_options": "110,120,130",
        }

        cls.csv_data = (
            "name,description,status,dhcp_cluster,server_id,relay_supplied_options",
            f'test-server-4,Test Server 4,{DHCPServerStatusChoices.STATUS_ACTIVE},{dhcp_cluster.name},{DHCPServerIDTypeChoices.ID_EN},"110,120,130"',  # noqa: E501
            f'test-server-5,Test Server 5,{DHCPServerStatusChoices.STATUS_INACTIVE},{dhcp_cluster.name},{DHCPServerIDTypeChoices.ID_LLT},"111,121,131"',  # noqa: E501
            f'test-server-6,Test Server 6,{DHCPServerStatusChoices.STATUS_ACTIVE},{dhcp_cluster.name},{DHCPServerIDTypeChoices.ID_LL},"112,122,132"',  # noqa: E501
        )

        cls.csv_update_data = (
            "id,description,status,dhcp_cluster,server_id,relay_supplied_options",
            f"{dhcp_servers[0].pk},Test Server 1 (updated),{DHCPServerStatusChoices.STATUS_INACTIVE},,{DHCPServerIDTypeChoices.ID_LL},",  # noqa: E501
            f"{dhcp_servers[1].pk},Test Server 2 (updated),{DHCPServerStatusChoices.STATUS_INACTIVE},,{DHCPServerIDTypeChoices.ID_LL},",  # noqa: E501
            f"{dhcp_servers[2].pk},Test Server 3 (updated),{DHCPServerStatusChoices.STATUS_INACTIVE},,{DHCPServerIDTypeChoices.ID_LL},",  # noqa: E501
        )

    maxDiff = None
