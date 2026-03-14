from django.urls import reverse
from django.test import SimpleTestCase

from netbox_dhcp import __version__
from utilities.testing.api import APITestCase


class NetBoxDHCPVersionTestCase(SimpleTestCase):
    def test_version(self):
        assert __version__ == "0.1.5"


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_dhcp-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, 200)
