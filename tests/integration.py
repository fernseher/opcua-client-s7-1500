import asyncio
from asyncua import Client, ua
from opcua_client import OPCUAClient


async def main():
    url = "$URL"
    user = '$USER'
    password = '$PASSWORD'
    asyncua_client = Client(url)
    opcua_client = await OPCUAClient.create(asyncua_client, user, password)

    # Read value
    node_id = '$NODE_ID_1'
    dvs_status = await opcua_client.read(node_id)
    print(dvs_status)

    # Write value
    speed_variable_id = '$NODE_ID_2'
    speed = 16
    await opcua_client.write(speed_variable_id, speed)

    # Call Method
    node_id = '$NODE_ID_3'
    target = ua.tfPose(0.1337, 0.1337, 0, 0, 0, 0)   # type: ignore
    tcp = ua.tfPose(0.1337, 0.1337, 0, 0, 0, 0)   # type: ignore
    speed = ua.Variant(0.01, ua.VariantType.Float)
    acceleration = ua.Variant(0.1, ua.VariantType.Float)
    res = await opcua_client.call_method(
        node_id,
        target,
        speed,
        acceleration,
        tcp
    )
    print(res)

if __name__ == '__main__':
    asyncio.run(main())
