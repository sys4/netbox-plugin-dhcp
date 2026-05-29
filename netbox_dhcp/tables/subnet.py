# import django_tables2 as tables
# from django.utils.translation import gettext_lazy as _

from netbox.tables import PrimaryModelTable
from netbox_dhcp.models import Subnet

from .mixins import (
    ClientClassTableMixin,
    DDNSUpdateTableMixin,
    DHCPServerTableMixin,
    EvaluateClientClassTableMixin,
    LeaseTableMixin,
    NetBoxDHCPTableMixin,
    PrefixTableMixin,
)

__all__ = (
    "SubnetTable",
    "RelatedSubnetTable",
    "ParentSubnetTable",
)


class SubnetTable(
    NetBoxDHCPTableMixin,
    DHCPServerTableMixin,
    PrefixTableMixin,
    ClientClassTableMixin,
    EvaluateClientClassTableMixin,
    DDNSUpdateTableMixin,
    LeaseTableMixin,
    PrimaryModelTable,
):
    class Meta(PrimaryModelTable.Meta):
        model = Subnet

        fields = (
            "name",
            "subnet_id",
            "weight",
            "dhcp_server",
            "shared_network",
            "prefix",
            "description",
            "next_server",
            "server_hostname",
            "boot_file_name",
            "client_classes",
            "evaluate_additional_classes",
            "offer_lifetime",
            "valid_lifetime",
            "min_valid_lifetime",
            "max_valid_lifetime",
            "preferred_lifetime",
            "min_preferred_lifetime",
            "max_preferred_lifetime",
            "renew_timer",
            "rebind_timer",
            "calculate_tee_times",
            "t1_percent",
            "t2_percent",
            "adaptive_lease_time_threshold",
            "match_client_id",
            "reservations_global",
            "reservations_out_of_pool",
            "reservations_in_subnet",
            "cache_threshold",
            "cache_max_age",
            "authoritative",
            "store_extended_info",
            "allocator",
            "pd_allocator",
            "relay",
            "interface_id",
            "rapid_commit",
            "hostname_char_set",
            "hostname_char_replacement",
            "ddns_send_updates",
            "ddns_override_no_update",
            "ddns_override_client_update",
            "ddns_replace_client_name",
            "ddns_generated_prefix",
            "ddns_qualifying_suffix",
            "ddns_update_on_renew",
            "ddns_conflict_resolution_mode",
            "ddns_ttl_percent",
            "ddns_ttl",
            "ddns_ttl_min",
            "ddns_ttl_max",
        )

        default_columns = (
            "name",
            "subnet_id",
            "weight",
            "prefix",
        )


class RelatedSubnetTable(SubnetTable):
    class Meta(SubnetTable.Meta):
        fields = (
            "name",
            "description",
        )

        default_columns = (
            "name",
            "description",
        )

    actions = None


class ParentSubnetTable(SubnetTable):
    class Meta(SubnetTable.Meta):
        pass

    actions = None
