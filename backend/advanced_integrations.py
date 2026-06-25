"""
Advanced Integrations Module
Includes connectors for enterprise security tools and threat hunting capabilities
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import subprocess
import os

# ============================================================================
# SECTION 1: EDR/XDR INTEGRATIONS
# ============================================================================

class CrowdStrikeConnector:
    """Falcon Endpoint Protection Integration"""
    
    def __init__(self, client_id, client_secret, base_url="https://api.crowdstrike.com"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token = self._get_auth_token()
    
    def _get_auth_token(self):
        """Authenticate and get OAuth token"""
        response = requests.post(
            f"{self.base_url}/oauth2/token",
            auth=(self.client_id, self.client_secret),
            data={"client_id": self.client_id, "client_secret": self.client_secret}
        )
        return response.json()['access_token']
    
    def get_detections(self, limit=50, offset=0):
        """Retrieve CrowdStrike detections"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(
            f"{self.base_url}/detects/queries/detects/v1",
            headers=headers,
            params={"limit": limit, "offset": offset}
        )
        
        detection_ids = response.json()['resources']
        
        # Get detailed detection info
        details_response = requests.post(
            f"{self.base_url}/detects/entities/summaries/GET/v1",
            headers=headers,
            json={"ids": detection_ids}
        )
        
        return details_response.json()['resources']
    
    def isolate_host(self, device_id):
        """Isolate infected host from network"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.post(
            f"{self.base_url}/host-group-actions/entities/actions/v1",
            headers=headers,
            json={
                "action_name": "contain",
                "ids": [device_id]
            }
        )
        
        return response.json()
    
    def get_running_processes(self, device_id):
        """Get running processes on a device"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(
            f"{self.base_url}/processes/entities/processes/v1",
            headers=headers,
            params={"ids": [device_id]}
        )
        
        return response.json()


class SentinelOneConnector:
    """SentinelOne XDR Integration"""
    
    def __init__(self, api_token, base_url="https://api.sentinelone.com"):
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {"Authorization": f"Token {api_token}"}
    
    def get_threats(self, status="active"):
        """Get active threats"""
        response = requests.get(
            f"{self.base_url}/web/api/v2.1/threats",
            headers=self.headers,
            params={"threatStatus": status, "limit": 100}
        )
        
        return response.json()['data']
    
    def quarantine_file(self, threat_id):
        """Quarantine infected file"""
        response = requests.post(
            f"{self.base_url}/web/api/v2.1/threats/{threat_id}/quarantine",
            headers=self.headers
        )
        
        return response.json()
    
    def get_agent_logs(self, agent_uuid):
        """Get logs from specific agent"""
        response = requests.get(
            f"{self.base_url}/web/api/v2.1/agents/{agent_uuid}/logs",
            headers=self.headers
        )
        
        return response.json()['data']


# ============================================================================
# SECTION 2: THREAT HUNTING QUERIES
# ============================================================================

