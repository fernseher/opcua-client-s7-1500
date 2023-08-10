from dataclasses import dataclass
import logging
from asyncua import Client, ua


logger = logging.getLogger(__name__)


@dataclass
class OPCUAVariable:
    node_id: str
    type: str


class OPCUAClient:
    client: Client
    ua_types = {
        'float': ua.VariantType.Float,
        'int32': ua.VariantType.UInt32,
        'str': ua.VariantType.String,
        'byte': ua.VariantType.Byte,
    }

    @classmethod
    async def create(
        cls,
        asyncua_client: Client,
        user: str,
        password: str
    ):
        self = OPCUAClient()
        try:
            self.client = asyncua_client
            self.client.set_user(user)
            self.client.set_password(password)
            # client.set_security_string()
            await self.client.connect()
        except Exception:
            raise  # TODO
        return self

    async def read(self, variable_id: str) -> int | float | str:
        var = self.client.get_node(variable_id)
        value = await var.read_value()
        return value

    async def write(
            self,
            opcua_var: OPCUAVariable,
            value: int | float | str,
    ) -> None:
        var = self.client.get_node(opcua_var.node_id)
        ua_type = self.ua_types[opcua_var.type]
        try:
            # Send only data value without timestamps etc. because PLC does not accept otherwise
            await var.set_value(ua.DataValue(ua.Variant(value, ua_type)))
        except ua.UaError:
            logger.exception(f"Node with ID: {opcua_var.node_id} does not exist")
            return

    # # TODO: Calling a method
    # res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)
    # print(f"Calling ServerMethod returned {res}")
