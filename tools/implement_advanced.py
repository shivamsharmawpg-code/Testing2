import os
import re

root_dir = r"c:\Users\aweso\Downloads\Testing2"

assets_dir = os.path.join(root_dir, 'assets')
css_path = os.path.join(assets_dir, 'css', 'style.css')
js_path = os.path.join(assets_dir, 'js', 'script.js')

# ---------------------------------------------------------
# 1. CSS UPDATES (Dark Mode, Print Styles, Badges)
# ---------------------------------------------------------
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Add Dark Mode Variables and Print Styles
advanced_css = """
/* --- Advanced Features --- */
/* Dark Mode Theme */
[data-theme="dark"] {
    --primary-green: #a4c99b;
    --secondary-green: #2c5f2d;
    --accent-brown: #d4a373;
    --bg-light: #121212;
    --bg-white: #1e1e1e;
    --text-dark: #e0e0e0;
    --text-light: #121212;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] header {
    background-color: #1a1a1a;
    border-bottom: 1px solid #333;
}
[data-theme="dark"] .trade-fair-card, [data-theme="dark"] .quickstart-step, [data-theme="dark"] .quickstart-card, [data-theme="dark"] .trails-card, [data-theme="dark"] .trail-mini-card, [data-theme="dark"] .bird-card {
    background: #1e1e1e;
    border-color: #333;
    color: #e0e0e0;
}
[data-theme="dark"] .bird-modal__content {
    background: #1e1e1e;
    color: #e0e0e0;
}

/* Dark Mode Toggle Button */
.theme-toggle {
    background: none;
    border: none;
    color: var(--text-light);
    font-size: 1.2rem;
    cursor: pointer;
    margin-left: 15px;
    transition: transform 0.3s;
}
.theme-toggle:hover {
    transform: scale(1.1);
}

/* Print Optimization */
@media print {
    header, footer, .hero, .theme-toggle, .skip-link, .search-bar, .audio-btn {
        display: none !important;
    }
    body {
        background: white !important;
        color: black !important;
    }
    .content-section, .bird-card, .bird-modal__content {
        box-shadow: none !important;
        border: 1px solid #ccc !important;
        page-break-inside: avoid;
    }
    .bird-card img {
        filter: grayscale(100%);
    }
}

/* Share Button */
.share-btn {
    background: var(--accent-brown);
    color: white;
    padding: 8px 16px;
    border-radius: 25px;
    border: none;
    cursor: pointer;
    font-weight: bold;
    margin-left: 10px;
}
.share-btn:hover { background: #b0895b; }

/* Journal Notes */
.journal-notes {
    width: 100%;
    margin-top: 10px;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    background: var(--bg-light);
    color: var(--text-dark);
    font-family: var(--font-main);
    resize: vertical;
}

/* Gamification Badges */
.achievements-container {
    display: flex;
    gap: 15px;
    justify-content: center;
    margin-bottom: 30px;
    flex-wrap: wrap;
}
.achievement-badge {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: #ddd;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0.4;
    filter: grayscale(100%);
    transition: all 0.5s ease;
    text-align: center;
    font-size: 0.7rem;
    font-weight: bold;
}
.achievement-badge.unlocked {
    opacity: 1;
    filter: none;
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #121212;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    transform: scale(1.1);
}
.achievement-badge i {
    font-size: 1.5rem;
    margin-bottom: 5px;
}
"""

if "/* --- Advanced Features --- */" not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write("\n" + advanced_css)


# ---------------------------------------------------------
# 2. JS UPDATES (Gamification, Share API, Dark Mode, Journal)
# ---------------------------------------------------------
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

