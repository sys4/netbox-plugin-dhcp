from django.urls import include, path

from utilities.urls import get_model_urls

# +
# Import views so the register_model_view is run. This is required for the
# URLs to be set up properly with get_model_urls().
# -
from .views import *  # noqa: F401

app_name = "netbox_dhcp"

urlpatterns = (
    path(
        "clientclasses/",
        include(get_model_urls("netbox_dhcp", "clientclass", detail=False)),
    ),
    path(
        "clientclasses/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "clientclass")),
    ),
    path(
        "ddns/",
        include(get_model_urls("netbox_dhcp", "ddns", detail=False)),
    ),
    path(
        "ddns/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "ddns")),
    ),
    path(
        "hostreservations/",
        include(get_model_urls("netbox_dhcp", "hostreservation", detail=False)),
    ),
    path(
        "hostreservations/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "hostreservation")),
    ),
    path(
        "options/",
        include(get_model_urls("netbox_dhcp", "option", detail=False)),
    ),
    path(
        "options/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "option")),
    ),
    path(
        "optiondefinitions/",
        include(get_model_urls("netbox_dhcp", "optiondefinition", detail=False)),
    ),
    path(
        "optiondefinitions/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "optiondefinition")),
    ),
    path(
        "dhcpclusters/",
        include(get_model_urls("netbox_dhcp", "dhcpcluster", detail=False)),
    ),
    path(
        "dhcpclusters/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "dhcpcluster")),
    ),
    path(
        "dhcpservers/",
        include(get_model_urls("netbox_dhcp", "dhcpserver", detail=False)),
    ),
    path(
        "dhcpservers/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "dhcpserver")),
    ),
    path(
        "dhcpserverinterfaces/",
        include(get_model_urls("netbox_dhcp", "dhcpserverinterface", detail=False)),
    ),
    path(
        "dhcpserverinterfaces/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "dhcpserverinterface")),
    ),
    path(
        "pdpools/",
        include(get_model_urls("netbox_dhcp", "pdpool", detail=False)),
    ),
    path(
        "pdpools/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "pdpool")),
    ),
    path(
        "pools/",
        include(get_model_urls("netbox_dhcp", "pool", detail=False)),
    ),
    path(
        "pools/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "pool")),
    ),
    path(
        "sharednetworks/",
        include(get_model_urls("netbox_dhcp", "sharednetwork", detail=False)),
    ),
    path(
        "sharednetworks/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "sharednetwork")),
    ),
    path(
        "subnets/",
        include(get_model_urls("netbox_dhcp", "subnet", detail=False)),
    ),
    path(
        "subnets/<int:pk>/",
        include(get_model_urls("netbox_dhcp", "subnet")),
    ),
)
