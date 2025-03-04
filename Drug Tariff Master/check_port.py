import socket

def is_port_open(host, port):
    """Check if a port is open on the given host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is OPEN on {host}")
            return True
        else:
            print(f"Port {port} is CLOSED on {host} (error code: {result})")
            return False
    except Exception as e:
        print(f"Error checking port {port} on {host}: {str(e)}")
        return False
    finally:
        s.close()

if __name__ == "__main__":
    is_port_open("127.0.0.1", 5000) 