class ThreatHunter:
    """Threat Hunting Engine with Pre-built Queries"""
    
    def __init__(self, siem_connector):
        self.siem = siem_connector
    
    def hunt_living_off_land(self):
        """
        Hunt for Living off the Land attacks (LOLBAS)
        Uses legitimate Windows tools for malicious purposes
        """
        queries = {
            "powershell_download": {
                "query": """
                    (process_name:powershell.exe OR process_name:pwsh.exe) AND
                    (command_line:"Invoke-WebRequest" OR 
                     command_line:"DownloadFile" OR
                     command_line:"DownloadString" OR
                     command_line:"IEX")
                """,
                "severity": "high",
                "mitre_technique": "T1086"
            },
            "wmic_execution": {
                "query": """
                    process_name:wmic.exe AND
                    (command_line:"process call create" OR
                     command_line:"PROCESS CALL CREATE" OR
                     command_line:"/node")
                """,
                "severity": "high",
                "mitre_technique": "T1047"
            },
            "certutil_download": {
                "query": """
                    process_name:certutil.exe AND
                    (command_line:"-urlcache" OR
                     command_line:"-downloadfile" OR
                     command_line:"-download")
                """,
                "severity": "critical",
                "mitre_technique": "T1105"
            },
            "cmstp_execution": {
                "query": """
                    process_name:cmstp.exe AND
                    (command_line:"/s" OR command_line:"/au")
                """,
                "severity": "critical",
                "mitre_technique": "T1191"
            }
        }
        
        results = {}
        for hunt_name, hunt_config in queries.items():
            results[hunt_name] = self.siem.search(hunt_config['query'])
        
        return results
    
    def hunt_lateral_movement(self):
        """Hunt for lateral movement techniques"""
        queries = {
            "psexec_usage": {
                "query": "process_name:psexec* OR command_line:PsExec",
                "mitre": "T1021"
            },
            "wmi_lateral": {
                "query": "process_name:wmiexec* OR WMI connection to remote host",
                "mitre": "T1047"
            },
            "winrm_usage": {
                "query": "process_name:winrm* OR WinRM service",
                "mitre": "T1021.006"
            },
            "pass_the_hash": {
                "query": "Kerberos without password OR NTLM hash reuse",
                "mitre": "T1550.002"
            },
            "kerberoast": {
                "query": "ServicePrincipalName request OR TGS-REQ for user",
                "mitre": "T1558.003"
            }
        }
        
        results = {}
        for hunt_name, config in queries.items():
            results[hunt_name] = self.siem.search(config['query'])
        
        return results
    
    def hunt_persistence_mechanisms(self):
        """Hunt for persistence techniques"""
        queries = {
            "registry_autorun": {
                "query": """
                    event_type:registry AND
                    path:*Run* AND
                    (value:*.exe OR value:*.vbs OR value:*.js)
                """,
                "mitre": "T1547.001"
            },
            "scheduled_task": {
                "query": """
                    process:schtasks.exe OR
                    event_id:4698 (Task Scheduler creation)
                """,
                "mitre": "T1053.005"
            },
            "startup_folder": {
                "query": """
                    file_path:*Startup* AND
                    file_type:(exe, vbs, js, lnk)
                """,
                "mitre": "T1547.004"
            },
            "wmi_event_binding": {
                "query": """
                    WMI event subscription created OR
                    ActiveScriptEventConsumer
                """,
                "mitre": "T1547.020"
            }
        }
        
        return {name: self.siem.search(config['query']) 
                for name, config in queries.items()}
    
    def hunt_credential_theft(self):
        """Hunt for credential dumping/theft"""
        queries = {
            "lsass_access": {
                "query": """
                    process:lsass.exe AND
                    (access:0x1010 OR access:0x1038)
                """,
                "mitre": "T1003.001"
            },
            "registry_samsam": {
                "query": "registry:HKLM\\SAM OR registry:HKLM\\SECURITY",
                "mitre": "T1003.002"
            },
            "credential_dumping_tools": {
                "query": """
                    process:(mimikatz* OR procdump* OR secretsdump* OR
                            pypykatz* OR hashcat*)
                """,
                "mitre": "T1003"
            },
            "password_spray": {
                "query": """
                    event_id:4625 (failed login) AND
                    multiple accounts AND
                    same source_ip
                """,
                "mitre": "T1110.003"
            }
        }
        
        return {name: self.siem.search(config['query']) 
                for name, config in queries.items()}
    
    def hunt_c2_communication(self):
        """Hunt for Command and Control communication"""
        queries = {
            "dns_tunneling": {
                "query": """
                    dns_query_length > 200 OR
                    dns_subdomain_count > 10 OR
                    dns_entropy > 4.5
                """,
                "mitre": "T1071.004"
            },
            "http_beaconing": {
                "query": """
                    http_request_interval < 5_minutes AND
                    http_response_size < 1KB AND
                    consistency:high
                """,
                "mitre": "T1071.001"
            },
            "dga_domains": {
                "query": """
                    domain_entropy > 4.0 AND
                    new_domain AND
                    similar_to_other_domains
                """,
                "mitre": "T1568.002"
            },
            "tor_exit_nodes": {
                "query": "destination_ip IN tor_exit_node_list",
                "mitre": "T1090.003"
            }
        }
        
        return {name: self.siem.search(config['query']) 
                for name, config in queries.items()}


# ============================================================================
# SECTION 3: MALWARE ANALYSIS INTEGRATION
# ============================================================================

