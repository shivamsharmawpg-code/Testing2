import urllib.request

try:
    req = urllib.request.Request(
        "https://xeno-canto.org/api/3/recordings?query=Mallard&key=demo",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        print(response.read().decode()[:200])
except Exception as e:
    print("Error:", e)
