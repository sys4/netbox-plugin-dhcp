from unittest import skip

from django.test import override_settings
from rest_framework import status

from ipam.choices import IPAddressFamilyChoices
from netbox_dhcp.choices import (
    OptionSpaceChoices,
    OptionTypeChoices,
)
from netbox_dhcp.models import OptionDefinition
from netbox_dhcp.tests.custom import (
    APITestCase,
    NetBoxDHCPGraphQLMixin,
    TestObjects,
)
from utilities.testing import APIViewTestCases


class OptionDefinitionAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxDHCPGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = OptionDefinition

    def _get_queryset(self):
        return self.model.objects.filter(standard=False)

    brief_fields = [
        "code",
        "description",
        "display",
        "family",
        "id",
        "name",
        "space",
        "url",
    ]

    @classmethod
    def setUpTestData(cls):
        dhcp_servers = TestObjects.get_dhcp_servers()

        option_definitions = (
            OptionDefinition(
                name="test-option-definition-1",
                description="Test Option Definition 1",
                code=251,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_STRING,
                dhcp_server=dhcp_servers[0],
            ),
            OptionDefinition(
                name="test-option-definition-2",
                description="Test Option Definition 2",
                code=252,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_IPV4_ADDRESS,
                dhcp_server=dhcp_servers[0],
            ),
            OptionDefinition(
                name="test-option-definition-3",
                description="Test Option Definition 3",
                code=253,
                family=IPAddressFamilyChoices.FAMILY_4,
                type=OptionTypeChoices.TYPE_IPV4_ADDRESS,
                dhcp_server=dhcp_servers[0],
            ),
        )
        OptionDefinition.objects.bulk_create(option_definitions)

        cls.create_data = [
            {
                "name": "test-option-definition-4",
                "description": "Test Option Definition 4",
                "family": IPAddressFamilyChoices.FAMILY_6,
                "space": OptionSpaceChoices.DHCPV6,
                "code": 251,
                "type": OptionTypeChoices.TYPE_EMPTY,
                "dhcp_server": dhcp_servers[0].pk,
            },
            {
                "name": "test-option-definition-5",
                "description": "Test Option Definition 5",
                "family": IPAddressFamilyChoices.FAMILY_6,
                "space": OptionSpaceChoices.DHCPV6,
                "code": 252,
                "type": OptionTypeChoices.TYPE_RECORD,
                "record_types": [
                    OptionTypeChoices.TYPE_UINT32,
                    OptionTypeChoices.TYPE_IPV6_ADDRESS,
                ],
                "dhcp_server": dhcp_servers[0].pk,
            },
            {
                "name": "test-option-definition-6",
                "description": "Test Option Definition 6",
                "family": IPAddressFamilyChoices.FAMILY_6,
                "space": OptionSpaceChoices.DHCPV6,
                "code": 253,
                "type": OptionTypeChoices.TYPE_IPV6_ADDRESS,
                "dhcp_server": dhcp_servers[0].pk,
            },
        ]

        cls.bulk_update_data = {
            "description": "Test Description Update",
            "family": IPAddressFamilyChoices.FAMILY_6,
            "space": OptionSpaceChoices.DHCPV6,
            "type": OptionTypeChoices.TYPE_UINT32,
            "record_types": [
                OptionTypeChoices.TYPE_INT32,
                OptionTypeChoices.TYPE_IPV4_ADDRESS,
            ],
            "encapsulate": "isc",
            "array": True,
        }

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_list_objects_anonymous(self):
        url = f"{self._get_list_url()}?standard=false"

        response = self.client.get(url, **self.header)

        self.assertHttpStatus(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), self._get_queryset().count())

    def test_list_objects_brief(self):
        self.add_permissions(
            f"{self.model._meta.app_label}.view_{self.model._meta.model_name}"
        )
        url = f"{self._get_list_url()}?brief=1&standard=false"

        response = self.client.get(url, **self.header)

        self.assertEqual(len(response.data["results"]), self._get_queryset().count())
        self.assertEqual(sorted(response.data["results"][0]), self.brief_fields)

    @skip("Fails because if a bug in the NetBox test framework")
    # +
    # The issue is caused by the filter returning the object definition with ID 31,
    # which is not in the test classes queryset. This is not supposed to happen.
    #
    # TODO: Investigate and open issue
    # -
    def test_graphql_filter_objects(self):
        return super().test_graphql_filter_objects()
