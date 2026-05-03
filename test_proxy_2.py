import urllib.request
import json
import urllib.parse

target_url = "https://xeno-canto.org/api/2/recordings?query=" + urllib.parse.quote("Mallard")
proxy_url = "https://api.allorigins.win/get?url=" + urllib.parse.quote(target_url)

req = urllib.request.Request(proxy_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if data.get('contents'):
            xc_data = json.loads(data['contents'])
            print(f"Found {xc_data.get('numRecordings', 0)} recordings")
            if xc_data.get('recordings'):
                print("First recording file:", xc_data['recordings'][0].get('file'))
except Exception as e:
    print("Error:", e)