advanced_js = """
// --- Advanced Features ---

// 1. Dark Mode
function setupTheme() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    toggle.innerHTML = currentTheme === 'dark' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';

    toggle.addEventListener('click', () => {
        let theme = document.documentElement.getAttribute('data-theme');
        let newTheme = theme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        toggle.innerHTML = newTheme === 'dark' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    });
}

// 2. Native Web Share API
function shareBird(birdName, fact) {
    if (navigator.share) {
        navigator.share({
            title: `I spotted a ${birdName}!`,
            text: `Check out this fact: ${fact}`,
            url: window.location.href
        }).catch(console.error);
    } else {
        alert("Sharing is not supported on this device/browser.");
    }
}

// 3. Gamification & Confetti
function checkAchievements(count) {
    const badges = {
        5: 'badge-5',
        10: 'badge-10',
        20: 'badge-20',
        40: 'badge-40'
    };
    
    if (badges[count]) {
        const badgeEl = document.getElementById(badges[count]);
        if (badgeEl && !badgeEl.classList.contains('unlocked')) {
            badgeEl.classList.add('unlocked');
            if (typeof confetti !== 'undefined') {
                confetti({
                    particleCount: 150,
                    spread: 70,
                    origin: { y: 0.6 },
                    colors: ['#FFD700', '#FFA500', '#2c5f2d']
                });
            }
        }
    }
}

// Override toggleSpotted to add Confetti check
const originalToggleSpotted = toggleSpotted;
window.toggleSpotted = function(birdId) {
    let spotted = getSpottedBirds();
    const wasSpotted = spotted.includes(birdId);
    
    // Save Journal Note before toggling if exists
    const noteArea = document.getElementById('journal-note-area');
    if (noteArea) {
        let notes = JSON.parse(localStorage.getItem('birdNotes') || '{}');
        notes[birdId] = noteArea.value;
        localStorage.setItem('birdNotes', JSON.stringify(notes));
    }

    originalToggleSpotted(birdId);
    
    spotted = getSpottedBirds();
    if (!wasSpotted && spotted.includes(birdId)) {
        checkAchievements(spotted.length);
    }
};

// Update Modal to include Share button and Notes
const originalOpenBirdModal = openBirdModal;
window.openBirdModal = function(bird) {
    originalOpenBirdModal(bird);
    
    // Add Share Event
    const shareBtn = document.getElementById('modal-share-btn');
    if (shareBtn) {
        shareBtn.onclick = () => shareBird(bird.Common_Name, bird.Fact);
    }
    
    // Load Notes
    const noteArea = document.getElementById('journal-note-area');
    if (noteArea) {
        let notes = JSON.parse(localStorage.getItem('birdNotes') || '{}');
        noteArea.value = notes[bird.Common_Name] || '';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    setupTheme();
    // Init achievements state
    const spotted = getSpottedBirds();
    [5, 10, 20, 40].forEach(num => {
        if (spotted.length >= num) {
            const el = document.getElementById(`badge-${num}`);
            if (el) el.classList.add('unlocked');
        }
    });
});
"""

if "// --- Advanced Features ---" not in js_content:
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write("\n" + advanced_js)


# ---------------------------------------------------------
# 3. HTML UPDATES
# ---------------------------------------------------------
confetti_script = '<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>'
theme_btn = '<button id="theme-toggle" class="theme-toggle" aria-label="Toggle Dark Mode"><i class="fa-solid fa-moon"></i></button>'

for root, dirs, files in os.walk(root_dir):
    if 'assets' in root or 'tools' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()

            # Add Dark Mode Button to Header
            if 'theme-toggle' not in html:
                # Find the end of nav-links
                html = html.replace('</ul>\n        </nav>', f'</ul>\n        </nav>\n        {theme_btn}')

            # Add Confetti Script
            if 'confetti' not in html:
                html = html.replace('</body>', f'    {confetti_script}\n</body>')

            # Catalogue specific: Add Achievements UI and Modal Updates
            if 'catalogue' in filepath:
                # Add Achievements Bar
                if 'achievements-container' not in html:
                    achievements_html = """
            <div class="achievements-container">
                <div id="badge-5" class="achievement-badge"><i class="fa-solid fa-feather"></i> 5 Birds</div>
                <div id="badge-10" class="achievement-badge"><i class="fa-solid fa-binoculars"></i> 10 Birds</div>
                <div id="badge-20" class="achievement-badge"><i class="fa-solid fa-compass"></i> 20 Birds</div>
                <div id="badge-40" class="achievement-badge"><i class="fa-solid fa-crown"></i> 40 Birds</div>
            </div>
"""
                    html = html.replace('<div class="search-bar">', achievements_html + '<div class="search-bar">')
                
            # Update Modal UI in script.js (Wait, modal HTML is generated in script.js. I need to update script.js modal string)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)


# ---------------------------------------------------------
# 4. Update Modal HTML in script.js
# ---------------------------------------------------------
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

if 'modal-share-btn' not in js_content:
    new_modal_buttons = """<button id="modal-spotted-btn" class="cta-button" style="margin: 0; padding: 8px 16px; font-size: 0.9rem;">Mark as Spotted</button>
                    <button id="modal-share-btn" class="share-btn"><i class="fa-solid fa-share-nodes"></i></button>"""
    js_content = js_content.replace('<button id="modal-spotted-btn" class="cta-button" style="margin: 0; padding: 8px 16px; font-size: 0.9rem;">Mark as Spotted</button>', new_modal_buttons)
    
    new_notes = """</div>
                <p class="bird-modal__fact"></p>
                <textarea id="journal-note-area" class="journal-notes" rows="2" placeholder="Add personal field notes here..."></textarea>"""
    js_content = js_content.replace('</div>\n                <p class="bird-modal__fact"></p>', new_notes)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

print("Advanced Features (Dark Mode, Gamification, Share API, Journal Notes, Print Styles) Implemented Successfully.")