class MalwareAnalysisConnector:
    """Interface with external malware analysis services"""
    
    def __init__(self):
        self.virustotal_key = os.environ.get('VIRUSTOTAL_API_KEY')
        self.hybrid_key = os.environ.get('HYBRID_ANALYSIS_KEY')
        self.any_run_key = os.environ.get('ANYRUN_API_KEY')
    
    def submit_virustotal(self, file_hash, file_path=None):
        """Submit file to VirusTotal for analysis"""
        
        url = "https://www.virustotal.com/api/v3/files"
        headers = {"x-apikey": self.virustotal_key}
        
        if file_path:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, headers=headers, files=files)
        else:
            # Check existing hash
            response = requests.get(
                f"https://www.virustotal.com/api/v3/files/{file_hash}",
                headers=headers
            )
        
        return response.json()
    
    def get_dynamic_analysis(self, sample_hash):
        """Get dynamic analysis from Hybrid-Analysis"""
        
        response = requests.post(
            "https://www.hybrid-analysis.com/api/v2/search/hash",
            headers={"api-key": self.hybrid_key},
            json={"hash": sample_hash}
        )
        
        return response.json()
    
    def submit_anyrun(self, file_path):
        """Submit to ANY.RUN for behavioral analysis"""
        
        with open(file_path, 'rb') as f:
            files = {'file': ('sample', f)}
            response = requests.post(
                "https://api.any.run/v1/analysis",
                headers={"Authorization": f"Bearer {self.any_run_key}"},
                files=files,
                data={"_info": "SOC_Assistant"}
            )
        
        return response.json()


# ============================================================================
# SECTION 4: OSINT & RECONNAISSANCE
# ============================================================================

class OSINTCollector:
    """Gather Open Source Intelligence"""
    
    def __init__(self):
        self.shodan_key = os.environ.get('SHODAN_API_KEY')
    
    def shodan_search(self, query):
        """Search Shodan for exposed services"""
        import shodan
        
        api = shodan.Shodan(self.shodan_key)
        results = api.search(query)
        
        return {
            "total_results": results['total'],
            "matches": [{
                "ip": item['ip_str'],
                "port": item['port'],
                "org": item.get('org', 'Unknown'),
                "country": item.get('country_code', 'Unknown'),
                "product": item.get('product', 'Unknown'),
                "version": item.get('version', 'Unknown')
            } for item in results['matches']]
        }
    
    def domain_intelligence(self, domain):
        """Gather intelligence on a domain"""
        import dns.resolver
        import whois
        
        intel = {
            "domain": domain,
            "whois": None,
            "dns_records": {},
            "mx_records": [],
            "ns_records": [],
            "txt_records": []
        }
        
        # WHOIS
        try:
            intel['whois'] = str(whois.whois(domain))
        except:
            pass
        
        # DNS records
        try:
            resolver = dns.resolver.Resolver()
            
            # A records
            intel['dns_records']['A'] = [str(r) for r in resolver.resolve(domain, 'A')]
            
            # MX records
            intel['mx_records'] = [str(r) for r in resolver.resolve(domain, 'MX')]
            
            # NS records
            intel['ns_records'] = [str(r) for r in resolver.resolve(domain, 'NS')]
            
            # TXT records (SPF, DKIM, DMARC)
            intel['txt_records'] = [str(r) for r in resolver.resolve(domain, 'TXT')]
        except:
            pass
        
        return intel
    
    def ip_intelligence(self, ip_address):
        """Gather intelligence on IP address"""
        import pygeoip
        
        geoip = pygeoip.GeoIP('/path/to/GeoIP.dat')
        
        return {
            "ip": ip_address,
            "country": geoip.country_name_by_addr(ip_address),
            "city": geoip.city_by_addr(ip_address),
            "organization": geoip.org_by_addr(ip_address)
        }


# ============================================================================
# SECTION 5: NETWORK ANALYSIS & PACKET INSPECTION
# ============================================================================

class NetworkAnalyzer:
    """Network traffic analysis and inspection"""
    
    @staticmethod
    def analyze_pcap(pcap_file):
        """Analyze PCAP file for suspicious traffic"""
        import pyshark
        
        cap = pyshark.FileCapture(pcap_file)
        
        analysis = {
            "total_packets": len(cap),
            "protocols": {},
            "suspicious_flows": [],
            "indicators": []
        }
        
        for packet in cap:
            if packet.highest_layer not in analysis['protocols']:
                analysis['protocols'][packet.highest_layer] = 0
            analysis['protocols'][packet.highest_layer] += 1
        
        return analysis
    
    @staticmethod
    def detect_beaconing(pcap_file):
        """Detect C2 beaconing patterns"""
        import pyshark
        
        cap = pyshark.FileCapture(pcap_file)
        
        intervals = []
        last_time = None
        
        for packet in cap:
            if 'IP' in packet:
                current_time = float(packet.sniff_time)
                
                if last_time:
                    intervals.append(current_time - last_time)
                
                last_time = current_time
        
        # Check for regularity
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        return {
            "average_interval": avg_interval,
            "is_regular": bool(avg_interval and avg_interval < 300),
            "beaconing_confidence": min(100, len(intervals) / 100 * 100)
        }


