import os
import re

script_path = r"c:\Users\aweso\Downloads\Testing2\script.js"

with open(script_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# 1. Add Bird Journal Logic
journal_logic = """
// --- Bird Journal Memory ---
function getSpottedBirds() {
    return JSON.parse(localStorage.getItem('spottedBirds') || '[]');
}

function toggleSpotted(birdId) {
    let spotted = getSpottedBirds();
    if (spotted.includes(birdId)) {
        spotted = spotted.filter(id => id !== birdId);
    } else {
        spotted.push(birdId);
    }
    localStorage.setItem('spottedBirds', JSON.stringify(spotted));
    updateProgress();
    
    // Update UI for the specific card
    const card = document.querySelector(`.bird-card[data-common-name="${birdId}"]`);
    if (card) {
        if (spotted.includes(birdId)) card.classList.add('spotted');
        else card.classList.remove('spotted');
    }
    
    // Update modal button if open
    const modalBtn = document.getElementById('modal-spotted-btn');
    if (modalBtn) {
        if (spotted.includes(birdId)) {
            modalBtn.textContent = '✓ Spotted';
            modalBtn.classList.add('is-spotted');
        } else {
            modalBtn.textContent = 'Mark as Spotted';
            modalBtn.classList.remove('is-spotted');
        }
    }
}

function updateProgress() {
    const spotted = getSpottedBirds();
    const progressEl = document.getElementById('spotted-progress');
    if (progressEl) {
        progressEl.textContent = `${spotted.length} / ${birdsData.length} Birds Spotted`;
    }
}
"""

# Inject before populateCatalogue
js_content = js_content.replace('function populateCatalogue(data) {', journal_logic + '\nfunction populateCatalogue(data) {')

# Update populateCatalogue to use the spotted state
populate_replacement = """function populateCatalogue(data) {
    const grid = document.getElementById('catalogue-grid');
    if (!grid) return;
    grid.innerHTML = "";
    const spotted = getSpottedBirds();
    data.forEach(bird => {
        const card = document.createElement('div');
        card.className = 'bird-card';
        if (spotted.includes(bird.Common_Name)) card.classList.add('spotted');
        card.tabIndex = 0;
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `View details for ${bird.Common_Name}`);
        card.dataset.commonName = bird.Common_Name;
        card.dataset.scientificName = bird.Scientific_Name;
        card.dataset.type = bird.Type;
        card.dataset.season = bird.Season;
        card.dataset.fact = bird.Fact;
        card.dataset.call = bird.Call;
        card.dataset.whistle = bird.Whistle;
        card.dataset.image = bird.Image;
        card.innerHTML = `
            <div class="spotted-badge">✓</div>
            <img src="${bird.Image}" alt="${bird.Common_Name}" loading="lazy">
            <div class="bird-card-info">
                <div class="bird-card-title">${bird.Common_Name}</div>
                <div class="bird-card-meta"><span style="color: var(--primary-green); font-weight:bold;">${bird.Type}</span> • ${bird.Season}</div>
                <p class="bird-card-desc">${bird.Fact}</p>
            </div>`;
        grid.appendChild(card);
    });
    updateProgress();
}"""

js_content = re.sub(r'function populateCatalogue\(data\) \{[\s\S]*?(?=function setupCatalogueModal)', populate_replacement + '\n\n', js_content)


# Update setupCatalogueModal to include spotted button and audio placeholder
modal_replacement = """function setupCatalogueModal() {
    if (document.getElementById('bird-modal')) return;
    const modal = document.createElement('div');
    modal.className = 'bird-modal';
    modal.id = 'bird-modal';
    modal.setAttribute('aria-hidden', 'true');
    modal.innerHTML = `
        <div class="bird-modal__backdrop"></div>
        <div class="bird-modal__content" role="dialog" aria-modal="true" aria-labelledby="bird-modal-title">
            <button class="bird-modal__close" type="button" aria-label="Close bird details">&times;</button>
            <div class="bird-modal__media">
                <img class="bird-modal__image" src="" alt="">
            </div>
            <div class="bird-modal__details">
                <div class="bird-modal__header-flex">
                    <div>
                        <h2 class="bird-modal__title" id="bird-modal-title"></h2>
                        <p class="bird-modal__scientific"></p>
                    </div>
                    <button id="modal-spotted-btn" class="cta-button" style="margin: 0; padding: 8px 16px; font-size: 0.9rem;">Mark as Spotted</button>
                </div>
                <div class="bird-modal__meta">
                    <span class="bird-modal__type"></span>
                    <span class="bird-modal__season"></span>
                </div>
                <p class="bird-modal__fact"></p>
                <div class="bird-modal__callout">
                    <h3>Bird call <button class="audio-btn" aria-label="Play bird call"><i class="fa-solid fa-play"></i></button></h3>
                    <p class="bird-modal__call"></p>
                </div>
                <div class="bird-modal__callout">
                    <h3>Whistle tip</h3>
                    <p class="bird-modal__whistle"></p>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    const closeModal = () => {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('modal-open');
    };

    modal.querySelector('.bird-modal__close').addEventListener('click', closeModal);
    modal.querySelector('.bird-modal__backdrop').addEventListener('click', closeModal);
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });

    document.getElementById('modal-spotted-btn').addEventListener('click', () => {
        const title = document.getElementById('bird-modal-title').textContent;
        toggleSpotted(title);
    });
}"""

js_content = re.sub(r'function setupCatalogueModal\(\) \{[\s\S]*?(?=function setupCatalogueInteractions)', modal_replacement + '\n\n', js_content)


# Update openBirdModal to set the spotted button state
open_modal_addition = """
    const spotted = getSpottedBirds();
    const modalBtn = document.getElementById('modal-spotted-btn');
    if (spotted.includes(bird.Common_Name)) {
        modalBtn.textContent = '✓ Spotted';
        modalBtn.classList.add('is-spotted');
    } else {
        modalBtn.textContent = 'Mark as Spotted';
        modalBtn.classList.remove('is-spotted');
    }
    
    // Play placeholder audio logic
    const audioBtn = modal.querySelector('.audio-btn');
    audioBtn.onclick = () => {
        const icon = audioBtn.querySelector('i');
        icon.className = 'fa-solid fa-pause';
        setTimeout(() => icon.className = 'fa-solid fa-play', 2000); // Simulate 2s audio
    };
"""
js_content = js_content.replace("modal.setAttribute('aria-hidden', 'false');", open_modal_addition + "\n    modal.setAttribute('aria-hidden', 'false');")


# 2. Profanity Filter Logic
profanity_check = """
        const lowerName = name.toLowerCase();
        const hasSwear = SWEAR_BLACKLIST.some(swear => lowerName.includes(swear));
        if (hasSwear) {
            errorMessage.textContent = "Please use an appropriate name.";
            nameInput.classList.add('shake');
            setTimeout(() => nameInput.classList.remove('shake'), 500);
            return;
        }
"""
js_content = js_content.replace('if (name.length > maxNameLength) {', profanity_check + '        if (name.length > maxNameLength) {')

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated script.js with Memory, Profanity Filter, and Audio hooks.")
