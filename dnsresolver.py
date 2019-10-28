# import dns.query
# import dns.zone

# z = dns.zone.from_xfr(dns.query.xfr('ahmetcankaraagacli.com', 'zonetransfer.me'))
# names = z.nodes.keys()
# for n in names:
#     print (z[n].to_text(n))


import dns.resolver

domain = 'ahmetcankaraagacli.com'
nameservers = dns.resolver.query(domain,'NS')
for data in nameservers:
	print (data)