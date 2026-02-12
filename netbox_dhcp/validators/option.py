import re
import netaddr
import json

from django.utils.translation import gettext_lazy as _
from django.core import validators as django_validators
from django.core.exceptions import ValidationError

from netbox_dhcp.choices import OptionTypeChoices

__all__ = ("validate_data",)


def validate_empty(data):
    if data not in (None, ""):
        raise ValidationError(_("{data} is not a valid empty value").format(data=data))


def validate_binary(data):
    if re.search(
        r"^([0-9a-f]{1,2}[: ]){0,254}[0-9a-f]{1,2}$", data, flags=re.IGNORECASE
    ):
        return
    if re.search(r"^(0x)?[0-9a-f]{1,510}$", data, flags=re.IGNORECASE):
        return
    if re.search(r"^'.{0,255}'$", data):
        return

    raise ValidationError(_("{data} is not a valid binary value").format(data=data))


def validate_boolean(data):
    if data.lower() not in ("true", "false"):
        raise ValidationError(
            _("{data} is not a valid boolean value").format(data=data)
        )


def validate_fqdn(data):
    try:
        django_validators.validate_domain_name(data)
    except ValidationError:
        raise ValidationError(_("{data} is not a valid FQDN").format(data=data))


def validate_ipv4_address(data):
    if not netaddr.valid_ipv4(data):
        raise ValidationError(_("{data} is not a valid IPv4 address").format(data=data))


def validate_ipv6_address(data):
    if not netaddr.valid_ipv6(data):
        raise ValidationError(_("{data} is not a valid IPv6 address").format(data=data))


def validate_ipv6_prefix(data):
    if not (split_data := re.match(r"(.*)/(.*)", data)):
        raise ValidationError(_("{data} is not a valid IPv6 prefix").format(data=data))

    address, prefixlen = split_data.groups()
    if (
        not netaddr.valid_ipv6(address)
        or not prefixlen.isnumeric()
        or int(prefixlen) not in range(0, 129)
    ):
        raise ValidationError(_("{data} is not a valid IPv6 prefix").format(data=data))


def validate_psid(data):
    if not (split_data := re.match(r"(.*)/(.*)", data)):
        raise ValidationError(_("{data} is not a valid PSID").format(data=data))

    psid, psid_len = split_data.groups()
    if (
        not psid.isnumeric()
        or int(psid) not in range(0, 17)
        or not psid_len.isnumeric()
        or int(psid_len) not in range(0, 65536)
    ):
        raise ValidationError(_("{data} is not a valid IPv6 prefix").format(data=data))


def validate_string(data):
    if len(data) > 255:
        raise ValidationError(_("{data} is not valid string data").format(data=data))


def validate_tuple(data):
    try:
        json.loads(data)
    except json.JSONDecodeError:
        raise ValidationError(_("{data} is not valid JSON data").format(data=data))


def validate_uint8(data):
    if not data.isnumeric() or int(data) not in range(0, 0x100):
        raise ValidationError(_("{data} is not a valid uint8 value").format(data=data))


def validate_uint16(data):
    if not data.isnumeric() or int(data) not in range(0, 0x10000):
        raise ValidationError(_("{data} is not a valid uint16 value").format(data=data))


def validate_uint32(data):
    if not data.isnumeric() or int(data) not in range(0, 0x100000000):
        raise ValidationError(_("{data} is not a valid uint32 value").format(data=data))


def validate_int8(data):
    if not re.sub(r"^-", "", data).isnumeric() or int(data) not in range(-0x80, 0x80):
        raise ValidationError(_("{data} is not a valid int8 value").format(data=data))


def validate_int16(data):
    if not re.sub(r"^-", "", data).isnumeric() or int(data) not in range(
        -0x8000, 0x8000
    ):
        raise ValidationError(_("{data} is not a valid int16 value").format(data=data))


def validate_int32(data):
    if not re.sub(r"^-", "", data).isnumeric() or int(data) not in range(
        -0x80000000, 0x80000000
    ):
        raise ValidationError(_("{data} is not a valid int32 value").format(data=data))


def validate_data(data, data_type):
    if data_type == OptionTypeChoices.TYPE_RECORD:
        return

    validator_function = {
        OptionTypeChoices.TYPE_EMPTY: validate_empty,
        OptionTypeChoices.TYPE_BINARY: validate_binary,
        OptionTypeChoices.TYPE_BOOLEAN: validate_boolean,
        OptionTypeChoices.TYPE_FQDN: validate_fqdn,
        OptionTypeChoices.TYPE_IPV4_ADDRESS: validate_ipv4_address,
        OptionTypeChoices.TYPE_IPV6_ADDRESS: validate_ipv6_address,
        OptionTypeChoices.TYPE_IPV6_PREFIX: validate_ipv6_prefix,
        OptionTypeChoices.TYPE_PSID: validate_psid,
        OptionTypeChoices.TYPE_STRING: validate_string,
        OptionTypeChoices.TYPE_TUPLE: validate_tuple,
        OptionTypeChoices.TYPE_UINT8: validate_uint8,
        OptionTypeChoices.TYPE_UINT16: validate_uint16,
        OptionTypeChoices.TYPE_UINT32: validate_uint32,
        OptionTypeChoices.TYPE_INT8: validate_int8,
        OptionTypeChoices.TYPE_INT16: validate_int16,
        OptionTypeChoices.TYPE_INT32: validate_int32,
    }

    try:
        validator_function.get(data_type, validate_string)(data)
    except ValidationError as exc:
        raise ValidationError({"data": exc.message})
