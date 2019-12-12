from ip2geotools.databases.noncommercial import DbIpCity
response = DbIpCity.get('116.202.1.22', api_key='free')
print(response)