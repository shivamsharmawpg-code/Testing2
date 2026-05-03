import os
import re

root_dir = r"c:\Users\aweso\Downloads\Testing2"
assets_dir = os.path.join(root_dir, 'assets')
js_path = os.path.join(assets_dir, 'js', 'script.js')
css_path = os.path.join(assets_dir, 'css', 'style.css')
index_html = os.path.join(root_dir, 'index.html')

# 1. Remove Trade Fairs from index.html
with open(index_html, 'r', encoding='utf-8') as f:
    html = f.read()

# Regex to find trade fair section
pattern = r'<section class="content-section trade-fair-section.*?</section>'
html = re.sub(pattern, '', html, flags=re.DOTALL)

with open(index_html, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css to center search and style Google Translate
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

css_fixes = """
/* --- Fixes --- */
#global-search-input {
    margin: 0 auto; /* Center it */
    min-width: 250px;
    padding: 8px 15px;
    border-radius: 20px;
    border: 1px solid #ccc;
    font-family: var(--font-main);
}
header {
    flex-wrap: wrap;
}
/* Google Translate styling */
#google_translate_element select {
    background: var(--bg-white);
    color: var(--primary-green);
    border: 1px solid var(--primary-green);
    border-radius: 4px;
    padding: 4px;
    font-weight: bold;
}
.goog-te-banner-frame { display: none !important; }
body { top: 0px !important; }
"""

if "/* --- Fixes --- */" not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write("\n" + css_fixes)


# 3. Update script.js (Remove hacky language toggle, fix search bar placement)
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Remove hacky language toggle functions
js_content = re.sub(r'const translations = \{[\s\S]*?function applyLanguage\(lang\) \{[\s\S]*?\}\n\}', '', js_content)

# Update search placement
js_content = js_content.replace("if (nav) nav.appendChild(searchInput);", "const header = document.querySelector('header');\n    if (header) { const logo = document.querySelector('.logo'); logo.insertAdjacentElement('afterend', searchInput); }")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)


# 4. Update all HTML files (Replace EN/FR button with Google Translate)
google_translate_html = """
        <div id="google_translate_element" style="margin-left: 15px;"></div>
        <script type="text/javascript">
            function googleTranslateElementInit() {
                new google.translate.TranslateElement({pageLanguage: 'en', includedLanguages: 'en,fr', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}, 'google_translate_element');
            }
        </script>
        <script type="text/javascript" src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""

for root, dirs, files in os.walk(root_dir):
    if 'assets' in root or 'tools' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()

            # Remove old lang toggle
            html = html.replace('<button onclick="toggleLanguage()" class="lang-toggle">EN/FR</button>', '')
            html = html.replace('<button onclick="toggleLanguage()" class="lang-toggle">EN/FR</button>\n', '')

            # Inject Google Translate into Header
            if 'google_translate_element' not in html:
                # Insert before the theme toggle
                html = html.replace('<button id="theme-toggle"', google_translate_html + '\n        <button id="theme-toggle"')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

print("Applied fixes: Removed Trade Fairs, centered search, added robust Google Translate for the entire site.")
