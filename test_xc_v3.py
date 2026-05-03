import urllib.request
import json
import urllib.parse

url = "https://xeno-canto.org/api/3/recordings?query=" + urllib.parse.quote("Anas platyrhynchos")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(f"Found {data.get('numRecordings', 0)} recordings")
        if data.get('recordings'):
            print("First recording file:", data['recordings'][0].get('file'))
except Exception as e:
    print("Error:", e)
