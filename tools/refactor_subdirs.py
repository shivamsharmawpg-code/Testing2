import os
import re

root_dir = r"c:\Users\aweso\Downloads\Testing2"

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'index.html':
            filepath = os.path.join(root, file)
            # Skip root index.html as it is already fixed
            if os.path.abspath(filepath) == os.path.join(os.path.abspath(root_dir), 'index.html'):
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()

            # Remove base script
            html = re.sub(r'<script>\s*\(function \(\) \{.*?\<\/script>\s*', '', html, flags=re.DOTALL)

            # Replace absolute paths with relative paths for subdirectories (../)
            html = re.sub(r'href="/(.*?)/"', r'href="../\1/"', html)
            html = re.sub(r'href="/"', r'href="../"', html)
            
            # Fix style and scripts
            html = html.replace('href="style.css"', 'href="../style.css"')
            html = html.replace('src="birds.js"', 'src="../birds.js"')
            html = html.replace('src="script.js"', 'src="../script.js"')
            
            # Fix logo image
            html = html.replace('src="logo.png"', 'src="../logo.png"')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"Fixed paths in {filepath}")
