import sys
from pathlib import Path


def read_file(filepath: str):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f.readlines()]


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


def validate_file(filename: str):
    data = read_file(filename)
    try:
        master_port = int(data[0])
        if not (1024 <= master_port <= 65535):
            return False
        for line in data[1:]:
            _, port_str = line.split(',')
            port = int(port_str)
            if not (1024 <= port <= 65535):
                return False
    except:
        return False
    return True





def check_configuration(root_file: Path, singles_dir: Path, port_in_first_line: list):

    with open(singles_dir + "/root.conf", "r") as file:
        root_data = file.readlines()


    # Extract records with domain as key and port as value
    records = {}
    for line in root_data[1:]:
        domain, port_str = line.split(',')
        # print(port_str)

        records[domain] = int(port_str)
        # print(records)

        if port_str not in port_in_first_line:
            print("neq")
            return

    

    for record, port in records.items():
        # Check if the specific conf file exists
        conf_file_path = singles_dir + f"/{record}.conf"
        
        if Path(conf_file_path).exists():
            conf_data = read_file(conf_file_path)
            
            if not conf_data:
                print("neq")
                return
            
            conf_port = int(conf_data[0])
    
            if conf_port != port:
                print("neq")
                return


            # For each domain in the conf file, check its corresponding specific conf file
            for line in conf_data[1:]:
                sub_domain, port_str = line.split(',')
                sub_domain_port = int(port_str)

                # Determine path for the specific conf file
                specific_conf_file_path = singles_dir + f"/{sub_domain}.conf"
                if Path(specific_conf_file_path).exists():
                    specific_conf_data = read_file(specific_conf_file_path)
                    specific_conf_port = int(specific_conf_data[0])
                    if specific_conf_port != sub_domain_port:
                        print("neq")
                        return

    print("eq")


        


def main():
    if len(sys.argv) != 3:
        print("invalid arguments")
        return
    
    master_file, singles_dir = sys.argv[1], sys.argv[2]

    if not Path(master_file).exists() or not Path(master_file).is_file():
        print("invalid master")
        return
    

    if not Path(singles_dir).exists() or not Path(singles_dir).is_dir():
        print("singles io error")
        return

    

    



    try:
            with open(master_file, 'r') as file:
                lines = file.readlines()
                if not lines:
                    print("Master file is empty.")
                    return

                

            master_port = int(lines[0].strip())
        

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
        print("invalid master")
        return

    master_data = read_file(master_file)

    all_single_data = []
    port_in_first_line =[]
    for single_file in Path(singles_dir).iterdir():
        if not single_file.is_file():
            continue
        if not validate_file(single_file):
            print("invalid single")
            return
        
        with open(single_file, 'r') as single:
            line = single.readlines()
        
        
        port_in_first_line.append(line[0])
    
    root_file = Path(singles_dir) / "root.conf"

    check_configuration(root_file, singles_dir, port_in_first_line)
    
    



if __name__ == "__main__":
    main()