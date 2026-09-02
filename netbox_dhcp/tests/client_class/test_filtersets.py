from django.test import TestCase

from netbox_dhcp.filtersets import ClientClassFilterSet
from netbox_dhcp.models import ClientClass
from netbox_dhcp.tests.custom import (
    BOOTPFilterSetTestMixin,
    OfferLifetimeFilterSetTestMixin,
    OptionFilterSetTestMixin,
    PreferredLifetimeFilterSetTestMixin,
    TestObjects,
    ValidLifetimeFilterSetTestMixin,
)
from utilities.testing import ChangeLoggedFilterSetTestMixin


class ClientClassFilterSetTestCase(
    TestCase,
    ChangeLoggedFilterSetTestMixin,
    BOOTPFilterSetTestMixin,
    ValidLifetimeFilterSetTestMixin,
    OfferLifetimeFilterSetTestMixin,
    PreferredLifetimeFilterSetTestMixin,
    OptionFilterSetTestMixin,
):
    queryset = ClientClass.objects.all()
    filterset = ClientClassFilterSet

    ignore_fields = (
        "option_set",
        "hostreservation_set",
        "dhcpserver_set",
        "pdpool_set",
        "evaluate_pdpool_set",
        "pool_set",
        "evaluate_pool_set",
        "sharednetwork_set",
        "evaluate_sharednetwork_set",
        "subnet_set",
        "evaluate_subnet_set",
    )

    @classmethod
    def setUpTestData(cls):
        cls.dhcp_servers = TestObjects.get_dhcp_servers()

        cls.client_classes = (
            ClientClass(
                name="test-client-class-1",
                description="Test Client Class 1",
                weight=90,
                dhcp_server=cls.dhcp_servers[0],
                test="substring(option[61].hex,0,3) == 'foo'",
                template_test="substring(option[23].hex,0,3)",
                only_in_additional_list=False,
                **BOOTPFilterSetTestMixin.DATA[0],
                **ValidLifetimeFilterSetTestMixin.DATA[0],
                **PreferredLifetimeFilterSetTestMixin.DATA[0],
                **OfferLifetimeFilterSetTestMixin.DATA[0],
            ),
            ClientClass(
                name="test-client-class-2",
                description="Test Client Class 2",
                weight=100,
                dhcp_server=cls.dhcp_servers[0],
                test="substring(option[61].hex,0,3) == 'bar'",
                template_test="substring(option[42].hex,0,3)",
                only_in_additional_list=True,
                **BOOTPFilterSetTestMixin.DATA[1],
                **ValidLifetimeFilterSetTestMixin.DATA[1],
                **PreferredLifetimeFilterSetTestMixin.DATA[1],
                **OfferLifetimeFilterSetTestMixin.DATA[1],
            ),
            ClientClass(
                name="test-client-class-3",
                description="Test Client Class 3",
                weight=110,
                dhcp_server=cls.dhcp_servers[1],
                test="substring(option[61].hex,0,3) == 'baz'",
                template_test="substring(option[66].hex,0,3)",
                only_in_additional_list=True,
                **BOOTPFilterSetTestMixin.DATA[2],
                **ValidLifetimeFilterSetTestMixin.DATA[2],
                **PreferredLifetimeFilterSetTestMixin.DATA[2],
                **OfferLifetimeFilterSetTestMixin.DATA[2],
            ),
        )
        ClientClass.objects.bulk_create(cls.client_classes)

        cls.add_test_options(cls.client_classes)

    def test_name(self):
        params = {"name": ["test-client-class-1", "test-client-class-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["test-client-class-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_description(self):
        params = {"description": ["Test Client Class 1", "Test Client Class 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"description": ["Test Client Class 3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_test(self):
        params = {"test__iregex": r"== '(foo|bar)'"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"test": "substring(option[61].hex,0,3) == 'baz'"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_template_test(self):
        params = {"template_test__iregex": r"\[(23|42)\]"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"template_test": "substring(option[66].hex,0,3)"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_only_in_additional_list(self):
        params = {"only_in_additional_list": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"only_in_additional_list": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_weight(self):
        params = {"weight": [100]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"weight": [90]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_dhcp_servers(self):
        params = {"dhcp_server_id": [self.dhcp_servers[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"dhcp_server": [self.dhcp_servers[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
