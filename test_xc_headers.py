import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    "https://xeno-canto.org/api/2/recordings?query=Anas+platyrhynchos",
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        print(response.read().decode()[:200])
except Exception as e:
    print("Error:", e)
