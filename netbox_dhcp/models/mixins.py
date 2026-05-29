from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox_dhcp.choices import (
    AllocatorTypeChoices,
    DDNSConflictResolutionModeChoices,
    DDNSReplaceClientNameChoices,
    PDAllocatorTypeChoices,
)

__all__ = (
    "NetBoxDHCPModelMixin",
    "BOOTPModelMixin",
    "ClientClassModelMixin",
    "EvaluateClientClassModelMixin",
    "LifetimeModelMixin",
    "OfferLifetimeModelMixin",
    "DDNSUpdateModelMixin",
    "LeaseModelMixin",
    "NetworkModelMixin",
)


class NetBoxDHCPModelMixin(models.Model):
    FIELDS = [
        "name",
        "description",
    ]

    class Meta:
        abstract = True

    name = models.CharField(
        verbose_name=_("Name"),
        unique=True,
        max_length=255,
        db_collation="natural_sort",
    )

    def __str__(self):
        return str(self.name)


class BOOTPModelMixin(models.Model):
    FIELDS = [
        "next_server",
        "server_hostname",
        "boot_file_name",
    ]

    class Meta:
        abstract = True

    next_server = models.CharField(
        verbose_name=_("Next Server"),
        blank=True,
        null=True,
        max_length=15,
    )
    server_hostname = models.CharField(
        verbose_name=_("Server Hostname"),
        blank=True,
        null=True,
        max_length=64,
    )
    boot_file_name = models.CharField(
        verbose_name=_("Boot File Name"),
        blank=True,
        null=True,
        max_length=128,
    )


class ClientClassModelMixin(models.Model):
    class Meta:
        abstract = True

    client_classes = models.ManyToManyField(
        verbose_name=_("Client Classes"),
        to="ClientClass",
        related_name="%(class)s_set",
        blank=True,
    )


class EvaluateClientClassModelMixin(models.Model):
    class Meta:
        abstract = True

    evaluate_additional_classes = models.ManyToManyField(
        verbose_name=_("Evaluate Additional Classes"),
        to="ClientClass",
        related_name="evaluate_%(class)s_set",
        blank=True,
    )


class ValidLifetimeModelMixin(models.Model):
    class Meta:
        abstract = True

    valid_lifetime = models.PositiveIntegerField(
        verbose_name=_("Valid Lifetime"),
        null=True,
        blank=True,
    )
    min_valid_lifetime = models.PositiveIntegerField(
        verbose_name=_("Minimum Valid Lifetime"),
        null=True,
        blank=True,
    )
    max_valid_lifetime = models.PositiveIntegerField(
        verbose_name=_("Maximum Valid Lifetime"),
        null=True,
        blank=True,
    )


class PreferredLifetimeModelMixin(models.Model):
    class Meta:
        abstract = True

    preferred_lifetime = models.PositiveIntegerField(
        verbose_name=_("Preferred Lifetime"),
        null=True,
        blank=True,
    )
    min_preferred_lifetime = models.PositiveIntegerField(
        verbose_name=_("Minimum Preferred Lifetime"),
        null=True,
        blank=True,
    )
    max_preferred_lifetime = models.PositiveIntegerField(
        verbose_name=_("Maximum Preferred Lifetime"),
        null=True,
        blank=True,
    )


class OfferLifetimeModelMixin(models.Model):
    class Meta:
        abstract = True

    offer_lifetime = models.PositiveIntegerField(
        verbose_name=_("Offer Lifetime"),
        null=True,
        blank=True,
    )


class LifetimeModelMixin(
    ValidLifetimeModelMixin,
    PreferredLifetimeModelMixin,
    OfferLifetimeModelMixin,
):
    class Meta:
        abstract = True