# ============================================================================
# SECTION 6: COMPLIANCE & GRC
# ============================================================================

class ComplianceChecker:
    """Check security posture against compliance frameworks"""
    
    @staticmethod
    def check_pci_dss_compliance(findings):
        """Verify PCI-DSS compliance"""
        
        pci_requirements = {
            "1": "Firewall configuration",
            "2": "Default passwords removed",
            "3": "Cardholder data protection",
            "4": "Encryption of data in transit",
            "5": "Antivirus protection",
            "6": "Secure applications",
            "7": "Access control",
            "8": "User identification",
            "9": "Physical access control",
            "10": "Logging and monitoring",
            "11": "Security testing",
            "12": "Information security policy"
        }
        
        compliance_status = {}
        
        for req_id, requirement in pci_requirements.items():
            # Check if requirement is met based on findings
            compliance_status[req_id] = {
                "requirement": requirement,
                "status": "compliant" if check_requirement(findings, req_id) else "non-compliant"
            }
        
        return compliance_status
    
    @staticmethod
    def check_nist_csf_mapping(detections):
        """Map security findings to NIST CSF categories"""
        
        nist_categories = {
            "IDENTIFY": ["Asset Management", "Business Environment"],
            "PROTECT": ["Access Control", "Data Security", "Protective Technology"],
            "DETECT": ["Anomalies", "Security Continuous Monitoring"],
            "RESPOND": ["Response Planning", "Communications", "Analysis"],
            "RECOVER": ["Recovery Planning", "Improvements", "Communications"]
        }
        
        return nist_categories


# ============================================================================
# SECTION 7: INCIDENT RESPONSE PLAYBOOKS
# ============================================================================

class IncidentPlaybooks:
    """Pre-built incident response playbooks"""
    
    @staticmethod
    def ransomware_response():
        """Ransomware incident response playbook"""
        return {
            "detection": [
                "Monitor file encryption activities",
                "Alert on mass file modifications",
                "Detect ransom note creation"
            ],
            "immediate_actions": [
                "Isolate affected systems",
                "Disconnect from network",
                "Disable network access for that segment"
            ],
            "investigation": [
                "Identify patient zero",
                "Review recent logins",
                "Check for lateral movement",
                "Collect forensics evidence"
            ],
            "eradication": [
                "Remove malware/ransomware",
                "Reset compromised credentials",
                "Patch vulnerable systems",
                "Review and harden access controls"
            ],
            "recovery": [
                "Restore from clean backups",
                "Rebuild systems if necessary",
                "Verify integrity of restored data",
                "Gradually reconnect to network"
            ]
        }
    
    @staticmethod
    def data_exfiltration_response():
        """Data exfiltration incident response playbook"""
        return {
            "detection": [
                "Monitor outbound data volume",
                "Alert on unusual external connections",
                "Track large file transfers"
            ],
            "immediate_actions": [
                "Block external IP",
                "Quarantine user account",
                "Preserve network logs",
                "Snapshot affected systems"
            ],
            "investigation": [
                "Identify what data was exfiltrated",
                "Determine duration of exfiltration",
                "Find attacker access point",
                "Review user activities"
            ],
            "eradication": [
                "Remove attacker access",
                "Reset credentials",
                "Patch entry vectors",
                "Enable enhanced monitoring"
            ]
        }


if __name__ == "__main__":
    print("Security Integration Modules Loaded")
    print("=" * 60)
    print("Available integrations:")
    print("  - CrowdStrike EDR")
    print("  - SentinelOne XDR")
    print("  - Threat Hunting Engine")
    print("  - Malware Analysis")
    print("  - OSINT Collector")
    print("  - Network Analyzer")
    print("  - Compliance Checker")
    print("  - Incident Response Playbooks")
