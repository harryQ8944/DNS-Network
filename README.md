# DNS-infrastructure

The Domain Name System (DNS) is the phone book of the Internet. Humans access information online through domain names, like www.google.com or www.apple.com . Web browsers interact through Internet Protocol (IP) addresses. DNS translates domain names to IP addresses, so browsers can load Internet resources.
Each device connected to the Internet has a unique public IP address which other machines use to find the device. DNS servers eliminate the need for humans to memorise IP addresses such as 172.217.24.46 (in IPv4).
However, in the context of this, we want to reduce the complexity of communication over the Internet, therefore simplify the DNS server and implement the simplified DNS server. On the high level, we weaken the DNS functionality and assume all simplified DNS servers listen on the local network interface named localhost . Moreover, each simplified DNS server on
localhost occupies a unique port which other servers use to connect the server. Domain vs. Hostname
 When the DNS servers are running, any end user can ask the recursor to resolve a hostname. Then, the recursor initiates a chain of DNS queries to the DNS servers via TCP connection. 
 
Eventually, the recursor shall collect responses from the DNS servers, and resolve the hostname to a valid identifier or NXDOMAIN to the end use

On the high level, the DNS server is capable of the following:

1. Start up according to the given command-line arguments.

2. Accept DNS queries from the recursor via TCP.

3. Process the queries and reply to the recursor via TCP.

4. Log the server activities on the standard output.

5. Parse commands sent from the user via TCP and update the server.

   The recursor can:

1. Start up if the root DNS server is specified in command-line argument.

2. Read and validate a domain in the standard input.

3. Query a chain of DNS servers, and receive responses.

4. Resolve the domain and output the response in the standard output.
