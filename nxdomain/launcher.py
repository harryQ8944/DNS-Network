import sys
from pathlib import Path
from typing import Dict, List


def is_valid_domain(domain: str) -> bool:
    labels = domain.split('.')
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



def is_valid_port(port: int) -> bool:
    return 1024 <= port <= 65535


def generate_unique_port(master_port: int, used_ports: set) -> int:
    """Generate a unique port number."""
    port = master_port
    while port in used_ports:
        port += 1
    used_ports.add(port)
    return port

def generate_config_files(single_dir: Path, records: Dict[str, int], master_port: int) -> None:
    if not records:
        return
    
    used_ports = {master_port} | set(records.values())
    roots = {}
    tlds = {}
    auths = {}
    unique_ports_for_tlds = {}

    for record, port in records.items():
        parts = record.split('.')
        
        root = parts[-1]
        tld = parts[-2]
        auth = '.'.join(parts[:-1])

        if root not in roots:
            port = generate_unique_port(master_port, used_ports)
            roots[root] = port

        full_tld = f"{tld}.{root}"
        if full_tld not in tlds:
            tlds[full_tld] = roots[root] 

        full_auth = f"{auth}.{tld}.{root}"
        if full_auth not in auths:
            port = generate_unique_port(master_port, used_ports)
            auths[full_auth] = port

    # Generate the root.conf file
    with open(single_dir + "/root.conf", "w") as root_file:
        root_file.write(f"{master_port}\n")
        for root, port in roots.items():
            root_file.write(f"{root}, {port}\n")

    # Generate the tld-*.conf files
    processed_tld_names = set()  # To keep track of TLD names we've processed
    for tld, port in tlds.items():
        tld_name = tld.split('.')[-1]
        with open(single_dir + f"/tld-{tld_name}.conf", "a") as tld_file:
            if tld_name not in processed_tld_names:  # Only write port if TLD name is new
                tld_file.write(f"{port}\n")
                processed_tld_names.add(tld_name)  # Mark this TLD name as processed
            
            unique_port_for_tld = generate_unique_port(master_port, used_ports)
            unique_ports_for_tlds[tld] = unique_port_for_tld  # Store this for auths
            tld_file.write(f"{tld}, {unique_port_for_tld}\n")

    # Generate the auth-*.conf files
    for tld in tlds:
        tld_name = tld.split('.')[-2]
        with open(single_dir + f"/auth-{tld_name}.conf", "w") as auth_file:
            # Using the stored unique port number for the TLD
            auth_file.write(f"{unique_ports_for_tlds[tld]}\n")
            
            # Now, write the full domains (auth) from the master file for this TLD
            for auth_domain, port in records.items():
                if auth_domain.endswith(tld):
                    auth_file.write(f"{auth_domain}, {port}\n")




def main(args: List[str]) -> None:
    
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        return
    
    master_file = args[0]
    single_dir = args[1]

    master_file, single_dir = args
    master_path = Path(master_file)
    single_dir_path = Path(single_dir)

    if not master_path.exists() or not master_path.is_file():
        print("INVALID MASTER")
        return

    if not single_dir_path.exists() or not single_dir_path.is_dir():
        print("NON-WRITABLE SINGLE DIR")
        return

    try:
        with open(master_file, 'r') as file:
            lines = file.readlines()
            

        master_port = int(lines[0].strip())
        if not is_valid_port(master_port):
            raise ValueError

        records = {}
        for line in lines[1:]:
            domain, port_str = line.strip().split(',')
            port = int(port_str)

            if not is_valid_domain(domain):
                raise ValueError

            port = int(port_str)
            if not is_valid_port(port) or domain in records:
                raise ValueError

            records[domain] = port

    except ValueError:
        print("INVALID MASTER")
        return
    
    generate_config_files(single_dir, records, master_port)



if __name__ == "__main__":
    main(sys.argv[1:])