from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from netbox_dhcp.models import DHCPServer, DHCPServerInterface


@receiver(m2m_changed, sender=DHCPServer.device_interfaces.through)
def device_interfaces_changed(action, instance, pk_set, **kwargs):
    if action in ("post_clear", "post_remove"):
        for interface in instance.interfaces.filter(device_interface__pk__in=pk_set):
            interface.delete()

    if action == "post_add":
        for pk in pk_set:
            interface = DHCPServerInterface.objects.create(
                dhcp_server=instance,
                device_interface=instance.device_interfaces.get(pk=pk),
            )
            instance.interfaces.add(interface)


@receiver(m2m_changed, sender=DHCPServer.virtual_machine_interfaces.through)
def virtual_machine_interfaces_changed(action, instance, pk_set, **kwargs):
    if action in ("post_clear", "post_remove"):
        for interface in instance.interfaces.filter(
            virtual_machine_interface__pk__in=pk_set
        ):
            interface.delete()

    if action == "post_add":
        for pk in pk_set:
            interface = DHCPServerInterface.objects.create(
                dhcp_server=instance,
                virtual_machine_interface=instance.virtual_machine_interfaces.get(
                    pk=pk
                ),
            )
            instance.interfaces.add(interface)
