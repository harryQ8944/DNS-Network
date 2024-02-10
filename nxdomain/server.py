import socket
import sys
from pathlib import Path
from typing import Dict, List


class DNSServer:
    def __init__(self, config_file: str):
        self.records: Dict[str, int] = {}
        self.buffer = ""
        self.load_config(config_file)

    def is_valid_domain(self, domain: str) -> bool:
        if not domain or domain[0] == '.' or domain[-1] == '.':
            return False
        labels = domain.split('.')
        return all(label.isalnum() or '-' in label for label in labels)

    def load_config(self, config_file: str):
        try:
            with open(config_file, 'r') as file:
                lines = file.readlines()
                self.port = int(lines[0].strip())
                
                if not 0 <= self.port <= 65535:
                    raise ValueError

                for line in lines[1:]:
                    domain, port = line.strip().split(',')
                    port = int(port)

                    if not 0 <= port <= 65535 or not self.is_valid_domain(domain):
                        raise ValueError

                    self.records[domain] = port
        except Exception:
            print("INVALID CONFIGURATION")
            sys.exit()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                s.bind(('localhost', self.port))
            except OSError as e:
                print("INVALID CONFIGURATION")
                return
            
            s.listen()

            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024).decode()
                    self.buffer += data
                    if '\n' in self.buffer:
                        commands = self.buffer.split('\n')
                        for command in commands[:-1]:
                            response = self.process_command(command.strip())
                            if response:
                                conn.sendall(response.encode())
                        self.buffer = commands[-1]

    def process_command(self, command: str) -> str:
        if command.startswith('!'):
            return self.process_server_command(command)
        else:
            return self.resolve_hostname(command)

    def process_server_command(self, command: str) -> str:
        parts = command.split()
        cmd = parts[0]

        try:
            if cmd == "!ADD" and len(parts) == 3:
                hostname, port = parts[1], int(parts[2])
                if not self.is_valid_domain(hostname) or not (0 <= port <= 65535):
                    raise ValueError
                self.records[hostname] = port
                return ""
            elif cmd == "!DEL" and len(parts) == 2:
                hostname = parts[1]
                if not self.is_valid_domain(hostname):
                    raise ValueError
                if hostname in self.records:
                    del self.records[hostname]
                return ""
            elif cmd == "!EXIT":
                sys.exit()
            else:
                raise ValueError
        except ValueError:
            return "INVALID\n"

    def resolve_hostname(self, hostname: str) -> str:
        if hostname in self.records:
            port = self.records[hostname]
            print(f"resolve {hostname} to {port}")
            return f"{port}\n"
        else:
            print(f"resolve {hostname} to NXDOMAIN")
            return "NXDOMAIN\n"

def main(args: List[str]) -> None:
    if len(args) != 1:
        print("INVALID ARGUMENTS")
        return

    config_file = args[0]
    server = DNSServer(config_file)
    server.start()

if __name__ == "__main__":
    main(sys.argv[1:])