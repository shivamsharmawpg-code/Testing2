import urllib.request
import json
import urllib.parse
import os

def get_wikipedia_audio(sci_name):
    headers = {'User-Agent': 'Mozilla/5.0'}
    # Search for files related to the scientific name
    query = f"File:{sci_name}"
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        for result in data['query']['search']:
            title = result['title']
            if title.lower().endswith(('.ogg', '.mp3', '.wav')):
                print(f"Found candidate: {title}")
                # Get the file URL
                info_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
                req_info = urllib.request.Request(info_url, headers=headers)
                with urllib.request.urlopen(req_info) as res_info:
                    info_data = json.loads(res_info.read().decode())
                    pages = info_data['query']['pages']
                    for p_id in pages:
                        if 'imageinfo' in pages[p_id]:
                            return pages[p_id]['imageinfo'][0]['url']
    except Exception as e:
        print(f"Error: {e}")
    return None

sci_name = "Poecile atricapillus"
audio_url = get_wikipedia_audio(sci_name)
if audio_url:
    print(f"Downloading from {audio_url}")
    req = urllib.request.Request(audio_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        ext = audio_url.split('.')[-1]
        with open(f"test.{ext}", "wb") as f:
            f.write(response.read())
    print("Success")
else:
    print("No audio found on Wikipedia.")
