import os
import re

root_dir = r"c:\Users\aweso\Downloads\Testing2"

# 1. Create manifest.json
manifest_content = """{
  "name": "Beak-a-boo Bird Catalogue",
  "short_name": "Beak-a-boo",
  "description": "Manitoba family birdwatching field guide",
  "start_url": "./",
  "display": "standalone",
  "background_color": "#f4f7f6",
  "theme_color": "#2c5f2d",
  "icons": [
    {
      "src": "logo.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "logo.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""
with open(os.path.join(root_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
    f.write(manifest_content)

# 2. Create sw.js
sw_content = """const CACHE_NAME = 'beak-a-boo-v1';
const ASSETS = [
    './',
    './index.html',
    './style.css',
    './script.js',
    './birds.js',
    './logo.png',
    './catalogue/index.html',
    './trails/index.html',
    './about/index.html',
    './quickstart/index.html',
    './certificates/index.html'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(cache => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
        .then(response => {
            return response || fetch(event.request);
        })
    );
});
"""
with open(os.path.join(root_dir, 'sw.js'), 'w', encoding='utf-8') as f:
    f.write(sw_content)

# 3. Update style.css
css_additions = """
/* --- 5x Upgrade Additions --- */
/* Bird Journal / Spotted State */
.spotted-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #FFD700;
    color: #333;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: none;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    z-index: 10;
}
.bird-card.spotted .spotted-badge {
    display: flex;
}
.bird-card.spotted {
    border: 2px solid #FFD700;
    box-shadow: 0 8px 24px rgba(255, 215, 0, 0.3);
}
.is-spotted {
    background-color: #FFD700 !important;
    color: #333 !important;
}

/* Audio Button */
.audio-btn {
    background: var(--primary-green);
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    margin-left: 10px;
}
.bird-modal__header-flex {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}
"""

with open(os.path.join(root_dir, 'style.css'), 'a', encoding='utf-8') as f:
    f.write(css_additions)


# 4. Modify all HTML files
gsap_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>'
sw_script = """<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js').then(function(registration) {
      console.log('ServiceWorker registration successful');
    });
  });
}
</script>"""

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'index.html':
            filepath = os.path.join(root, file)
            is_root = os.path.abspath(filepath) == os.path.join(os.path.abspath(root_dir), 'index.html')
            
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()

            # Add manifest and font updates
            if '<link rel="manifest"' not in html:
                manifest_path = "./manifest.json" if is_root else "../manifest.json"
                html = html.replace('</head>', f'    <link rel="manifest" href="{manifest_path}">\n</head>')

            # Add SW and GSAP scripts
            if 'gsap.min.js' not in html:
                html = html.replace('</body>', f'    {gsap_script}\n    {sw_script}\n</body>')

            # Catalogue specific update
            if 'catalogue' in filepath:
                if 'spotted-progress' not in html:
                    html = html.replace('<div class="search-bar">', '<p id="spotted-progress" class="section-subtitle" style="font-weight:bold;"></p>\n            <div class="search-bar">')

            # Trails specific update (Leaflet)
            if 'trails' in filepath:
                if 'leaflet' not in html:
                    leaflet_css = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />'
                    leaflet_js = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
                    html = html.replace('</head>', f'    {leaflet_css}\n</head>')
                    html = html.replace('</body>', f'    {leaflet_js}\n</body>')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

print("Applied 5x Upgrades: PWA, JS formatting, GSAP/Leaflet imports, and UI layout fixes.")
