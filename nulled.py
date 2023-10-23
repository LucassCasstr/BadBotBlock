import requests
from ipwhois import IPWhois

print(" _      _     _     _     _____ ____ ")
print("/ \  /|/ \ /\/ \   / \   /  __//  _ \\")
print("| |\ ||| | ||| |   | |   |  \  | | \\|")
print("| | \||| \_/|| |_/\| |_/\|  /_ | |_/|")
print("\_/  \|\____/\____/\____/\____\\\____/")

#QUALIDAD
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

###### API KEY ######
api_key = "ABUSE_DB_API_KEY"

ip = input("Digite o endereço IP: ")

def get_country(ip):
    ipwhois = IPWhois(ip)
    results = ipwhois.lookup_rdap()
    country = results['asn_country_code']
    return country

###### VALIDANDO ######
def check_ip_abuse(ip, api_key):
    #API URL
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
    
    #HEADERS
    headers = {'Key': api_key, 'Accept': 'application/json'}
    
    #RESPONSE
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['data']['abuseConfidenceScore'] >= 4: #ALTERE CONFORME A NECESSIDADE
            print(bcolors.FAIL + f" - O endereço IP {ip} é malicioso." + bcolors.ENDC)
            print("")
            print(f" - Porcentagem de certeza: {data['data']['abuseConfidenceScore']}%")
            print("")
            country = get_country(ip)
            if country:
                print(f" - País de origem: {country}")
                
            else:
                print("NULL")
        else:
            print(f"O endereço IP {ip} não foi encontrado na lista de endereços IP maliciosos conhecidos.")
    else:
        print(f"ERRO: {response.text}")


check_ip_abuse(ip, api_key)
