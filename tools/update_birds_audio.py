import json
import re

mapping = {"1": "mp3", "2": "wav", "3": "m4a", "4": "m4a", "5": "mp3", "6": "wav", "7": "m4a", "8": "mp3", "9": "m4a", "10": "m4a", "11": "m4a", "12": "wav", "13": "wav", "14": "m4a", "15": "m4a", "16": "m4a", "17": "m4a", "18": "m4a", "19": "mp3", "20": "wav", "21": "m4a", "22": "m4a", "23": "m4a", "24": "m4a", "25": "wav", "26": "mp3", "27": "m4a", "28": "wav", "29": "wav", "30": "wav", "31": "wav", "32": "wav", "33": "wav", "34": "m4a", "35": "m4a", "37": "mp3", "38": "wav", "40": "wav"}

path = r"c:\Users\aweso\Downloads\Testing2\assets\js\birds.js"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def add_ext(match):
    block = match.group(0)
    id_match = re.search(r'id:\s*(\d+)', block)
    if id_match:
        b_id = id_match.group(1)
        ext = mapping.get(b_id)
        if ext:
            if 'audioExt' not in block:
                return block.rstrip().rstrip('}') + f',\n    audioExt: "{ext}"\n  }}'
    return block

new_content = re.sub(r'\{[^{}]*?\}', add_ext, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated birds.js with audio extensions.")
