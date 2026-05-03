import os

filepath = r"c:\Users\aweso\Downloads\Testing2\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

gsap_script = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            if (typeof gsap !== 'undefined') {
                gsap.from(".hero-content", { duration: 1.2, y: 50, opacity: 0, ease: "power4.out", delay: 0.2 });
                gsap.from(".hero-content h1", { duration: 1, y: 30, opacity: 0, ease: "power3.out", delay: 0.5 });
                gsap.from(".hero-content p", { duration: 1, y: 20, opacity: 0, ease: "power3.out", delay: 0.7 });
                gsap.from(".hero-actions a", { duration: 0.8, y: 20, opacity: 0, stagger: 0.15, ease: "back.out(1.7)", delay: 0.9 });
                
                // Parallax on hero image
                gsap.to(".hero", {
                    backgroundPosition: `50% ${-50}px`,
                    ease: "none",
                    scrollTrigger: {
                        trigger: ".hero",
                        start: "top top",
                        end: "bottom top",
                        scrub: true
                    }
                });
            }
        });
    </script>
"""

# Make sure we don't duplicate
if 'gsap.from(".hero-content"' not in html:
    html = html.replace('</body>', gsap_script + '\n</body>')
    # Add scrolltrigger plugin since we use it
    scrolltrigger_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>'
    html = html.replace('gsap.min.js"></script>', 'gsap.min.js"></script>\n    ' + scrolltrigger_script)
    
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated GSAP animations on homepage")
