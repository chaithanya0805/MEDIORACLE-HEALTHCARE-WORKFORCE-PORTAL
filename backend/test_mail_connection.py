import socket
import sys

def test_connection(host, port):
    print(f"Testing TCP connection to {host}:{port}...")
    try:
        # 5 second timeout
        s = socket.create_connection((host, port), timeout=5)
        s.close()
        print(f"  SUCCESS: Successfully connected to {host}:{port}!")
        return True
    except Exception as e:
        print(f"  FAILED: Connection to {host}:{port} failed: {e}")
        return False

if __name__ == '__main__':
    print("Nexgile SMTP Connectivity Diagnostic Tool")
    print("=========================================")
    
    r587 = test_connection("smtp.gmail.com", 587)
    r465 = test_connection("smtp.gmail.com", 465)
    
    print("\nRecommendation:")
    if r587:
        print("Your network allows outbound traffic on Port 587 (TLS).")
        print("Please configure .env with:")
        print("  EMAIL_HOST=smtp.gmail.com")
        print("  EMAIL_PORT=587")
        print("  EMAIL_USE_TLS=True")
        print("  EMAIL_USE_SSL=False")
    elif r465:
        print("Your network blocks Port 587 but allows Port 465 (SSL).")
        print("Please configure .env with:")
        print("  EMAIL_HOST=smtp.gmail.com")
        print("  EMAIL_PORT=465")
        print("  EMAIL_USE_TLS=False")
        print("  EMAIL_USE_SSL=True")
    else:
        print("Both Port 587 and Port 465 are unreachable.")
        print("This indicates your network, firewall, VPN, or antivirus is blocking outbound SMTP connections entirely.")
        print("Please check your local Windows Firewall, antivirus outgoing mail scanning, or network settings.")