class DDNSUpdateModelMixin(models.Model):
    class Meta:
        abstract = True

    ddns_send_updates = models.BooleanField(
        verbose_name=_("Send DDNS updates"),
        null=True,
        blank=True,
    )
    ddns_override_no_update = models.BooleanField(
        verbose_name=_("Override client 'no update' flag"),
        null=True,
        blank=True,
    )
    ddns_override_client_update = models.BooleanField(
        verbose_name=_("Override client delegation flags"),
        null=True,
        blank=True,
    )
    ddns_replace_client_name = models.CharField(
        verbose_name=_("Replace client name"),
        choices=DDNSReplaceClientNameChoices,
        blank=True,
        null=True,
    )
    ddns_generated_prefix = models.CharField(
        verbose_name=_("Generated Prefix"),
        blank=True,
        null=True,
    )
    ddns_qualifying_suffix = models.CharField(
        verbose_name=_("Qualifying Suffix"),
        blank=True,
        null=True,
    )
    ddns_update_on_renew = models.BooleanField(
        verbose_name=_("Update DDNS on renew"),
        null=True,
        blank=True,
    )
    ddns_conflict_resolution_mode = models.CharField(
        verbose_name=_("Conflict Resolution Mode"),
        choices=DDNSConflictResolutionModeChoices,
        blank=True,
        null=True,
    )
    ddns_ttl_percent = models.DecimalField(
        verbose_name=_("TTL Percent"),
        max_digits=4,
        decimal_places=3,
        null=True,
        blank=True,
    )
    ddns_ttl = models.PositiveIntegerField(
        verbose_name=_("TTL"),
        null=True,
        blank=True,
    )
    ddns_ttl_min = models.PositiveIntegerField(
        verbose_name=_("Minimum TTL"),
        null=True,
        blank=True,
    )
    ddns_ttl_max = models.PositiveIntegerField(
        verbose_name=_("Maximum TTL"),
        null=True,
        blank=True,
    )
    hostname_char_set = models.CharField(
        verbose_name=_("Allowed Characters in Host Names"),
        max_length=255,
        blank=True,
    )
    hostname_char_replacement = models.CharField(
        verbose_name=_("Replacement Character for Invalid Host Names"),
        max_length=255,
        blank=True,
    )

    def get_ddns_replace_client_name_color(self):
        return DDNSReplaceClientNameChoices.colors.get(self.ddns_replace_client_name)

    def get_ddns_conflict_resolution_mode_color(self):
        return DDNSConflictResolutionModeChoices.colors.get(
            self.ddns_conflict_resolution_mode
        )


class LeaseModelMixin(models.Model):
    class Meta:
        abstract = True

    renew_timer = models.PositiveIntegerField(
        verbose_name=_("Renew Timer"),
        null=True,
        blank=True,
    )
    rebind_timer = models.PositiveIntegerField(
        verbose_name=_("Rebind Timer"),
        null=True,
        blank=True,
    )
    match_client_id = models.BooleanField(
        verbose_name=_("Match Client ID"),
        null=True,
        blank=True,
    )
    authoritative = models.BooleanField(
        verbose_name=_("Authoritative"),
        null=True,
        blank=True,
    )
    reservations_global = models.BooleanField(
        verbose_name=_("Global reservations"),
        null=True,
        blank=True,
    )
    reservations_out_of_pool = models.BooleanField(
        verbose_name=_("Out-of-pool reservations"),
        null=True,
        blank=True,
    )
    reservations_in_subnet = models.BooleanField(
        verbose_name=_("In-subnet reservations"),
        null=True,
        blank=True,
    )
    calculate_tee_times = models.BooleanField(
        verbose_name=_("Calculate T times"),
        null=True,
        blank=True,
    )
    t1_percent = models.DecimalField(
        verbose_name=_("T1 Percent"),
        max_digits=4,
        decimal_places=3,
        null=True,
        blank=True,
    )
    t2_percent = models.DecimalField(
        verbose_name=_("T2 Percent"),
        max_digits=4,
        decimal_places=3,
        null=True,
        blank=True,
    )
    cache_threshold = models.DecimalField(
        verbose_name=_("Cache Threshold"),
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    cache_max_age = models.PositiveIntegerField(
        verbose_name=_("Maximum Cache Age"),
        null=True,
        blank=True,
    )
    adaptive_lease_time_threshold = models.DecimalField(
        verbose_name=_("Adaptive Lease Time Threshold"),
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )
    store_extended_info = models.BooleanField(
        verbose_name=_("Store Extended Info"),
        null=True,
        blank=True,
    )
    allocator = models.CharField(
        verbose_name=_("Allocator"),
        choices=AllocatorTypeChoices,
        blank=True,
        null=True,
    )
    pd_allocator = models.CharField(
        verbose_name=_("Prefix Delegation Allocator"),
        choices=PDAllocatorTypeChoices,
        blank=True,
        null=True,
    )

    def get_allocator_color(self):
        return AllocatorTypeChoices.colors.get(self.allocator)

    def get_pd_allocator_color(self):
        return PDAllocatorTypeChoices.colors.get(self.pd_allocator)


class NetworkModelMixin(models.Model):
    class Meta:
        abstract = True

    server_interfaces = models.ManyToManyField(
        verbose_name=_("Server Interfaces"),
        to="DHCPServerInterface",
        blank=True,
    )
    relay = models.CharField(
        verbose_name=_("Relay IP Addresses"),
        max_length=255,
        blank=True,
        null=True,
    )
    interface_id = models.CharField(
        verbose_name=_("Interface ID"),
        max_length=255,
        blank=True,
        null=True,
    )
    rapid_commit = models.BooleanField(
        verbose_name=_("Rapid Commit"),
        null=True,
        blank=True,
    )
