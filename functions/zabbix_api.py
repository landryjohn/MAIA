from decouple import config
from pyzabbix import ZabbixAPI

ZABBIX_SERVER = config('ZABBIX_SERVER')
# AUTH_TOKEN = None
zapi = ZabbixAPI(ZABBIX_SERVER)

# Authencication 
zapi.login('Admin', 'zabbix')



# DRAFT :)

# def get_payload(method:str, params:dict, auth:str=None) -> dict :
#     return {  
#         "jsonrpc": "2.0",
#         "method": method,
#         "params": params,
#         "id": 1,
#         "auth": auth
#     }

# def login() -> None : 
    # params = {
    #     'user': 'Admin',
    #     'password': 'zabbix'
    # }
    # resp = requests.post(
    #     url = f'{ZABBIX_SERVER}/api_jsonrpc.php',
    #     headers={'Content-Type': 'application/json-rpc'},
    #     data=get_payload('user.login', params)
    # )
    # return resp 



