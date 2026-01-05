/* Beak-a-Boo Certificate Engine v3.0
   Features: Procedural Shaded Parchment, High-Fidelity Typography, 
   and Vector-Style Ornate Borders.
*/

const SWEAR_BLACKLIST = ["badword", "swear", "inappropriate"];
let slideIndex = 1;

document.addEventListener('DOMContentLoaded', () => {
    if (typeof birdsData === 'undefined') return;

    if (document.getElementById('bird-slideshow-wrapper')) {
        populateSlideshow();
        showSlides(slideIndex);
        setInterval(() => plusSlides(1), 5000);
    }

    if (document.getElementById('oath-confirm-btn')) {
        setupCertificateLogic();
    }

    if (document.getElementById('catalogue-grid')) {
        populateCatalogue(birdsData);
        setupSearch();
    }
});

// --- General Site Logic ---
function populateSlideshow() {
    const wrapper = document.getElementById('bird-slideshow-wrapper');
    const dotsContainer = document.getElementById('slideshow-dots');
    const featuredBirds = birdsData.slice(0, 5); 
    featuredBirds.forEach((bird, index) => {
        const slide = document.createElement('div');
        slide.className = 'bird-slide fade';
        slide.innerHTML = `<img src="${bird.Image}" alt="${bird.Common_Name}"><div class="slide-content"><h3 class="playfair-font">${bird.Common_Name}</h3><p><strong>${bird.Type}</strong> | ${bird.Fact}</p></div>`;
        wrapper.appendChild(slide);
        const dot = document.createElement('span');
        dot.className = 'dot';
        dot.onclick = () => currentSlide(index + 1);
        dotsContainer.appendChild(dot);
    });
}
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

function populateCatalogue(data) {
    const grid = document.getElementById('catalogue-grid');
    grid.innerHTML = "";
    data.forEach(bird => {
        const card = document.createElement('div');
        card.className = 'bird-card';
        card.innerHTML = `<img src="${bird.Image}" alt="${bird.Common_Name}" loading="lazy"><div class="bird-card-info"><div class="bird-card-title">${bird.Common_Name}</div><div class="bird-card-meta"><span style="color: #1e401f; font-weight:bold;">${bird.Type}</span> • ${bird.Season}</div><p class="bird-card-desc">${bird.Fact}</p></div>`;
        grid.appendChild(card);
    });
}

function setupSearch() {
    const searchInput = document.getElementById('catalogue-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = birdsData.filter(bird => bird.Common_Name.toLowerCase().includes(term) || bird.Type.toLowerCase().includes(term));
            populateCatalogue(filtered);
        });
    }
}

// --- High-Resolution Certificate Engine ---

