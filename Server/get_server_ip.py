def get_server_ip(filename: str, local: bool = False):
    if local:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    else:
        with open(filename) as file:
            for st in file:
                return st
