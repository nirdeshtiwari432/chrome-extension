import mysql.connector
import socket

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "yourdatabase"
}

TABLE_NAME = "your_table"  
DOMAIN_COLUMN = "Domain"  
IP_COLUMN = "ip_address"       

def fetch_and_store_ips():
   
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Select domains that don't have an IP stored
    cursor.execute(f"SELECT `Rank`, `{DOMAIN_COLUMN}` FROM `{TABLE_NAME}` WHERE `{IP_COLUMN}` IS NULL OR `{IP_COLUMN}` = ''")
    rows = cursor.fetchall()

    for row_id, domain in rows:
        try:
            ip_address = socket.gethostbyname(domain)
            cursor.execute(f"UPDATE `{TABLE_NAME}` SET `{IP_COLUMN}` = %s WHERE `Rank` = %s", (ip_address, row_id))
            print(f"Updated {domain} → {ip_address}")
        except socket.gaierror:
            print(f"Failed to resolve: {domain}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    
    fetch_and_store_ips()
