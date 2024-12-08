# The Domain Name System (DNS) Server Infrastructure

The Domain Name System (DNS) is the phone book of the Internet. Humans access information online through domain names, like www.google.com or www.apple.com . Web browsers interact through Internet Protocol (IP) addresses. DNS translates domain names to IP addresses, so browsers can load Internet resources.Each device connected to the Internet has a unique public IP address which other machines use to find the device. DNS servers eliminate the need for humans to memorise IP addresses such as 172.217.24.46 (in IPv4).
However, in the context of this, we want to reduce the complexity of communication over the Internet, therefore simplify the DNS server and implement the simplified DNS server. On the high level, we weaken the DNS functionality and assume all simplified DNS servers listen on the local network interface named localhost .

Moreover, each simplified DNS server on
localhost occupies a unique port which other servers use to connect the server. Domain vs. Hostname
 When the DNS servers are running, any end user can ask the recursor to resolve a hostname. Then, the recursor initiates a chain of DNS queries to the DNS servers via TCP connection. 
 
When the DNS servers are running, any end user can ask the recursor to resolve a hostname.
Then, the recursor initiates a chain of DNS queries to the DNS servers via TCP connection.
Eventually, the recursor shall collect responses from the DNS servers, and resolve the hostname
to a valid identifier or NXDOMAIN to the end user.
Eventually, the recursor shall collect responses from the DNS servers, 
and resolve the hostname to a valid identifier or NXDOMAIN to the end use

* NXDOMAIN stands for a non-existent domain and represents an error DNS message received by
the Recursive DNS server (the client) when the requested domain cannot be resolved to an IP
address. In other words, an NXDOMAIN error message simply indicates that the domain does not
exist.

There are four components involved in resolving a domain:
1. The DNS recursor. The recursor can be thought of as a librarian who is asked to go find a
particular book somewhere in a library. The DNS recursor is a server designed to receive
queries from client. Typically, the recursor is then responsible for making additional requests
in order to satisfy the client's DNS query.
2. Root nameserver. The root server is the first step in translating (resolving) human-readable
host names into port identifiers. It can be thought of like an index in a library that points to
different racks of books - typically it serves as a reference to other more specific locations.
3. TLD nameserver. The top level domain server (TLD) can be thought of as a specific rack of
books in a library. This server is the next step in the search for a specific identifier, and it
hosts the last portion of a hostname.
4. Authoritative nameserver. This final nameserver can be thought of as a dictionary on a rack
of books, in which a specific name can be translated into its definition. The authoritative
nameserver is the last stop in the nameserver query. If the authoritative name server has
access to the requested record, it will return the identifier for the requested hostname back
to the DNS recursor (the librarian) that made the initial request.



On the high level, the DNS server is capable of the following:

1. Start up according to the given command-line arguments.

2. Accept DNS queries from the recursor via TCP.

3. Process the queries and reply to the recursor via TCP.

4. Log the server activities on the standard output.

5. Parse commands sent from the user via TCP and update the server.


2. Read and validate a domain in the standard input.

3. Query a chain of DNS servers, and receive responses.

4. Resolve the domain and output the response in the standard output.
