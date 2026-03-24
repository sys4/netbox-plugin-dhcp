from netbox_dhcp.models import Option, OptionDefinition
from netbox_dhcp.choices import (
    OptionSpaceChoices,
    AllocatorTypeChoices,
    PDAllocatorTypeChoices,
    DDNSReplaceClientNameChoices,
    DDNSConflictResolutionModeChoices,
)

__all__ = (
    "BOOTPFilterSetTests",
    "ValidLifetimeFilterSetTests",
    "PreferredLifetimeFilterSetTests",
    "OfferLifetimeFilterSetTests",
    "LeaseFilterSetTests",
    "DDNSUpdateFilterSetTests",
    "OptionFilterSetTests",
)


class BOOTPFilterSetTests:
    DATA = [
        {
            "next_server": "10.0.0.1",
            "server_hostname": "server1.test.example.com",
            "boot_file_name": "/tftpboot/file-1.img",
        },
        {
            "next_server": "10.0.0.2",
            "server_hostname": "server2.test.example.com",
            "boot_file_name": "/tftpboot/file-2.img",
        },
        {
            "next_server": "10.0.0.3",
            "server_hostname": "server3.test.example.com",
            "boot_file_name": "/tftpboot/file-3.img",
        },
    ]

    def test_next_server(self):
        params = {"next_server": ["10.0.0.1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"next_server": ["10.0.0.1", "10.0.0.2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_server_hostname(self):
        params = {"server_hostname": ["server1.test.example.com"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_boot_file_name(self):
        params = {"boot_file_name": ["/tftpboot/file-2.img"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"boot_file_name": ["/tftpboot/file-2.img", "/tftpboot/file-3.img"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class ValidLifetimeFilterSetTests:
    DATA = [
        {
            "valid_lifetime": 86400,
            "min_valid_lifetime": 43200,
            "max_valid_lifetime": 172400,
        },
        {
            "valid_lifetime": 86401,
            "min_valid_lifetime": 43201,
            "max_valid_lifetime": 172401,
        },
        {
            "valid_lifetime": 86402,
            "min_valid_lifetime": 43202,
            "max_valid_lifetime": 172402,
        },
    ]

    def test_valid_lifetime(self):
        params = {"valid_lifetime": [86400]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"valid_lifetime": [86401, 86402]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_min_valid_lifetime(self):
        params = {"min_valid_lifetime": [43200]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"min_valid_lifetime": [43200, 43201]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_max_valid_lifetime(self):
        params = {"max_valid_lifetime": [172400]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"max_valid_lifetime": [172401, 172402]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class PreferredLifetimeFilterSetTests:
    DATA = [
        {
            "preferred_lifetime": 86400,
            "min_preferred_lifetime": 43200,
            "max_preferred_lifetime": 172400,
        },
        {
            "preferred_lifetime": 86401,
            "min_preferred_lifetime": 43201,
            "max_preferred_lifetime": 172401,
        },
        {
            "preferred_lifetime": 86402,
            "min_preferred_lifetime": 43202,
            "max_preferred_lifetime": 172402,
        },
    ]

    def test_preferred_lifetime(self):
        params = {"preferred_lifetime": [86400]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"preferred_lifetime": [86401, 86402]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_min_preferred_lifetime(self):
        params = {"min_preferred_lifetime": [43200]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"min_preferred_lifetime": [43201, 43202]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_max_preferred_lifetime(self):
        params = {"max_preferred_lifetime": [172402]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"max_preferred_lifetime": [172400, 172401]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class OfferLifetimeFilterSetTests:
    DATA = [
        {
            "offer_lifetime": 86400,
        },
        {
            "offer_lifetime": 86401,
        },
        {
            "offer_lifetime": 86402,
        },
    ]

    def test_offer_lifetime(self):
        params = {"offer_lifetime": [86400]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"offer_lifetime": [86401, 86402]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class LeaseFilterSetTests:
    DATA = [
        {
            "renew_timer": 43200,
            "rebind_timer": 86400,
            "match_client_id": False,
            "authoritative": False,
            "reservations_global": False,
            "reservations_out_of_pool": False,
            "reservations_in_subnet": False,
            "calculate_tee_times": False,
            "t1_percent": "0.4",
            "t2_percent": "0.5",
            "cache_threshold": "0.7",
            "cache_max_age": 3600,
            "adaptive_lease_time_threshold": "0.5",
            "store_extended_info": False,
            "allocator": AllocatorTypeChoices.ITERATIVE,
            "pd_allocator": PDAllocatorTypeChoices.ITERATIVE,
        },
        {
            "renew_timer": 43201,
            "rebind_timer": 86401,
            "match_client_id": False,
            "authoritative": False,
            "reservations_global": False,
            "reservations_out_of_pool": False,
            "reservations_in_subnet": False,
            "calculate_tee_times": False,
            "t1_percent": "0.5",
            "t2_percent": "0.6",
            "cache_threshold": "0.8",
            "cache_max_age": 3601,
            "adaptive_lease_time_threshold": "0.6",
            "store_extended_info": False,
            "allocator": AllocatorTypeChoices.RANDOM,
            "pd_allocator": PDAllocatorTypeChoices.RANDOM,
        },
        {
            "renew_timer": 43202,
            "rebind_timer": 86402,
            "match_client_id": True,
            "authoritative": True,
            "reservations_global": True,
            "reservations_out_of_pool": True,
            "reservations_in_subnet": True,
            "calculate_tee_times": True,
            "t1_percent": "0.6",
            "t2_percent": "0.7",
            "cache_threshold": "0.9",
            "cache_max_age": 3602,
            "adaptive_lease_time_threshold": "0.7",
            "store_extended_info": True,
            "allocator": AllocatorTypeChoices.ITERATIVE,
            "pd_allocator": PDAllocatorTypeChoices.FREE_LEASE_QUEUE,
        },
    ]

    def test_renew_timer(self):
        params = {"renew_timer": [43200]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"renew_timer": [43201, 43202]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_rebind_timer(self):
        params = {"rebind_timer": [86400]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"rebind_timer": [86401, 86402]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_match_client_id(self):
        params = {"match_client_id": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"match_client_id": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_authoritative(self):
        params = {"authoritative": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"authoritative": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_reservations_global(self):
        params = {"reservations_global": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"reservations_global": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_reservations_out_of_pool(self):
        params = {"reservations_out_of_pool": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"reservations_out_of_pool": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_reservations_in_subnet(self):
        params = {"reservations_in_subnet": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"reservations_in_subnet": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_calculate_tee_times(self):
        params = {"calculate_tee_times": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"calculate_tee_times": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_t1_percent(self):
        params = {"t1_percent": [0.4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"t1_percent": [0.5, 0.6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_t2_percent(self):
        params = {"t2_percent": [0.5]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"t2_percent": [0.6, 0.7]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_cache_threshold(self):
        params = {"cache_threshold": [0.7]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"cache_threshold": [0.8, 0.9]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_cache_max_age(self):
        params = {"cache_max_age": [3600]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"cache_max_age": [3600, 3601]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_adaptive_lease_time_threshold(self):
        params = {"adaptive_lease_time_threshold": [0.5]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"adaptive_lease_time_threshold": [0.5, 0.6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_store_extended_info(self):
        params = {"store_extended_info": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"store_extended_info": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_allocator(self):
        params = {"allocator": [AllocatorTypeChoices.ITERATIVE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"allocator": [AllocatorTypeChoices.RANDOM]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_pd_allocator(self):
        params = {
            "pd_allocator": [
                PDAllocatorTypeChoices.ITERATIVE,
                PDAllocatorTypeChoices.RANDOM,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"pd_allocator": [PDAllocatorTypeChoices.FREE_LEASE_QUEUE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class DDNSUpdateFilterSetTests:
    DATA = [
        {
            "hostname_char_set": r"[a-z0-9_-]",
            "hostname_char_replacement": "invalid",
            "ddns_send_updates": True,
            "ddns_override_no_update": True,
            "ddns_override_client_update": True,
            "ddns_replace_client_name": DDNSReplaceClientNameChoices.NEVER,
            "ddns_generated_prefix": "server",
            "ddns_qualifying_suffix": "zone1.example.com",
            "ddns_update_on_renew": True,
            "ddns_conflict_resolution_mode": DDNSConflictResolutionModeChoices.CHECK_WITH_DHCID,
            "ddns_ttl_percent": "0.5",
            "ddns_ttl": 86400,
            "ddns_ttl_min": 43200,
            "ddns_ttl_max": 172800,
        },
        {
            "hostname_char_set": r"[a-z0-9_]",
            "hostname_char_replacement": "invalid",
            "ddns_send_updates": True,
            "ddns_override_no_update": True,
            "ddns_override_client_update": True,
            "ddns_replace_client_name": DDNSReplaceClientNameChoices.ALWAYS,
            "ddns_generated_prefix": "client",
            "ddns_qualifying_suffix": "zone2.example.com",
            "ddns_update_on_renew": True,
            "ddns_conflict_resolution_mode": DDNSConflictResolutionModeChoices.NO_CHECK_WITH_DHCID,
            "ddns_ttl_percent": "0.6",
            "ddns_ttl": 86401,
            "ddns_ttl_min": 43201,
            "ddns_ttl_max": 172801,
        },
        {
            "hostname_char_set": r"[a-z0-9-]",
            "hostname_char_replacement": "replaced",
            "ddns_send_updates": False,
            "ddns_override_no_update": False,
            "ddns_override_client_update": False,
            "ddns_replace_client_name": DDNSReplaceClientNameChoices.WHEN_PRESENT,
            "ddns_generated_prefix": "server",
            "ddns_qualifying_suffix": "zone3.example.com",
            "ddns_update_on_renew": False,
            "ddns_conflict_resolution_mode": DDNSConflictResolutionModeChoices.CHECK_EXISTS_WITH_DHCID,
            "ddns_ttl_percent": "0.7",
            "ddns_ttl": 86402,
            "ddns_ttl_min": 43202,
            "ddns_ttl_max": 172802,
        },
    ]

    def test_hostname_char_set(self):
        params = {"hostname_char_set": [r"[a-z0-9_-]", r"[a-z0-9-]"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"hostname_char_set": [r"[a-z0-9_-]"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_hostname_char_replacement(self):
        params = {"hostname_char_replacement": ["invalid"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"hostname_char_replacement": ["replaced"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ddns_send_updates(self):
        params = {"ddns_send_updates": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_send_updates": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_override_no_update(self):
        params = {"ddns_override_no_update": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_override_no_update": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_override_client_update(self):
        params = {"ddns_override_client_update": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_override_client_update": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_replace_client_name(self):
        params = {
            "ddns_replace_client_name": [
                DDNSReplaceClientNameChoices.NEVER,
                DDNSReplaceClientNameChoices.ALWAYS,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "ddns_replace_client_name": [DDNSReplaceClientNameChoices.WHEN_PRESENT]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ddns_generated_prefix(self):
        params = {"ddns_generated_prefix": ["server"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"ddns_generated_prefix": ["client"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ddns_qualifying_suffix(self):
        params = {"ddns_qualifying_suffix": ["zone1.example.com"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "ddns_qualifying_suffix__iregex": ["zone1.example.com", "zone2.example.com"]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_update_on_renew(self):
        params = {"ddns_update_on_renew": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_update_on_renew": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_conflict_resolution_mode(self):
        params = {
            "ddns_conflict_resolution_mode": [
                DDNSConflictResolutionModeChoices.CHECK_WITH_DHCID,
                DDNSConflictResolutionModeChoices.NO_CHECK_WITH_DHCID,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "ddns_conflict_resolution_mode": [
                DDNSConflictResolutionModeChoices.CHECK_EXISTS_WITH_DHCID
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ddns_ttl_percent(self):
        params = {"ddns_ttl_percent": [0.5]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_ttl_percent": [0.5, 0.6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_ttl(self):
        params = {"ddns_ttl": [86400]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_ttl": [86401, 86402]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_ttl_min(self):
        params = {"ddns_ttl_min": [43200]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_ttl_min": [43201, 43202]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_ddns_ttl_max(self):
        params = {"ddns_ttl_max": [172800]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ddns_ttl_max": [172800, 172801]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class OptionFilterSetTests:
    @classmethod
    def add_test_options(cls, test_objects):
        option_definitions = (
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV4,
                name="routers",  # code 3
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV4,
                name="domain-name-servers",  # code 6
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV4,
                name="interface-mtu",  # code 26
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV6,
                name="dns-servers",  # code 23
            ),
            OptionDefinition.objects.get(
                space=OptionSpaceChoices.DHCPV6,
                name="domain-search",  # code 24
            ),
        )

        options = (
            Option(
                definition=option_definitions[0],
                data="192.0.2.1,192.0.2.2",
                assigned_object=test_objects[0],
            ),
            Option(
                definition=option_definitions[0],
                data="192.0.2.3,192.0.2.4",
                assigned_object=test_objects[1],
            ),
            Option(
                definition=option_definitions[1],
                data="192.0.2.5,192.0.2.6",
                assigned_object=test_objects[0],
            ),
            Option(
                definition=option_definitions[2],
                data="1380",
                assigned_object=test_objects[1],
            ),
            Option(
                definition=option_definitions[3],
                data="2001:db8:1::53,2001:db8:2::53",
                assigned_object=test_objects[2],
            ),
            Option(
                definition=option_definitions[4],
                data="example.com",
                assigned_object=test_objects[2],
            ),
        )
        Option.objects.bulk_create(options)

    def test_option_name(self):
        params = {"option_name": ["routers"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"option_name": ["dns-servers", "domain-search"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_option_code(self):
        params = {"option_code": [3]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"option_code": [23, 24]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_option_space(self):
        params = {"option_space": [OptionSpaceChoices.DHCPV4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"option_space": [OptionSpaceChoices.DHCPV6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
