# OPCUA Client


## Description
Simple async OPCUA client wrapping the asyncua client to enable communication with our SIMATIC S7-1500 PLC of Wiring Robot


## Usage

```python
from asyncua import Client
from opcua_client import OPCUAClient

url = "opc.tcp://192.168.100.127:4840"
user = 'FAU'
password = '12345678'
asyncua_client = Client(url)
opcua_client = await OPCUAClient.create(asyncua_client, user, password)

# Read value
node_id = 'ns=3;s="DB_DVSData"."CD"."CyclicInputDataLE"."DVS_Status"'
dvs_status = await opcua_client.read(node_id)

# Write value
speed_id = 'ns=3;s="DB_DVSData"."CD"."CyclicOutputDataBE"."Feed Speed"'
speed = 10
await opcua_client.write(speed_var, speed)
```
