import random
import dns.resolver
import json
from datetime import datetime, timedelta

class DNSRecord:
    def __init__(self, name, record_type, data):
        self.name = name
        self.type = record_type
        self.data = data

    def __str__(self):
        return f"{self.type}: {self.data}"

class DNSServer:
    CACHE_FILE = "dns_record.txt"

    def __init__(self, name, resolver):
        self.name = name
        self.resolver = resolver
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.CACHE_FILE, "r") as file:
                cache_data = json.load(file)
                return {record['query']: record['data'] for record in cache_data}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_cache(self):
        cache_data = [{'query': query, 'data': data} for query, data in self.cache.items()]
        with open(self.CACHE_FILE, "w") as file:
            json.dump(cache_data, file)

    def process_query(self, query_id, query, client_ip, recursive=True):
        if query in self.cache:
            print(f"{self.name} using cached result for {query} locally")
            reply = self.cache[query]
            locally_resolved = True
        else:
            reply = self.lookup_dns_records(query)

            if recursive:
                print(f"{self.name} using recursive approach for {query}")
                reply, hops = self.forward_query(query_id, query, client_ip, reply)
                reply += f"\n-- HOPS --\n{hops}"
                locally_resolved = False

            self.cache[query] = reply
            self.save_cache()

        self.send_reply(query_id, reply, client_ip, locally_resolved)

    def forward_query(self, query_id, query, client_ip, reply):
        hops = ""
        try:
            # Include multiple record types in the resolve function
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
                try:
                    answers = self.resolver.resolve(query, record_type)
                    reply += f"{query}/{record_type}: {', '.join(str(answer) for answer in answers)}\n"
                    hops += f"{self.name}/{record_type}: {', '.join(str(answer) for answer in answers)}\n"
                except dns.resolver.NoAnswer:
                    reply += f"{query}/{record_type}: No answer\n"
                    hops += f"{self.name}/{record_type}: No answer\n"
        except dns.resolver.NXDOMAIN:
            reply = f"ERROR: No DNS record for '{query}'"

        return reply, hops

    def lookup_dns_records(self, query):
        # Placeholder method to look up DNS records for the query
        # This should be extended based on your actual DNS record list
        return f"ERROR: No DNS record for '{query}'"

    def send_reply(self, query_id, reply, client_ip, locally_resolved):
        resolved_location = "locally" if locally_resolved else "recursively"
        print(f"{self.name} replying to {client_ip} (Query ID: {query_id}): Resolved {resolved_location}\n{reply}")

# Instantiate DNS resolver with specific DNS server
root_resolver = dns.resolver.Resolver()
root_resolver.nameservers = ['8.8.8.8']

tld_resolver = dns.resolver.Resolver()
tld_resolver.nameservers = ['8.8.4.4']

auth_resolver = dns.resolver.Resolver()
auth_resolver.nameservers = ['1.1.1.1']

# Instantiate servers with respective resolvers
root_server = DNSServer('RootServer', root_resolver)
tld_server = DNSServer('TLDServer', tld_resolver)
auth_server = DNSServer('AuthoritativeServer', auth_resolver)

# Take user input for the domain to query
user_query = input("Enter the domain to query: ")

# Simulate a DNS query for the user-provided domain
query_id = random.randint(1, 65535)  # Generate a random query ID
root_server.process_query(query_id, user_query, 'client_ip')
