import logging
from asyncua import Client, ua


logger = logging.getLogger(__name__)


class OPCUAClient:
    client: Client

    @classmethod
    async def create(
        cls,
        asyncua_client: Client,
        user: str,
        password: str
    ):
        """Creates OPCUAClient instance, connects to the PLC
        and loads its ExtensionObjects"""
        self = OPCUAClient()
        self.client = asyncua_client
        self.client.set_user(user)
        self.client.set_password(password)
        await self.client.connect()
        await self.client.load_type_definitions()
        return self

    async def read(self, variable_id: str) -> int | float | str:
        """Returns value of specified PLC variable """
        var = self.client.get_node(variable_id)
        value = await var.read_value()
        return value

    async def write(
            self,
            variable_id: str,
            value: int | float | str,
    ) -> None:
        """Writes value to specified PLC variable"""
        var = self.client.get_node(variable_id)
        data_type = await var.read_data_type_as_variant_type()
        try:
            # Send only data value without timestamps etc.
            # because S7-1500 does not accept otherwise
            await var.set_value(ua.DataValue(ua.Variant(value, data_type)))
        except ua.UaError:
            logger.exception(f"Node with ID: {variable_id} does not exist")
            return

    async def call_method(self, node_id, *args):
        """Calls a method at the PLC and returns its response"""
        node = self.client.get_node(node_id)
        res = await node.call_method('Method', *args)
        logger.info(f"Calling ServerMethod returned {res}")
        return res
