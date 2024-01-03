# OPCUA Client


## Description
Simple async OPCUA client wrapping the asyncua client to enable communication with SIMATIC S7-1500 PLC


## Usage Example

```python
from asyncua import Client
from opcua_client import OPCUAClient

url = "opc.tcp://$IP:4840"
user = '$USER'
password = '$PASSWORD'
asyncua_client = Client(url)
opcua_client = await OPCUAClient.create(asyncua_client, user, password)

# Read value
node_id = 'ns=3;s="DB_Motor"."CyclicInputData"."Status"'
dvs_status = await opcua_client.read(node_id)

# Write value
node_id = 'ns=3;s="DB_Motor"."CyclicOutputData"."Speed"'
speed = 10
await opcua_client.write(speed_var, speed)
```
