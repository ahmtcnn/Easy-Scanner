import requests

response = requests.get('http://googdfasfle.com')
assert response.status_code < 400,