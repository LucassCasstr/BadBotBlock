import subprocess
import re
import requests

#CHAVE
api_key = "ABUSE_DB_API_KEY"

#CORZINHA BONITINHA
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


###### IPTABLES ######

def block_ip(ip):
    iptables = f"sudo iptables -A INPUT -s {ip} -j DROP"
    subprocess.run(iptables, shell=True)


###### ABUSEDBIP ######

check = set() 
def AbuseDBIP(ip, api_key):
    
    #VERIFICA SE O IP JÁ FOI CHECADO ANTES
    if ip in check:
        #print(bcolors.OKGREEN + f"AVISO: O endereço IP {ip} ja foi verificado." + bcolors.ENDC)
        return  

    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
    headers = {'Key': api_key, 'Accept': 'application/json'}
    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        data = response.json()
        if data['data']['abuseConfidenceScore'] >= 20:
            print( bcolors.FAIL + f" - O endereço IP {ip} é malicioso." + bcolors.ENDC)
            print("")
            print(f" - Porcentagem de certeza: {data['data']['abuseConfidenceScore']}%")
            print("")
            block_ip(ip)
        elif ip == "192.168.0.109":
            print(bcolors.FAIL + f"Endereço {ip} é malicioso" + bcolors.ENDC)
            block_ip(ip)
    else:
        print(f"ERRO: {response.text}")

    check.add(ip) 


###### TCP DUMP ######


tcpdump = "tcpdump -l -i eth0 host 192.168.0.113" #SUBSTITUA O "HOST" PELO IP DA MÁQUINA LINUX QUE QUERES DEFENDER
process = subprocess.Popen(tcpdump, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

for linha in process.stdout:
    print(linha.strip())  
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', linha)
    for ip in ips:
        AbuseDBIP(ip, api_key)  


#RODANDO INFINITAMENTE
process.wait()
