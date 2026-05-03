import urllib.request
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
sci_name = "Poecile atricapillus"
query = urllib.parse.quote(sci_name)
url = f"https://xeno-canto.org/api/3/recordings?query={query}"

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print(f"Found {len(data['recordings'])} recordings")
    if data['recordings']:
        rec = data['recordings'][0]
        audio_url = rec['file']
        if audio_url.startswith('//'):
            audio_url = 'https:' + audio_url
        print(f"Downloading from {audio_url}")
        req = urllib.request.Request(audio_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open("test.mp3", "wb") as f:
                f.write(response.read())
        print("Success")
