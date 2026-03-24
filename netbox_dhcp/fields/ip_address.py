from django.db.models import Lookup

from ipam.fields import IPAddressField


class NetHostLTE(Lookup):
    lookup_name = "net_host_lte"

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)

        if rhs_params:
            rhs_params[0] = rhs_params[0].split("/")[0]

        params = lhs_params + rhs_params
        return f"CAST(HOST({lhs}) AS INET) <= CAST({rhs} AS INET)", params


class NetHostGTE(Lookup):
    lookup_name = "net_host_gte"

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)

        if rhs_params:
            rhs_params[0] = rhs_params[0].split("/")[0]

        params = lhs_params + rhs_params
        return f"CAST(HOST({lhs}) AS INET) >= CAST({rhs} AS INET)", params


IPAddressField.register_lookup(NetHostLTE)
IPAddressField.register_lookup(NetHostGTE)
