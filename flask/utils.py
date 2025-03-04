import whois
import dns.resolver
import ssl
import socket
from datetime import datetime

TRUSTED_SSL_PROVIDERS = {"DigiCert Inc", "Entrust, Inc.", "GlobalSign", "Sectigo Limited", "Let's Encrypt","Google Trust Services"}

def whois_lookup(domain):
    try:
        return whois.whois(domain)
    except Exception:
        return None

def dns_lookup(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [ip.address for ip in result]
    except Exception:
        return []

def ssl_certificate_check(domain):
    try:
        conn = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            sock = conn.wrap_socket(sock, server_hostname=domain)
            cert = sock.getpeercert()
        return {
            "issuer": dict(x[0] for x in cert.get("issuer", [])),
            "subject": dict(x[0] for x in cert.get("subject", [])),
            "valid_from": cert.get("notBefore", ""),
            "valid_to": cert.get("notAfter", ""),
        }
    except Exception:
        return None

import json
from datetime import datetime

TRUSTED_SSL_PROVIDERS = {"DigiCert", "Entrust", "Google Trust Services", "Let's Encrypt"}

def calculate_score(domain, whois_info, ssl_info, dns_info, js_ip, db_ip):
    score = 0

    # Fix: Convert WHOIS JSON string to dictionary
    if isinstance(whois_info, str):
        whois_info = json.loads(whois_info)

    # Fix: Extract and convert creation_date properly
    if whois_info and "creation_date" in whois_info:
        creation_date_data = whois_info["creation_date"]
        if isinstance(creation_date_data, list):
            creation_date_data = creation_date_data[0]

        if isinstance(creation_date_data, str):
            try:
                creation_date = datetime.strptime(creation_date_data, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                creation_date = None
        else:
            creation_date = creation_date_data

        #  Calculate domain age
        if creation_date:
            age = (datetime.utcnow() - creation_date).days // 365
            if age >= 1:
                score += 50  # Should be added correctly now

    #  Fix: Proper SSL Issuer Check
    if ssl_info and "issuer" in ssl_info:
        issuer_org = ssl_info["issuer"].get("organizationName", "")
        if issuer_org in TRUSTED_SSL_PROVIDERS:
            score += 30

    #  Fix: DNS and IP Matching
    if dns_info:
        if db_ip in dns_info:
            score += 20  # If DB IP matches
        elif js_ip in dns_info:
            score += 10  # If JS IP matches
    

    return score

