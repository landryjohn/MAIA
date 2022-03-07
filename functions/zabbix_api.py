from decouple import config
from pyzabbix import ZabbixAPI
import termcolor, datetime 

ZABBIX_SERVER = config('ZABBIX_SERVER')
# AUTH_TOKEN = None
zapi = ZabbixAPI(ZABBIX_SERVER)

# Authencication 
zapi.login('Admin', 'zabbix')

def network_status() -> str : 
    hosts = zapi.host.get()
    available_hosts = zapi.host.get(filter={'available': '1'})
    unavailable_hosts = zapi.host.get(filter={'available': '0'})
    resp = termcolor.colored("STATUT DU RESEAU", color='green') 
    resp += '\n----------------------------------------------'
    resp += f"\n* Nombre total d'hôtes : {len(hosts)}" 
    resp += f"\n* Nombre d'hôtes actifs : {len(available_hosts)}"
    resp += f"\n* Nombre d'hôtes inactifs : {len(unavailable_hosts)}" 
    resp += '----------------------------------------------\n\n'
    resp += 'List des hôtes :\n\n'
    for host in hosts :
        resp += f"\nid={host['hostid']} | Nom={host['host']} | statut={'Actif' if host['available']=='1' else 'Inactif'}"
    return resp  

def activity_status() -> str : 
    """Permet d'avoir la liste des dernières alertes"""      
    problems = zapi.problem.get()
    resp = '**************************************************\n'
    resp += termcolor.colored("LISTE DES ALERTES DANS LE RESEAU", color='red') 
    resp += '\n**************************************************'
    for problem in problems :
        host = zapi.event.get(eventids=problem['eventid'], selectHosts = ["host","name"])[0]['hosts'][0]['host']
        resp += f"\n[!] ''{termcolor.colored(host, color='blue')}'' : {termcolor.colored(problem['name'], color='red')} | Date : {datetime.datetime.fromtimestamp(int(problem['clock'])).isoformat()} | Sévérité : {problem['severity']}\n"
    return resp

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



