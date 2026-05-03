import os
import re

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove base script
html = re.sub(r'<script>\s*\(function \(\) \{.*?\<\/script>\s*', '', html, flags=re.DOTALL)

# Replace absolute paths with relative paths
html = re.sub(r'href="/(.*?)/"', r'href="./\1/"', html)
html = re.sub(r'href="/"', r'href="./"', html)

# Accessibility for slideshow buttons
html = html.replace('<a class="prev" onclick="plusSlides(-1)">&#10094;</a>', '<button class="prev" onclick="plusSlides(-1)" aria-label="Previous slide">&#10094;</button>')
html = html.replace('<a class="next" onclick="plusSlides(1)">&#10095;</a>', '<button class="next" onclick="plusSlides(1)" aria-label="Next slide">&#10095;</button>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace(
    "background: url('https://www.nps.gov/articles/000/images/GGO_spread-wings_Mel-Clements.jpg');",
    "background: url('hero-owl.jpg');"
)

old_cta = """.cta-button {
    background-color: var(--secondary-green);
    color: var(--primary-green);
    padding: 12px 30px;
    text-decoration: none;
    font-weight: bold;
    border-radius: 25px;
    transition: background 0.3s;
    display: inline-block;
}
.cta-button:hover { background-color: var(--text-light); }"""

new_cta = """.cta-button {
    background-color: var(--secondary-green);
    color: var(--primary-green);
    padding: 12px 30px;
    text-decoration: none;
    font-weight: bold;
    border-radius: 25px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    display: inline-block;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.cta-button:hover {
    background-color: var(--text-light);
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.15);
}"""

css = css.replace(old_cta, new_cta)

# Replace the previous/next button styling to apply to buttons
css = css.replace('.prev, .next {', '.prev, .next {\n    border: none;')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Refactored index.html and style.css successfully.")

# Optimize images if PIL is available
try:
    from PIL import Image
    for img_name in ['winakwa.jpg', 'StVital.jpg', 'Kildonan.jpg']:
        if os.path.exists(img_name):
            with Image.open(img_name) as img:
                # Resize if too large
                if img.width > 1200:
                    img.thumbnail((1200, 1200))
                # Save as webp
                new_name = img_name.rsplit('.', 1)[0] + '.webp'
                img.save(new_name, 'WEBP', quality=80)
                print(f"Optimized {img_name} -> {new_name}")
                
                # Update HTML to use webp
                with open('index.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                html_content = html_content.replace(img_name, new_name)
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)

except ImportError:
    print("PIL not installed. Skipping image optimization.")
