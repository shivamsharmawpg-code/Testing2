import os

filepath = r"c:\Users\aweso\Downloads\Testing2\trails\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Add the Map container at the top of the section
map_html = """
            <div id="trails-main-map" style="height: 400px; width: 100%; border-radius: 16px; margin-bottom: 30px; border: 1px solid rgba(44, 95, 45, 0.15); box-shadow: 0 12px 24px rgba(44, 95, 45, 0.12); z-index: 1;"></div>
"""
html = html.replace('<div class="trails-card">', map_html + '<div class="trails-card" style="display:none;">') # Hide the big card to feature the map

# Add Leaflet init script before </body>
leaflet_init = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize Leaflet map
            const map = L.map('trails-main-map').setView([49.85, -97.15], 11);

            L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: 'abcd',
                maxZoom: 20
            }).addTo(map);

            const trailLocations = [
                { name: "Seine River Greenway", lat: 49.8309, lng: -97.0861 },
                { name: "Harte Trail", lat: 49.8445, lng: -97.2603 },
                { name: "Assiniboine Forest", lat: 49.8544, lng: -97.2451 },
                { name: "Bois-des-Esprits", lat: 49.8228, lng: -97.0820 },
                { name: "Niakwa Trail", lat: 49.8579, lng: -97.1023 },
                { name: "North Winnipeg Parkway", lat: 49.9016, lng: -97.1285 },
                { name: "Bunn's Creek", lat: 49.9486, lng: -97.0607 },
                { name: "St. Vital Park", lat: 49.8294, lng: -97.1479 },
                { name: "Little Mountain Park", lat: 49.9547, lng: -97.2542 },
                { name: "Transcona Bioreserve", lat: 49.9111, lng: -97.0130 },
                { name: "Sturgeon Creek Park", lat: 49.8885, lng: -97.2943 },
                { name: "Kings Park", lat: 49.7989, lng: -97.1248 },
                { name: "FortWhyte Alive", lat: 49.8204, lng: -97.2250 }
            ];

            const customIcon = L.divIcon({
                className: 'custom-pin',
                html: '<i class="fa-solid fa-location-dot" style="color: #2c5f2d; font-size: 24px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);"></i>',
                iconSize: [24, 24],
                iconAnchor: [12, 24]
            });

            trailLocations.forEach(loc => {
                L.marker([loc.lat, loc.lng], {icon: customIcon}).addTo(map)
                    .bindPopup(`<b>${loc.name}</b><br>Great for birdwatching.`);
            });
            
            // GSAP Animations
            if (typeof gsap !== 'undefined') {
                gsap.from("#trails-main-map", { duration: 1, y: 50, opacity: 0, ease: "power3.out", delay: 0.2 });
                gsap.from(".trail-mini-card", { duration: 0.8, y: 30, opacity: 0, stagger: 0.1, ease: "back.out(1.7)", delay: 0.5 });
            }
        });
    </script>
"""
if 'L.map(' not in html:
    html = html.replace('</body>', leaflet_init + '\n</body>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated trails map with Leaflet and GSAP")
