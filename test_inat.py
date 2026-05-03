import urllib.request
import json
import urllib.parse
import os

def get_inaturalist_audio(sci_name):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://api.inaturalist.org/v1/observations?taxon_name={urllib.parse.quote(sci_name)}&sounds=true&order_by=votes&per_page=1"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        if data['results']:
            obs = data['results'][0]
            if obs['sounds']:
                sound = obs['sounds'][0]
                # Try to get the mp3/wav
                return sound['file_url']
    except Exception as e:
        print(f"Error: {e}")
    return None

sci_name = "Poecile atricapillus"
audio_url = get_inaturalist_audio(sci_name)
if audio_url:
    print(f"Found audio: {audio_url}")
else:
    print("No audio found on iNaturalist.")
