import requests
url = 'https://httpbin.org/ip'
proxies = {
    "https": 'http://31.128.83.79:8080',
    "https": 'http://94.51.83.2:8080',
    "http": 'http://157.245.57.147:8080',
}
response = requests.get(url,proxies=proxies)
print(response.json())