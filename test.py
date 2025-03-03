import whois
import dns.resolver
import ssl
import socket
import requests
from urllib.parse import urlparse

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        return f"Error in WHOIS lookup: {e}"

def dns_lookup(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [ip.address for ip in result]
    except Exception as e:
        return f"Error in DNS lookup: {e}"

def ssl_certificate_check(domain):
    try:
        conn = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            sock = conn.wrap_socket(sock, server_hostname=domain)
            cert = sock.getpeercert()
        return cert
    except Exception as e:
        return f"Error in SSL certificate check: {e}"

def get_domain_ip_from_dns(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        return result[0].address
    except Exception as e:
        return f"Error resolving domain IP: {e}"

def compare_ip(js_ip, domain):
    python_ip = get_domain_ip_from_dns(domain)
    if js_ip == python_ip:
        return f"The IP addresses match. Both are {js_ip}."
    else:
        return f"The IP addresses do not match. JavaScript IP: {js_ip}, Python IP: {python_ip}"

def check_website(domain, js_ip):
    print(f"Checking website: {domain}")
    
    # Step 1: WHOIS Lookup
    whois_info = whois_lookup(domain)
    print(f"\nWHOIS Lookup:\n{whois_info}")
    
    # Step 2: DNS Lookup
    dns_info = dns_lookup(domain)
    print(f"\nDNS Lookup (A record):\n{dns_info}")
    
    # Step 3: SSL Certificate Check
    ssl_info = ssl_certificate_check(domain)
    print(f"\nSSL Certificate:\n{ssl_info}")
    
    # Step 4: Compare IP addresses from JavaScript and DNS resolution
    ip_comparison = compare_ip(js_ip, domain)
    print(f"\nIP Comparison:\n{ip_comparison}")

if __name__ == "__main__":
    # Input from JavaScript (simulated)
    js_ip = input("Enter the IP address from JavaScript (e.g., 57.144.125.32): ").strip()
    domain = input("Enter the domain to check (e.g., web.whatsapp.com): ").strip()
    
    check_website(domain, js_ip)
