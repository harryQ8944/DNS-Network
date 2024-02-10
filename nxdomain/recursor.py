import socket
import sys
import time

#pathlib , random , signal , sys.argv , socket , time , typing 

def validate_hostname(hostname: str) -> bool:
    labels = hostname.split('.')
    if len(labels) < 3:  # At least a C.B.A format
        return False

    # Validate A and B
    for label in labels[-2:]:
        if not (label.isalnum() or '-' in label):
            return False

    # Validate C
    c = '.'.join(labels[:-2])  # Take all labels except the last two
    if c.startswith('.') or c.endswith('.'):
        return False
    for part in c.split('.'):
        if not (part.isalnum() or '-' in part):
            return False

    return True



def query_server(port, hostname, timeout):
    try:
        with socket.create_connection(("localhost", port), timeout) as s:
            s.sendall(hostname.encode() + b'\n')
            response = s.recv(1024).decode().strip()
            if response == "NXDOMAIN":
                return None, response
            return int(response), None
    except socket.timeout:
        return None, "NXDOMAIN"
    except (ConnectionRefusedError, OSError):
        return None, "ERROR"


def main(args):
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        return

    try:
        root_port = int(args[0])
        if not (0 <= root_port <= 65535):
            raise ValueError

        timeout = float(args[1])
        if timeout <= 0:
            raise ValueError

    except ValueError:
        print("INVALID ARGUMENTS")
        return

    while True:
        try:
            hostname = input()
            
        except EOFError:
            break

        if not validate_hostname(hostname):
            print("INVALID")
            continue




        start_time = time.time()
        socket.setdefaulttimeout(timeout)

    # Step 1: Query the root nameserver
        tld_port, error = query_server(root_port, hostname.split('.')[-1], timeout)
        if error:
            if error == "ERROR":
                print("FAILED TO CONNECT TO ROOT")
            else:
                print(error)  # NXDOMAIN or TIMEOUT
            continue

        # Step 2: Query the TLD nameserver
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            print("NXDOMAIN")
            continue

        auth_port, error = query_server(tld_port, '.'.join(hostname.split('.')[-2:]), timeout - elapsed_time)
        if error:
            if error == "ERROR":
                print("FAILED TO CONNECT TO TLD")
            else:
                print(error)  # NXDOMAIN or TIMEOUT
            continue

        # Step 3: Query the authoritative nameserver
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            print("NXDOMAIN")
            continue

        identifier, error = query_server(auth_port, hostname, timeout - elapsed_time)
        if error:
            if error == "ERROR":
                print("FAILED TO CONNECT TO AUTH")
            else:
                print(error)  # NXDOMAIN or ERROR
            continue

        # Print the identifier and wait for the next input
        print(identifier)



if __name__ == "__main__":
    main(sys.argv[1:])