import requests
params = {'apikey': '0e800cf660c8cb0108547968241e6bf3108119b45997a67273619a916dcf021a', 'resource': 'b81f64818bb0711e17a630aacd99c5a8'}
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,  ConorSherman"
  }
response = requests.post('https://www.virustotal.com/vtapi/v2/file/rescan',
 params=params)
json_response = response.json()
