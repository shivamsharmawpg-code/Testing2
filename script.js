/* Beak-a-boo Certificate Engine v4.0
   Restoring high-fidelity shading, organic textures, and ornate flourishes.
*/

const SWEAR_BLACKLIST = ["badword", "swear", "inappropriate"];
let slideIndex = 1;

document.addEventListener('DOMContentLoaded', () => {
    if (typeof birdsData === 'undefined') return;

    // Initialize Home Page Slideshow
    if (document.getElementById('bird-slideshow-wrapper')) {
        setupCatalogueModal();
        populateSlideshow();
        setupSlideshowInteractions();
        showSlides(slideIndex);
        setInterval(() => plusSlides(1), 5000);
    }

    // Initialize Certificate Logic
    if (document.getElementById('oath-confirm-btn')) {
        setupCertificateLogic();
    }

    // Initialize Catalogue Logic
    if (document.getElementById('catalogue-grid')) {
        setupCatalogueModal();
        populateCatalogue(birdsData);
        setupCatalogueInteractions();
        setupSearch();
    }

    setupHomepageAnimations();
});

// --- General Utility ---
function plusSlides(n) { showSlides(slideIndex += n); }
function currentSlide(n) { showSlides(slideIndex = n); }
function showSlides(n) {
    const slides = document.getElementsByClassName("bird-slide");
    const dots = document.getElementsByClassName("dot");
    if (!slides.length) return;
    if (n > slides.length) slideIndex = 1;
    if (n < 1) slideIndex = slides.length;
    for (let i = 0; i < slides.length; i++) slides[i].style.display = "none";
    for (let i = 0; i < dots.length; i++) dots[i].className = dots[i].className.replace(" active", "");
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

function populateSlideshow() {
    const wrapper = document.getElementById('bird-slideshow-wrapper');
    const dotsContainer = document.getElementById('slideshow-dots');
    const featuredBirds = birdsData.slice(0, 10); 
    featuredBirds.forEach((bird, index) => {
        const slide = document.createElement('div');
        slide.className = 'bird-slide fade';
        slide.innerHTML = `
            <button class="slide-card" type="button">
                <img src="${bird.Image}" alt="${bird.Common_Name}">
                <div class="slide-content">
                    <h3 class="playfair-font">${bird.Common_Name}</h3>
                    <p><strong>${bird.Type}</strong> | ${bird.Fact}</p>
                    <span class="slide-cta">Learn more</span>
                </div>
            </button>
        `;
        const button = slide.querySelector('.slide-card');
        button.dataset.commonName = bird.Common_Name;
        button.dataset.scientificName = bird.Scientific_Name;
        button.dataset.type = bird.Type;
        button.dataset.season = bird.Season;
        button.dataset.fact = bird.Fact;
        button.dataset.call = bird.Call;
        button.dataset.whistle = bird.Whistle;
        button.dataset.image = bird.Image;
        wrapper.appendChild(slide);
        const dot = document.createElement('span');
        dot.className = 'dot';
        dot.onclick = () => currentSlide(index + 1);
        dotsContainer.appendChild(dot);
    });
}

function setupSlideshowInteractions() {
    const wrapper = document.getElementById('bird-slideshow-wrapper');
    if (!wrapper) return;
    wrapper.addEventListener('click', (event) => {
        const button = event.target.closest('.slide-card');
        if (!button) return;
        openBirdModal({
            Common_Name: button.dataset.commonName,
            Scientific_Name: button.dataset.scientificName,
            Type: button.dataset.type,
            Season: button.dataset.season,
            Fact: button.dataset.fact,
            Call: button.dataset.call,
            Whistle: button.dataset.whistle,
            Image: button.dataset.image
        });
    });
}

function setupHomepageAnimations() {
    const animatedItems = document.querySelectorAll('.animate-on-scroll, .animate-on-load');
    if (!animatedItems.length) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        animatedItems.forEach((item) => item.classList.add('is-visible'));
        return;
    }

    document.querySelectorAll('.animate-on-load').forEach((item) => {
        requestAnimationFrame(() => item.classList.add('is-visible'));
    });

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.2 }
    );

    document.querySelectorAll('.animate-on-scroll').forEach((item) => observer.observe(item));
}

