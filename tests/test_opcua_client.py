from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock
from opcua_client.opcua_client import OPCUAClient, OPCUAVariable
from asyncua import ua


class TestOPCUAClient(IsolatedAsyncioTestCase):
    def setUp(self):
        self.asyncua_client = AsyncMock()
        self.mock_value = 1337
        self.var = MagicMock()
        self.var.read_value = AsyncMock(return_value=self.mock_value)
        self.var.set_value = AsyncMock()
        self.asyncua_client.get_node = MagicMock(return_value=self.var)

    async def test_create(self):
        client = await OPCUAClient.create(self.asyncua_client, '', '')
        self.asyncua_client.set_user.assert_called()
        self.asyncua_client.set_password.assert_called()
        self.asyncua_client.connect.assert_called()
        self.assertIsInstance(client, OPCUAClient)

    async def test_read(self):
        client = await OPCUAClient.create(self.asyncua_client, '', '')
        value = await client.read('some_id')
        self.asyncua_client.get_node.assert_called_with('some_id')
        self.assertEqual(value, self.mock_value)

    async def test_write(self):
        client = await OPCUAClient.create(self.asyncua_client, '', '')
        params = [
            (OPCUAVariable('some_id', 'float'), 100),
            (OPCUAVariable('some_id', 'int32'), 99),
            (OPCUAVariable('some_id', 'str'), 'test'),
            (OPCUAVariable('some_id', 'byte'), 2),
        ]
        expected_types = [
            ua.VariantType.Float,
            ua.VariantType.UInt32,
            ua.VariantType.String,
            ua.VariantType.Byte,
        ]
        for param, type in zip(params, expected_types):
            await client.write(*param)
            self.asyncua_client.get_node.assert_called_with('some_id')
            self.var.set_value.assert_called_with(
                ua.DataValue(ua.Variant(param[1], type))
            )