function setupCertificateLogic() {
    const btns = document.querySelectorAll('.cert-btn');
    const oathArea = document.getElementById('cert-oath-area');
    const nameInput = document.getElementById('user-name-input');
    const confirmBtn = document.getElementById('oath-confirm-btn');
    const hatchlingSelect = document.getElementById('hatchling-bird-select');
    const hatchlingPrompt = document.getElementById('hatchling-prompt');
    const downloadContainer = document.getElementById('download-container');

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
            oathArea.scrollIntoView({ behavior: 'smooth' });
        });
    });

    confirmBtn.addEventListener('click', () => {
        const name = nameInput.value.trim();
        if (!name) return;
        const birdChoice = (selectedType === 'Hatchling') ? hatchlingSelect.value : null;
        drawCertificate(name, selectedType, birdChoice);
        oathArea.classList.add('hidden');
        document.getElementById('certificate-canvas').classList.remove('hidden');
        downloadContainer.classList.remove('hidden');
    });

    document.getElementById('btn-download').addEventListener('click', () => {
        const canvas = document.getElementById('certificate-canvas');
        const link = document.createElement('a');
        link.download = `Beak-a-Boo_Certificate.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();
    });
}

function drawCertificate(name, type, birdName) {
    const canvas = document.getElementById('certificate-canvas');
    const ctx = canvas.getContext('2d');
    
    // High-Res Print Dimensions (A4 Ratio)
    canvas.width = 2000;
    canvas.height = 1414;

    // 1. Procedural Parchment Shading
    renderParchment(ctx, canvas.width, canvas.height);

    // 2. Ornate Vector Borders
    renderBorders(ctx, canvas.width, canvas.height);

    // 3. Typography & Assets
    const logo = new Image();
    logo.src = 'logo.png';
    logo.onload = () => {
        // Shaded Watermark
        ctx.save();
        ctx.globalAlpha = 0.07;
        ctx.globalCompositeOperation = 'multiply';
        ctx.drawImage(logo, (canvas.width - 900)/2, (canvas.height - 900)/2, 900, 900);
        ctx.restore();

        renderText(ctx, canvas, name, type, birdName);
    };
}

function renderParchment(ctx, w, h) {
    // Light-to-Dark Radial Shading
    const baseGrd = ctx.createRadialGradient(w/2, h/2, 200, w/2, h/2, w*0.9);
    baseGrd.addColorStop(0, "#fdf8ec"); // Bright center
    baseGrd.addColorStop(0.6, "#f1e3c4"); // Natural mid
    baseGrd.addColorStop(1, "#dcc499");   // Aged edge
    ctx.fillStyle = baseGrd;
    ctx.fillRect(0, 0, w, h);

    // Realistic Organic "Coffee Stains"
    for(let i=0; i<12; i++) {
        ctx.save();
        const x = Math.random() * w;
        const y = Math.random() * h;
        const rad = Math.random() * 400 + 100;
        const grd = ctx.createRadialGradient(x, y, 0, x, y, rad);
        grd.addColorStop(0, "rgba(101, 67, 33, 0.06)");
        grd.addColorStop(1, "rgba(101, 67, 33, 0)");
        ctx.fillStyle = grd;
        ctx.beginPath();
        ctx.arc(x, y, rad, 0, Math.PI*2);
        ctx.fill();
        ctx.restore();
    }

    // High-Fidelity Paper Grain
    ctx.save();
    ctx.globalCompositeOperation = 'overlay';
    for (let i = 0; i < 60000; i++) {
        const x = Math.random() * w;
        const y = Math.random() * h;
        const opacity = Math.random() * 0.12;
        ctx.fillStyle = `rgba(0, 0, 0, ${opacity})`;
        ctx.fillRect(x, y, 1.2, 1.2);
    }
    ctx.restore();

    // Dark Corner Vignette
    const vig = ctx.createRadialGradient(w/2, h/2, w/4, w/2, h/2, w/1.1);
    vig.addColorStop(0, "rgba(0,0,0,0)");
    vig.addColorStop(1, "rgba(70, 45, 10, 0.25)");
    ctx.fillStyle = vig;
    ctx.fillRect(0, 0, w, h);
}

function renderBorders(ctx, w, h) {
    const margin = 60;
    
    // Outer Beak-a-Boo Green Border
    ctx.strokeStyle = '#1e401f';
    ctx.lineWidth = 45;
    ctx.strokeRect(margin, margin, w - margin*2, h - margin*2);

    // Stamped Gold Inlay Line
    const goldMargin = 100;
    ctx.strokeStyle = '#c5a059';
    ctx.lineWidth = 5;
    ctx.strokeRect(goldMargin, goldMargin, w - goldMargin*2, h - goldMargin*2);
    
    // Drop shadow on the gold line for depth
    ctx.strokeStyle = 'rgba(0,0,0,0.15)';
    ctx.lineWidth = 1;
    ctx.strokeRect(goldMargin + 3, goldMargin + 3, w - goldMargin*2, h - goldMargin*2);

    // Ornate Corner Details
    drawCorner(ctx, goldMargin, goldMargin, 0);
    drawCorner(ctx, w - goldMargin, goldMargin, Math.PI/2);
    drawCorner(ctx, w - goldMargin, h - goldMargin, Math.PI);
    drawCorner(ctx, goldMargin, h - goldMargin, -Math.PI/2);
}

function drawCorner(ctx, x, y, angle) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.fillStyle = '#1e401f';
    ctx.beginPath();
    ctx.arc(0, 0, 30, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle = '#c5a059';
    ctx.lineWidth = 4;
    ctx.stroke();
    // Inner dot flourish
    ctx.fillStyle = '#c5a059';
    ctx.beginPath();
    ctx.arc(0, 0, 8, 0, Math.PI*2);
    ctx.fill();
    ctx.restore();
}

function renderText(ctx, canvas, name, type, birdName) {
    ctx.textAlign = 'center';
    ctx.shadowColor = "rgba(0,0,0,0.15)";
    ctx.shadowBlur = 4;

    // Header
    ctx.fillStyle = '#1e401f';
    ctx.font = '700 110px "Cinzel Decorative", serif';
    ctx.fillText('Beak-a-Boo Certificate', canvas.width/2, 380);

    // Rank Achievement
    ctx.fillStyle = '#8B4513';
    ctx.font = '700 80px "Cinzel Decorative", serif';
    let rank = type === 'EagleEye' ? 'Master Birder' : type;
    ctx.fillText(`${rank} Achievement`, canvas.width/2, 510);

    // Middle Text
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#555';
    ctx.font = 'italic 55px "Playfair Display", serif';
    ctx.fillText('This official credential is presented to:', canvas.width/2, 660);

    // Name
    ctx.fillStyle = '#1e401f';
    ctx.font = '170px "Great Vibes", cursive';
    ctx.fillText(name, canvas.width/2, 840);

    // Gold Underline
    ctx.strokeStyle = '#c5a059';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(canvas.width/2 - 450, 865);
    ctx.lineTo(canvas.width/2 + 450, 865);
    ctx.stroke();

    // Achievement Description
    ctx.fillStyle = '#333';
    ctx.font = '48px "Playfair Display", serif';
    let text = "";
    if (type === 'Hatchling') text = `For identifying their first bird: The ${birdName}!`;
    else if (type === 'Fledgling') text = "For successfully identifying 5 distinct bird species.";
    else if (type === 'Brancher') text = "For successfully identifying 10 distinct bird species.";
    else if (type === 'Juvenile') text = "For successfully identifying 20 distinct bird species.";
    else text = "For the incredible feat of identifying all 40 species!";
    ctx.fillText(text, canvas.width/2, 970);

    // Footer Elements
    const footerY = 1200;
    
    // Date
    const today = new Date().toLocaleDateString();
    ctx.font = '55px "Great Vibes", cursive';
    ctx.fillStyle = '#333';
    ctx.fillText(today, 450, footerY);
    ctx.font = '32px "Playfair Display"';
    ctx.fillText("Date of Issue", 450, footerY + 60);

    // President Signature
    ctx.font = '65px "Great Vibes", cursive';
    ctx.fillStyle = '#1e401f';
    ctx.fillText('Shivam Sharma', 1550, footerY);
    ctx.font = '32px "Playfair Display"';
    ctx.fillStyle = '#333';
    ctx.fillText("President, Beak-a-Boo JA", 1550, footerY + 60);

    // Gold Seal
    drawSeal(ctx, canvas.width/2, footerY - 30, 110);
}

function drawSeal(ctx, x, y, radius) {
    ctx.save();
    ctx.translate(x, y);
    const spikes = 40;
    ctx.beginPath();
    for (let i = 0; i < spikes; i++) {
        let angle = (Math.PI / spikes) * 2 * i;
        ctx.lineTo(Math.cos(angle) * radius, Math.sin(angle) * radius);
        angle += (Math.PI / spikes);
        ctx.lineTo(Math.cos(angle) * (radius-15), Math.sin(angle) * (radius-15));
    }
    ctx.closePath();
    
    const grd = ctx.createLinearGradient(-radius, -radius, radius, radius);
    grd.addColorStop(0, "#FFD700");
    grd.addColorStop(0.5, "#B8860B");
    grd.addColorStop(1, "#FFD700");
    ctx.fillStyle = grd;
    ctx.fill();
    ctx.strokeStyle = "#8B4513";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.restore();
}
