import os
import re

root_dir = r"c:\Users\aweso\Downloads\Testing2"

# 1. Update robots.txt
robots_content = """User-agent: *
Allow: /
Disallow: /tools/
Disallow: /assets/js/

Sitemap: https://beakaboo.ca/sitemap.xml
"""
with open(os.path.join(root_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots_content)

# 2. Update sitemap.xml
sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://beakaboo.ca/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://beakaboo.ca/catalogue/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://beakaboo.ca/trails/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://beakaboo.ca/about/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://beakaboo.ca/quickstart/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://beakaboo.ca/certificates/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
"""
with open(os.path.join(root_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

# 3. Create llms.txt (Standard for AI crawlers)
llms_content = """# Beak-a-boo: Manitoba Birdwatching Field Guide
URL: https://beakaboo.ca
Description: A family-friendly field guide for birdwatching in Manitoba, Canada. Created by a Junior Achievement company from Windsor Park Collegiate.

## Site Structure
- / : Home page
- /catalogue/ : Database of 40 Manitoba bird species with facts, audio calls, and a memory checklist.
- /trails/ : Interactive Leaflet maps of birdwatching trails in Winnipeg.
- /quickstart/ : A beginner's guide to birdwatching.
- /certificates/ : A tool to generate custom birdwatching certificates.
- /about/ : Information about the student founders.

## Technology
- Vanilla HTML/CSS/JS
- Progressive Web App (PWA) with offline capabilities
- GreenSock Animation Platform (GSAP)
- Leaflet interactive maps
"""
with open(os.path.join(root_dir, 'llms.txt'), 'w', encoding='utf-8') as f:
    f.write(llms_content)

# 4. Add rich SEO tags to HTML files
favicons = """    <link rel="icon" type="image/png" href="{prefix}assets/images/logo.png">
    <link rel="apple-touch-icon" href="{prefix}assets/images/logo.png">"""

json_ld_website = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Beak-a-boo",
      "url": "https://beakaboo.ca/",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://beakaboo.ca/catalogue/?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
    </script>"""

for root, dirs, files in os.walk(root_dir):
    if 'assets' in root or 'tools' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            is_root = os.path.abspath(filepath) == os.path.join(os.path.abspath(root_dir), 'index.html')
            prefix = "./" if is_root else "../"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()

            # Add Favicons
            if '<link rel="apple-touch-icon"' not in html:
                html = html.replace('</head>', favicons.format(prefix=prefix) + '\n</head>')

            # Add WebSite JSON-LD to index.html ONLY
            if is_root and '"@type": "WebSite"' not in html:
                html = html.replace('</head>', json_ld_website + '\n</head>')
                
            # Ensure og:image points exactly to the absolute URL
            html = re.sub(r'content="https://beakaboo\.ca/.*?logo\.png"', 'content="https://beakaboo.ca/assets/images/logo.png"', html)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

print("SEO optimizations applied successfully.")
