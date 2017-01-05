'''CODE OUTLINE
1. Open the CSV
2. Extract the HASH into an Array (?)
Loop
3. Check the HASH with VT
4. Store the Respone 'HASH : Verdict"
5. Add the HASH to a 'Checked List'
6. Close loop and print report'''

import requests


params = {'apikey': '-YOUR API KEY HERE-', 'resource': '7657fcb7d772448a6d8504e4b20168b8'}
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,  My Python requests library example client or username"
  }
response = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
  params=params, headers=headers)
json_response = response.json()