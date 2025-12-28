import socket
import threading
from concurrent.futures import ThreadPoolExecutor

open_ports_list = []
list_lock = threading.Lock()

def check_port_and_grab(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, port))

        if result == 0:
                try:
                    data = sock.recv(1024)
                except socket.timeout:
                    data = b""
                if not data:
                    try:
                        sock.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                        data = sock.recv(1024)
                    except socket.timeout:
                        data = b""
                banner = data.decode(errors="ignore")
                return True, banner
        else:
            sock.close()
            return False, ""
    except Exception as e:
        print(f"Fehler: {e}")
        sock.close()
        return False, ""
    finally:
        sock.close()

def worker(ip, port):
    is_open, banner = check_port_and_grab(ip, port)
    if is_open:
        with list_lock:
            open_ports_list.append((port, banner))
            print(f"Port {port} offen: {banner[:50]}")

test_ports = range(1, 100)
threads = []

with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(worker, range(1, 100))

print("Scan abgeschlossen.")
print("Offene Ports inklusive Banner:", open_ports_list)


