import os
import re

root_dir = r"c:\Users\aweso\Downloads\Testing2"
assets_dir = os.path.join(root_dir, 'assets')
js_path = os.path.join(assets_dir, 'js', 'script.js')

# 1. Update JS logic
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

lang_logic = """
// Custom Google Translate Cookie Toggle
function toggleLangCookie() {
    const isFrench = document.cookie.includes('googtrans=/en/fr');
    if (isFrench) {
        document.cookie = "googtrans=/en/en; path=/";
        document.cookie = "googtrans=/en/en; path=/; domain=" + window.location.hostname;
    } else {
        document.cookie = "googtrans=/en/fr; path=/";
        document.cookie = "googtrans=/en/fr; path=/; domain=" + window.location.hostname;
    }
    window.location.reload();
}

document.addEventListener('DOMContentLoaded', () => {
    const langBtn = document.getElementById('lang-btn');
    if (langBtn) {
        if (document.cookie.includes('googtrans=/en/fr')) {
            langBtn.innerHTML = 'FR <i class="fa-solid fa-language"></i>';
        } else {
            langBtn.innerHTML = 'EN <i class="fa-solid fa-language"></i>';
        }
    }
});
"""

if "function toggleLangCookie()" not in js_content:
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write("\n" + lang_logic)


# 2. Update all HTML files
google_snippet_old = r'<div id="google_translate_element" style="margin-left: 15px;"></div>.*?<script type="text/javascript" src="https://translate\.google\.com/translate_a/element\.js\?cb=googleTranslateElementInit"></script>'

new_snippet = """
        <button onclick="toggleLangCookie()" class="lang-toggle" id="lang-btn" aria-label="Toggle Language" style="margin-left: 15px; order: 4;">EN/FR</button>
        <div id="google_translate_element" style="display:none;"></div>
        <script type="text/javascript">
            function googleTranslateElementInit() {
                new google.translate.TranslateElement({pageLanguage: 'en', includedLanguages: 'en,fr', autoDisplay: false}, 'google_translate_element');
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

            # Replace the old visible widget with the hidden one + our custom button
            html = re.sub(google_snippet_old, new_snippet, html, flags=re.DOTALL)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

print("Fixed translation UI.")
