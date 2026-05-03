import os
import re
import json
import urllib.request
import urllib.parse
import time

# Configuration
BIRDS_JS_PATH = r"c:\Users\aweso\Downloads\Testing2\assets\js\birds.js"
AUDIO_DIR = r"c:\Users\aweso\Downloads\Testing2\assets\audio"

def get_birds_from_js():
    with open(BIRDS_JS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the array content
    match = re.search(r'const birdsData = (\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Could not find birdsData in JS file.")
        return []
    
    # Clean up the JS object to make it valid JSON (remove trailing commas, etc.)
    # This is a bit hacky but works for simple JS objects
    js_data = match.group(1)
    # Remove trailing commas
    js_data = re.sub(r',\s*([\]}])', r'\1', js_data)
    # Ensure keys are quoted (if they aren't already)
    js_data = re.sub(r'(\w+):', r'"\1":', js_data)
    
    try:
        return json.loads(js_data)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        # Fallback: simple regex extraction if JSON fails
        birds = []
        bird_blocks = re.findall(r'\{.*?\}', match.group(1), re.DOTALL)
        for block in bird_blocks:
            bird = {}
            for key in ['id', 'Common_Name', 'Scientific_Name']:
                k_match = re.search(rf'{key}:\s*["\']?(.*?)["\']?,', block)
                if k_match:
                    bird[key] = k_match.group(1)
            if bird:
                birds.append(bird)
        return birds

def download_bird_call(bird):
    name = bird['Common_Name']
    sci_name = bird['Scientific_Name']
    bird_id = bird['id']
    target_file = os.path.join(AUDIO_DIR, f"{bird_id}.mp3")
    
    if os.path.exists(target_file):
        print(f"Skipping {name}, already exists.")
        return True

    print(f"Searching for {name} ({sci_name})...")
    
    # Search iNaturalist (reliable, no key required for low volume)
    url = f"https://api.inaturalist.org/v1/observations?taxon_name={urllib.parse.quote(sci_name)}&sounds=true&order_by=votes&per_page=1"
    
    try:
        headers = {'User-Agent': 'BeakABoo/1.0 (Educational Project)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        if data['results'] and data['results'][0]['sounds']:
            sound = data['results'][0]['sounds'][0]
            audio_url = sound['file_url']
            
            # iNaturalist often provides MP3s
            print(f"Downloading {name} call from {audio_url}...")
            req = urllib.request.Request(audio_url, headers=headers)
            with urllib.request.urlopen(req) as response:
                with open(target_file, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"Successfully saved to {bird_id}.mp3")
            return True
        else:
            print(f"Could not find any recordings for {name} on iNaturalist.")
    except Exception as e:
        print(f"Error downloading {name}: {e}")
    
    return False

def main():
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        
    birds = get_birds_from_js()
    print(f"Found {len(birds)} birds in catalogue.")
    
    success_count = 0
    for bird in birds:
        if download_bird_call(bird):
            success_count += 1
            # Rate limiting to be polite
            time.sleep(1)
            
    print(f"Finished! Downloaded {success_count} bird calls.")

if __name__ == "__main__":
    main()
