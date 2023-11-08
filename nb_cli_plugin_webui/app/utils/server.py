import socket


def find_available_port(start_port: int, end_port: int) -> int:
    for port in range(start_port, end_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("localhost", port))
            return port
        except socket.error:
            pass
        finally:
            sock.close()

    raise ValueError("No available ports in this range.")
