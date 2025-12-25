import socket
open_ports_list = []

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
                print(banner)
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

for port in range(1, 100):
    print(f"Teste Port {port}...", end="\r")
    is_open, banner = check_port_and_grab("127.0.0.1", port)
    if is_open:
            open_ports_list.append((port, banner))


print("Scan abgeschlossen.")
print("Offene Ports inklusive Banner:", open_ports_list)