function populateCatalogue(data) {
    const grid = document.getElementById('catalogue-grid');
    grid.innerHTML = "";
    data.forEach(bird => {
        const card = document.createElement('div');
        card.className = 'bird-card';
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
        card.innerHTML = `<img src="${bird.Image}" alt="${bird.Common_Name}" loading="lazy"><div class="bird-card-info"><div class="bird-card-title">${bird.Common_Name}</div><div class="bird-card-meta"><span style="color: #1e401f; font-weight:bold;">${bird.Type}</span> • ${bird.Season}</div><p class="bird-card-desc">${bird.Fact}</p></div>`;
        grid.appendChild(card);
    });
}

function setupCatalogueModal() {
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
                <h2 class="bird-modal__title" id="bird-modal-title"></h2>
                <p class="bird-modal__scientific"></p>
                <div class="bird-modal__meta">
                    <span class="bird-modal__type"></span>
                    <span class="bird-modal__season"></span>
                </div>
                <p class="bird-modal__fact"></p>
                <div class="bird-modal__callout">
                    <h3>Bird call</h3>
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
}

function setupCatalogueInteractions() {
    const grid = document.getElementById('catalogue-grid');
    if (!grid) return;
    const handleOpen = (card) => {
        if (!card) return;
        openBirdModal({
            Common_Name: card.dataset.commonName,
            Scientific_Name: card.dataset.scientificName,
            Type: card.dataset.type,
            Season: card.dataset.season,
            Fact: card.dataset.fact,
            Call: card.dataset.call,
            Whistle: card.dataset.whistle,
            Image: card.dataset.image
        });
    };

    grid.addEventListener('click', (event) => {
        handleOpen(event.target.closest('.bird-card'));
    });

    grid.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' && event.key !== ' ') return;
        const card = event.target.closest('.bird-card');
        if (!card) return;
        event.preventDefault();
        handleOpen(card);
    });
}

function openBirdModal(bird) {
    const modal = document.getElementById('bird-modal');
    if (!modal) return;
    modal.querySelector('.bird-modal__image').src = bird.Image;
    modal.querySelector('.bird-modal__image').alt = bird.Common_Name;
    modal.querySelector('.bird-modal__title').textContent = bird.Common_Name;
    modal.querySelector('.bird-modal__scientific').textContent = bird.Scientific_Name;
    modal.querySelector('.bird-modal__type').textContent = bird.Type;
    modal.querySelector('.bird-modal__season').textContent = bird.Season;
    modal.querySelector('.bird-modal__fact').textContent = bird.Fact;
    modal.querySelector('.bird-modal__call').textContent = bird.Call || "Call details coming soon.";
    modal.querySelector('.bird-modal__whistle').textContent = bird.Whistle || "Whistle tips coming soon.";
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
}

function setupSearch() {
    const searchInput = document.getElementById('catalogue-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = birdsData.filter(bird =>
                bird.Common_Name.toLowerCase().includes(term) ||
                bird.Type.toLowerCase().includes(term) ||
                bird.Season.toLowerCase().includes(term)
            );
            populateCatalogue(filtered);
        });
    }
}

// --- High-End Certificate Logic ---

