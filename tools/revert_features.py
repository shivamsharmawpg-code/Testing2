import os
import re

root_dir = r"c:\Users\aweso\Downloads\Testing2"
assets_dir = os.path.join(root_dir, 'assets')
js_path = os.path.join(assets_dir, 'js', 'script.js')
css_path = os.path.join(assets_dir, 'css', 'style.css')

# 1. Update JS
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Remove Dark Mode
js_content = re.sub(r'// 1\. Dark Mode\s*function setupTheme\(\) \{[\s\S]*?(?=// 2\. Native Web Share API)', '', js_content)
js_content = re.sub(r'setupTheme\(\);\s*', '', js_content)

# Remove Custom Google Translate Logic
js_content = re.sub(r'// Custom Google Translate Cookie Toggle\s*function toggleLangCookie\(\) \{[\s\S]*?(?=document\.addEventListener)', '', js_content)
js_content = re.sub(r'const langBtn = document\.getElementById\(\'lang-btn\'\);[\s\S]*?\}\s*\}', '', js_content)

# Clean up empty DOMContentLoaded if it has nothing else
js_content = re.sub(r'document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*\}\);', '', js_content)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)


# 2. Update CSS
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Remove Dark Mode CSS
css = re.sub(r'/\* Dark Mode Theme \*/[\s\S]*?/\* Dark Mode Toggle Button \*/[\s\S]*?(?=/\* Print Optimization \*/)', '', css)

# Remove Language Toggle CSS
css = re.sub(r'/\* Language Toggle \*/[\s\S]*?(?=/\* AI Identifier \*/)', '', css)

# Remove Google Translate CSS
css = re.sub(r'/\* Google Translate styling \*/[\s\S]*?(?=\Z|\n\n)', '', css)
css = re.sub(r'\.goog-te-banner-frame \{ display: none !important; \}\nbody \{ top: 0px !important; \}', '', css)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)


# 3. Update HTML Files
translate_pattern = r'<button onclick="toggleLangCookie\(\)".*?</button>\s*<div id="google_translate_element".*?</script>\s*<script type="text/javascript" src="https://translate\.google\.com/translate_a/element\.js\?cb=googleTranslateElementInit"></script>'
theme_pattern = r'<button id="theme-toggle".*?</button>'
old_translate_pattern = r'<div id="google_translate_element".*?</script>\s*<script type="text/javascript" src="https://translate\.google\.com/translate_a/element\.js\?cb=googleTranslateElementInit"></script>'


for root, dirs, files in os.walk(root_dir):
    if 'assets' in root or 'tools' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()

            # Strip Translation completely
            html = re.sub(translate_pattern, '', html, flags=re.DOTALL)
            html = re.sub(old_translate_pattern, '', html, flags=re.DOTALL)
            
            # Strip Theme Toggle completely
            html = re.sub(theme_pattern, '', html, flags=re.DOTALL)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

print("Successfully purged all translation logic, Google Translate widgets, and Dark Mode from JS, CSS, and HTML files.")
