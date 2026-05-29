from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_dhcp.api.serializers import (
    ClientClassSerializer,
    DHCPClusterSerializer,
    DHCPServerInterfaceSerializer,
    DHCPServerSerializer,
    HostReservationSerializer,
    OptionDefinitionSerializer,
    OptionSerializer,
    PDPoolSerializer,
    PoolSerializer,
    SharedNetworkSerializer,
    SubnetSerializer,
)
from netbox_dhcp.filtersets import (
    ClientClassFilterSet,
    DHCPClusterFilterSet,
    DHCPServerFilterSet,
    DHCPServerInterfaceFilterSet,
    HostReservationFilterSet,
    OptionDefinitionFilterSet,
    OptionFilterSet,
    PDPoolFilterSet,
    PoolFilterSet,
    SharedNetworkFilterSet,
    SubnetFilterSet,
)
from netbox_dhcp.models import (
    ClientClass,
    DHCPCluster,
    DHCPServer,
    DHCPServerInterface,
    HostReservation,
    Option,
    OptionDefinition,
    PDPool,
    Pool,
    SharedNetwork,
    Subnet,
)


class NetBoxDHCPRootView(APIRootView):
    def get_view_name(self):
        return "NetBoxDHCP"


class ClientClassViewSet(NetBoxModelViewSet):
    queryset = ClientClass.objects.all()
    serializer_class = ClientClassSerializer
    filterset_class = ClientClassFilterSet


class DHCPClusterViewSet(NetBoxModelViewSet):
    queryset = DHCPCluster.objects.all()
    serializer_class = DHCPClusterSerializer
    filterset_class = DHCPClusterFilterSet


class DHCPServerViewSet(NetBoxModelViewSet):
    queryset = DHCPServer.objects.all()
    serializer_class = DHCPServerSerializer
    filterset_class = DHCPServerFilterSet


class DHCPServerInterfaceViewSet(NetBoxModelViewSet):
    queryset = DHCPServerInterface.objects.all()
    serializer_class = DHCPServerInterfaceSerializer
    filterset_class = DHCPServerInterfaceFilterSet


class HostReservationViewSet(NetBoxModelViewSet):
    queryset = HostReservation.objects.all()
    serializer_class = HostReservationSerializer
    filterset_class = HostReservationFilterSet


class OptionViewSet(NetBoxModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filterset_class = OptionFilterSet


class OptionDefinitionViewSet(NetBoxModelViewSet):
    queryset = OptionDefinition.objects.all()
    serializer_class = OptionDefinitionSerializer
    filterset_class = OptionDefinitionFilterSet


class PDPoolViewSet(NetBoxModelViewSet):
    queryset = PDPool.objects.all()
    serializer_class = PDPoolSerializer
    filterset_class = PDPoolFilterSet


class PoolViewSet(NetBoxModelViewSet):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer
    filterset_class = PoolFilterSet


class SharedNetworkViewSet(NetBoxModelViewSet):
    queryset = SharedNetwork.objects.all()
    serializer_class = SharedNetworkSerializer
    filterset_class = SharedNetworkFilterSet


class SubnetViewSet(NetBoxModelViewSet):
    queryset = Subnet.objects.all()
    serializer_class = SubnetSerializer
    filterset_class = SubnetFilterSet
