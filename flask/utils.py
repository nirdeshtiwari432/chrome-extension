import whois
import dns.resolver
import ssl
import socket
from datetime import datetime

TRUSTED_SSL_PROVIDERS = {"DigiCert Inc", "Entrust, Inc.", "GlobalSign", "Sectigo Limited", "Let's Encrypt"}

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

def calculate_score(domain, whois_info, ssl_info, dns_info, js_ip, db_ip):
    score = 0
    if whois_info and whois_info.creation_date:
        creation_date = whois_info.creation_date[0] if isinstance(whois_info.creation_date, list) else whois_info.creation_date
        age = (datetime.utcnow() - creation_date).days // 365
        if age > 2:
            score += 50
    if ssl_info and ssl_info.get("issuer"):
        issuer_org = ssl_info["issuer"].get("organizationName", "")
        if issuer_org in TRUSTED_SSL_PROVIDERS:
            score += 30
    if js_ip in dns_info and (db_ip is None or js_ip == db_ip):
        score += 20
    return score
