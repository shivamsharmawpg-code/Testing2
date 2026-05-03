import os
import shutil
import re
import glob

root_dir = r"c:\Users\aweso\Downloads\Testing2"

# 1. Create directories
assets_dir = os.path.join(root_dir, 'assets')
css_dir = os.path.join(assets_dir, 'css')
js_dir = os.path.join(assets_dir, 'js')
img_dir = os.path.join(assets_dir, 'images')
tools_dir = os.path.join(root_dir, 'tools')

for d in [css_dir, js_dir, img_dir, tools_dir]:
    os.makedirs(d, exist_ok=True)

# 2. Move files
def move_file(src_name, dest_folder):
    src = os.path.join(root_dir, src_name)
    if os.path.exists(src):
        shutil.move(src, os.path.join(dest_folder, src_name))

move_file('style.css', css_dir)
move_file('script.js', js_dir)
move_file('birds.js', js_dir)

# Move images
images = glob.glob(os.path.join(root_dir, '*.png')) + \
         glob.glob(os.path.join(root_dir, '*.jpg')) + \
         glob.glob(os.path.join(root_dir, '*.webp'))

for img in images:
    shutil.move(img, os.path.join(img_dir, os.path.basename(img)))

# Move tools
py_scripts = glob.glob(os.path.join(root_dir, '*.py'))
for py in py_scripts:
    if os.path.basename(py) != 'organize_repo.py':
        shutil.move(py, os.path.join(tools_dir, os.path.basename(py)))

# 3. Update HTML files
for root, dirs, files in os.walk(root_dir):
    # Skip assets and tools folders
    if 'assets' in root or 'tools' in root or '.git' in root:
        continue
        
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            is_root = os.path.abspath(filepath) == os.path.join(os.path.abspath(root_dir), 'index.html')
            prefix = "./assets/" if is_root else "../assets/"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Update CSS
            html = re.sub(r'href="\.\.?/style\.css"', f'href="{prefix}css/style.css"', html)
            html = html.replace('href="style.css"', f'href="{prefix}css/style.css"')
            
            # Update JS
            html = re.sub(r'src="\.\.?/script\.js"', f'src="{prefix}js/script.js"', html)
            html = html.replace('src="script.js"', f'src="{prefix}js/script.js"')
            
            html = re.sub(r'src="\.\.?/birds\.js"', f'src="{prefix}js/birds.js"', html)
            html = html.replace('src="birds.js"', f'src="{prefix}js/birds.js"')
            
            # Update Images
            html = re.sub(r'src="\.\.?/(.*?\.(png|jpg|webp))"', f'src="{prefix}images/\\1"', html)
            html = re.sub(r'src="([^/]*?\.(png|jpg|webp))"', f'src="{prefix}images/\\1"', html)
            
            # Special case for meta tags
            meta_prefix = "https://beakaboo.ca/assets/images/"
            html = re.sub(r'content="https://beakaboo\.ca/logo\.png"', f'content="{meta_prefix}logo.png"', html)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

# 4. Update CSS (background image)
css_path = os.path.join(css_dir, 'style.css')
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    css = css.replace("url('hero-owl.jpg')", "url('../images/hero-owl.jpg')")
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)

# 5. Update JS (logo in script.js)
js_path = os.path.join(js_dir, 'script.js')
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
    js_content = js_content.replace("'../logo.png'", "'../assets/images/logo.png'")
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

# 6. Update sw.js
sw_path = os.path.join(root_dir, 'sw.js')
if os.path.exists(sw_path):
    with open(sw_path, 'r', encoding='utf-8') as f:
        sw = f.read()
    
    # Update cache paths
    sw = sw.replace("'./style.css'", "'./assets/css/style.css'")
    sw = sw.replace("'./script.js'", "'./assets/js/script.js'")
    sw = sw.replace("'./birds.js'", "'./assets/js/birds.js'")
    sw = sw.replace("'./logo.png'", "'./assets/images/logo.png'")
    
    with open(sw_path, 'w', encoding='utf-8') as f:
        f.write(sw)

print("Project reorganized successfully.")