function setupCertificateLogic() {
    const btns = document.querySelectorAll('.cert-btn');
    const oathArea = document.getElementById('cert-oath-area');
    const nameInput = document.getElementById('user-name-input');
    const errorMessage = document.getElementById('error-message');
    const confirmBtn = document.getElementById('oath-confirm-btn');
    const hatchlingSelect = document.getElementById('hatchling-bird-select');
    const hatchlingPrompt = document.getElementById('hatchling-prompt');
    const downloadContainer = document.getElementById('download-container');
    const maxNameLength = 32;

    const sortedBirds = [...birdsData].sort((a, b) => a.Common_Name.localeCompare(b.Common_Name));
    sortedBirds.forEach(bird => {
        const opt = document.createElement('option');
        opt.value = bird.Common_Name;
        opt.textContent = bird.Common_Name;
        hatchlingSelect.appendChild(opt);
    });

    let selectedType = "";
    btns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            selectedType = e.target.dataset.certType;
            oathArea.classList.remove('hidden');
            if (selectedType === 'Hatchling') hatchlingPrompt.classList.remove('hidden');
            else hatchlingPrompt.classList.add('hidden');
        });
    });

    confirmBtn.addEventListener('click', () => {
        if (!selectedType) {
            errorMessage.textContent = "Please choose a certificate rank first.";
            return;
        }
        const name = nameInput.value.trim();
        if (!name) {
            errorMessage.textContent = "Please enter your name.";
            return;
        }
        if (name.length > maxNameLength) {
            errorMessage.textContent = `Name must be ${maxNameLength} characters or fewer.`;
            return;
        }
        errorMessage.textContent = "";
        const birdChoice = (selectedType === 'Hatchling') ? hatchlingSelect.value : null;
        drawCertificate(name, selectedType, birdChoice);
        oathArea.classList.add('hidden');
        document.getElementById('certificate-canvas').classList.remove('hidden');
        downloadContainer.classList.remove('hidden');
    });

    document.getElementById('btn-download').addEventListener('click', () => {
        const canvas = document.getElementById('certificate-canvas');
        const link = document.createElement('a');
        link.download = `Beak-a-boo_Certificate.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();
    });
}

function drawCertificate(name, type, birdName) {
    const canvas = document.getElementById('certificate-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 2000;
    canvas.height = 1414;

    // 1. ADVANCED SHADED PARCHMENT
    renderParchment(ctx, canvas.width, canvas.height);

    // 2. ORNATE DOUBLE BORDER
    renderBorders(ctx, canvas.width, canvas.height);

    const logo = new Image();
    logo.crossOrigin = "anonymous";
    const logoImg = document.querySelector('.logo-img');
    logo.src = logoImg ? logoImg.src : '../logo.png';
    logo.onload = () => {
        // Watermark with blending
        ctx.save();
        ctx.globalAlpha = 0.08;
        ctx.globalCompositeOperation = 'multiply';
        const maxLogoSize = 900;
        const scale = Math.min(
            maxLogoSize / logo.width,
            maxLogoSize / logo.height,
            1
        );
        const logoWidth = logo.width * scale;
        const logoHeight = logo.height * scale;
        ctx.drawImage(
            logo,
            (canvas.width - logoWidth) / 2,
            (canvas.height - logoHeight) / 2,
            logoWidth,
            logoHeight
        );
        ctx.restore();

        renderText(ctx, canvas, name, type, birdName);
    };
    logo.onerror = () => {
        renderText(ctx, canvas, name, type, birdName);
    };
}

function renderParchment(ctx, w, h) {
    // Base Shaded Gradient
    const grd = ctx.createRadialGradient(w/2, h/2, 100, w/2, h/2, w);
    grd.addColorStop(0, "#fdf8ef");
    grd.addColorStop(0.7, "#eee0c5");
    grd.addColorStop(1, "#d9c5a3");
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, w, h);

    // Procedural Organic Spots (Aged look)
    for(let i=0; i<15; i++) {
        ctx.save();
        const x = Math.random() * w;
        const y = Math.random() * h;
        const radius = Math.random() * 300 + 100;
        const spotGrd = ctx.createRadialGradient(x,y,0,x,y,radius);
        spotGrd.addColorStop(0, "rgba(139, 69, 19, 0.06)");
        spotGrd.addColorStop(1, "rgba(139, 69, 19, 0)");
        ctx.fillStyle = spotGrd;
        ctx.beginPath(); ctx.arc(x,y,radius,0,Math.PI*2); ctx.fill();
        ctx.restore();
    }

    // Paper Grain
    ctx.save();
    ctx.globalCompositeOperation = 'overlay';
    for (let i = 0; i < 50000; i++) {
        const x = Math.random() * w;
        const y = Math.random() * h;
        ctx.fillStyle = `rgba(0,0,0,${Math.random() * 0.1})`;
        ctx.fillRect(x, y, 1.2, 1.2);
    }
    ctx.restore();
}

function renderBorders(ctx, w, h) {
    const pad = 60;
    // Thick Outer Brand Green
    ctx.strokeStyle = '#1e401f';
    ctx.lineWidth = 50;
    ctx.strokeRect(pad, pad, w - pad*2, h - pad*2);

    // Golden dashed line accent
    ctx.save();
    ctx.setLineDash([15, 10]);
    ctx.strokeStyle = '#c5a059';
    ctx.lineWidth = 4;
    ctx.strokeRect(pad, pad, w - pad*2, h - pad*2);
    ctx.restore();

    // Inner gold pin-stripe
    const innerPad = 100;
    ctx.strokeStyle = '#D4AF37';
    ctx.lineWidth = 5;
    ctx.strokeRect(innerPad, innerPad, w - innerPad*2, h - innerPad*2);

    // Draw Corner Flourishes
    drawFlourish(ctx, innerPad, innerPad, 0);
    drawFlourish(ctx, w - innerPad, innerPad, 90);
    drawFlourish(ctx, w - innerPad, h - innerPad, 180);
    drawFlourish(ctx, innerPad, h - innerPad, 270);
}

function drawFlourish(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot * Math.PI / 180);
    ctx.strokeStyle = '#D4AF37';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(0, 0); ctx.lineTo(100, 0);
    ctx.moveTo(0, 0); ctx.lineTo(0, 100);
    ctx.stroke();
    // Accent circle
    ctx.fillStyle = '#1e401f';
    ctx.beginPath(); ctx.arc(45, 45, 10, 0, Math.PI*2); ctx.fill();
    ctx.strokeStyle = '#c5a059'; ctx.stroke();
    ctx.restore();
}

function renderText(ctx, canvas, name, type, birdName) {
    ctx.textAlign = 'center';
    
    const typeKey = (type || '').toUpperCase();
    const rankMap = {
        HATCHLING: 'Hatchling',
        FLEDGLING: 'Fledgling',
        BRANCHER: 'Brancher',
        JUVENILE: 'Juvenile',
        EAGLEEYE: 'Skywarden'
    };

    // Header
    ctx.shadowColor = "rgba(0,0,0,0.15)";
    ctx.shadowBlur = 3;
    ctx.fillStyle = '#2b1b11';
    ctx.font = '700 120px "Cinzel Decorative", serif';
    ctx.fillText('EXPLORERS CERTIFICATE', canvas.width/2, 370);

    // Rank Achievement
    ctx.fillStyle = '#6b3e1f';
    ctx.font = '700 70px "Cinzel Decorative", serif';
    const rank = rankMap[typeKey] || type;
    ctx.fillText(`${rank.toUpperCase()} ACHIEVEMENT`, canvas.width/2, 485);

    // Detail
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#5b4a3d';
    ctx.font = 'italic 48px "Playfair Display", serif';
    ctx.fillText('this certificate is proudly presented to', canvas.width/2, 625);

    // Name
    ctx.fillStyle = '#2b1b11';
    ctx.font = '170px "Great Vibes", cursive';
    ctx.fillText(name, canvas.width/2, 825);

    // Signature Line
    ctx.strokeStyle = '#D4AF37'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(canvas.width/2 - 400, 850); ctx.lineTo(canvas.width/2 + 400, 850); ctx.stroke();

    // Text
    ctx.fillStyle = '#3a2a20';
    ctx.font = '44px "Playfair Display", serif';
    let text = "";
    if (typeKey === 'HATCHLING') text = `for identifying their first bird: the ${birdName}!`;
    else if (typeKey === 'FLEDGLING') text = "for successfully identifying 5 bird species";
    else if (typeKey === 'BRANCHER') text = "for successfully identifying 10 bird species";
    else if (typeKey === 'JUVENILE') text = "for successfully identifying 20 bird species";
    else text = "for the incredible feat of identifying all 40 bird species";
    ctx.fillText(text, canvas.width/2, 950);

    // Footer
    const footY = 1120;
    const today = new Date().toLocaleDateString();
    ctx.font = '55px "Great Vibes", cursive'; ctx.fillStyle = '#3a2a20';
    ctx.fillText(today, 450, footY);
    ctx.font = '32px "Playfair Display"'; ctx.fillText("Date", 450, footY+60);

    // President
    ctx.font = '65px "Great Vibes", cursive'; ctx.fillStyle = '#3a2a20';
    ctx.fillText('Shivam Sharma', 1550, footY);
    ctx.font = '32px "Playfair Display"'; ctx.fillStyle = '#333';
    ctx.fillText("President, Beak-a-boo", 1550, footY+55);
    ctx.fillText("JA", 1550, footY+95);

    // Seal
    drawGoldSeal(ctx, canvas.width/2, footY - 20, 115);
}

function drawGoldSeal(ctx, x, y, r) {
    ctx.save();
    ctx.translate(x,y);
    const spikes = 45;
    ctx.beginPath();
    for(let i=0; i<spikes; i++) {
        let a = (Math.PI/spikes)*2*i;
        ctx.lineTo(Math.cos(a)*r, Math.sin(a)*r);
        a += (Math.PI/spikes);
        ctx.lineTo(Math.cos(a)*(r-15), Math.sin(a)*(r-15));
    }
    ctx.closePath();
    const g = ctx.createLinearGradient(-r,-r,r,r);
    g.addColorStop(0,"#FFD700"); g.addColorStop(0.5,"#B8860B"); g.addColorStop(1,"#FFD700");
    ctx.fillStyle = g; ctx.fill();
    ctx.strokeStyle = "#8B4513"; ctx.lineWidth = 2; ctx.stroke();
    ctx.restore();
}
