
import dns.resolver

result = dns.resolver.query('google.com', 'CNAME')
for cnameval in result:
    print (' cname target address:', cnameval.target)
