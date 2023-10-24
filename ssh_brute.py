import subprocess
import datetime


login_attempts = {}
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

###### IPTABLES ######
iptables = f"journalctl -t sshd -f -S '{current_time}'"

process = subprocess.Popen(iptables, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

###### JOURNALCTL ######
for linha in process.stdout:
    if "sshd" in linha and ("Accepted password" in linha or "Failed password" in linha):
        print("Requisição de login SSH:")
        print(linha.strip())  
        parts = linha.split()
        ip = parts[parts.index("from") + 1]

        if ip in login_attempts:
            login_attempts[ip] += 1
        else:
            login_attempts[ip] = 1

        if login_attempts[ip] >= 3:
            print(f"IP {ip} bloqueado. Reason: SSH Bruteforce")
            iptables = f"sudo iptables -A INPUT -s {ip} -j DROP"
            subprocess.run(iptables, shell=True)

#EXECUTANDO PRA SEMPRE
process.wait()
