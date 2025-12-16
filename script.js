/* NOTE: birdsData is now loaded directly in the HTML files 
   to reduce the size of this script file.
*/

const SWEAR_BLACKLIST = ["badword", "swear", "inappropriate"];
let slideIndex = 1;

document.addEventListener('DOMContentLoaded', () => {
    // Check if birdsData exists
    if (typeof birdsData === 'undefined') {
        console.error("Bird Data not found. Ensure it is included in the HTML file.");
        return;
    }

    // Check if we are on the home page
    if (document.getElementById('bird-slideshow-wrapper')) {
        populateSlideshow();
        showSlides(slideIndex);
        setInterval(() => plusSlides(1), 5000);
    }

    // Check if we are on the certificate page
    if (document.getElementById('oath-confirm-btn')) {
        setupCertificateLogic();
    }

    // Check if we are on the catalogue page
    if (document.getElementById('catalogue-grid')) {
        populateCatalogue(birdsData);
        setupSearch();
    }
});

// --- Slideshow Logic ---
function populateSlideshow() {
    const wrapper = document.getElementById('bird-slideshow-wrapper');
    const dotsContainer = document.getElementById('slideshow-dots');
    const featuredBirds = birdsData.slice(0, 5); 

    featuredBirds.forEach((bird, index) => {
        const slide = document.createElement('div');
        slide.className = 'bird-slide fade';
        slide.innerHTML = `
            <img src="${bird.Image}" alt="${bird.Common_Name}">
            <div class="slide-content">
                <h3 class="playfair-font">${bird.Common_Name}</h3>
                <p><strong>${bird.Type}</strong> | ${bird.Fact}</p>
            </div>
        `;
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

// --- Catalogue Logic ---
function populateCatalogue(data) {
    const grid = document.getElementById('catalogue-grid');
    grid.innerHTML = "";
    data.forEach(bird => {
        const card = document.createElement('div');
        card.className = 'bird-card';
        card.innerHTML = `
            <img src="${bird.Image}" alt="${bird.Common_Name}" loading="lazy">
            <div class="bird-card-info">
                <div class="bird-card-title">${bird.Common_Name}</div>
                <div class="bird-card-meta"><span style="color: var(--primary-green); font-weight:bold;">${bird.Type}</span> • ${bird.Season}</div>
                <p class="bird-card-desc">${bird.Fact}</p>
            </div>
        `;
        grid.appendChild(card);
    });
}
function setupSearch() {
    const searchInput = document.getElementById('catalogue-search');
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

// --- Certificate Logic ---
function checkName(name) {
    const cleanName = name.toLowerCase().replace(/\s/g, '');
    return !SWEAR_BLACKLIST.some(word => cleanName.includes(word));
}

function setupCertificateLogic() {
    const btns = document.querySelectorAll('.cert-btn');
    const oathArea = document.getElementById('cert-oath-area');
    const nameInput = document.getElementById('user-name-input');
    const confirmBtn = document.getElementById('oath-confirm-btn');
    const errorMsg = document.getElementById('error-message');
    const hatchlingSelect = document.getElementById('hatchling-bird-select');
    const hatchlingPrompt = document.getElementById('hatchling-prompt');
    const downloadContainer = document.getElementById('download-container');
    const downloadBtn = document.getElementById('btn-download');

    // Populate Dropdown using the global birdsData
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
        errorMsg.textContent = "";

        if (!name) { errorMsg.textContent = "Please enter your name."; return; }
        if (!checkName(name)) { errorMsg.textContent = "That name is not allowed."; return; }

        const birdChoice = (selectedType === 'Hatchling') ? hatchlingSelect.value : null;
        
        drawCertificate(name, selectedType, birdChoice);
        
        oathArea.classList.add('hidden');
        document.getElementById('certificate-canvas').classList.remove('hidden');
        downloadContainer.classList.remove('hidden');
    });

    downloadBtn.addEventListener('click', () => {
        const canvas = document.getElementById('certificate-canvas');
        const link = document.createElement('a');
        link.download = `Beak-a-Boo_${selectedType}_Certificate.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();
    });
}

function drawCertificate(name, type, birdName) {
    const canvas = document.getElementById('certificate-canvas');
    const ctx = canvas.getContext('2d');
    
    // High Res
    canvas.width = 2000;
    canvas.height = 1545;

    // 1. Background
    drawParchmentBackground(ctx, canvas.width, canvas.height);

    // 2. Borders
    drawOrnateBorder(ctx, canvas.width, canvas.height);

    // 3. Logo & Text
    const logo = new Image();
    logo.src = 'logo.png';
    logo.onload = () => {
        ctx.save();
        ctx.globalAlpha = 0.12; 
        const wmSize = 1000;
        ctx.drawImage(logo, (canvas.width - wmSize)/2, (canvas.height - wmSize)/2, wmSize, wmSize);
        ctx.restore();

        const smLogoSize = 250;
        ctx.drawImage(logo, (canvas.width - smLogoSize)/2, 140, smLogoSize, smLogoSize);
        
        drawTopFlourishes(ctx, canvas.width);
        drawTextContent(ctx, canvas, name, type, birdName);
    };

    if (logo.complete) logo.onload();
    else logo.onerror = () => drawTextContent(ctx, canvas, name, type, birdName);
}

function drawParchmentBackground(ctx, w, h) {
    ctx.fillStyle = '#f4e4bc'; 
    ctx.fillRect(0, 0, w, h);

    for (let i = 0; i < 50000; i++) {
        const x = Math.random() * w;
        const y = Math.random() * h;
        ctx.fillStyle = `rgba(100, 80, 50, ${Math.random() * 0.05})`;
        ctx.fillRect(x, y, 2, 2);
    }

    const gradient = ctx.createRadialGradient(w/2, h/2, h/3, w/2, h/2, h);
    gradient.addColorStop(0, "rgba(255,255,255,0)");
    gradient.addColorStop(1, "rgba(80, 60, 20, 0.2)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, w, h);
}

function drawOrnateBorder(ctx, w, h) {
    const pad = 60;
    
    ctx.lineWidth = 50;
    ctx.strokeStyle = '#1e401f';
    ctx.strokeRect(pad, pad, w - pad*2, h - pad*2);

    ctx.save();
    ctx.strokeStyle = '#c5a059'; 
    ctx.lineWidth = 3;
    ctx.setLineDash([5, 5]);
    ctx.strokeRect(pad, pad, w - pad*2, h - pad*2);
    ctx.restore();

    const innerPad = 85;
    ctx.lineWidth = 4;
    ctx.strokeStyle = '#D4AF37'; 
    ctx.strokeRect(innerPad, innerPad, w - innerPad*2, h - innerPad*2);

    const corners = [
        {x: innerPad, y: innerPad, r: 0}, 
        {x: w - innerPad, y: innerPad, r: 90}, 
        {x: w - innerPad, y: h - innerPad, r: 180}, 
        {x: innerPad, y: h - innerPad, r: 270} 
    ];

    corners.forEach(c => {
        ctx.save();
        ctx.translate(c.x, c.y);
        ctx.rotate((c.r * Math.PI) / 180);
        drawCornerFlourish(ctx);
        ctx.restore();
    });
}

function drawCornerFlourish(ctx) {
    ctx.beginPath();
    ctx.strokeStyle = '#D4AF37';
    ctx.lineWidth = 3;
    ctx.moveTo(0, 0);
    ctx.lineTo(80, 0);
    ctx.moveTo(0, 0);
    ctx.lineTo(0, 80);
    ctx.moveTo(10, 0);
    ctx.quadraticCurveTo(20, 20, 0, 10);
    ctx.moveTo(0, 0);
    ctx.lineTo(40, 40);
    ctx.stroke();
    ctx.beginPath();
    ctx.fillStyle = '#1e401f';
    ctx.arc(40, 40, 5, 0, Math.PI*2);
    ctx.fill();
}

function drawTopFlourishes(ctx, w) {
    ctx.save();
    ctx.strokeStyle = '#c5a059';
    ctx.lineWidth = 2;
    ctx.beginPath();
    const cx = w/2;
    ctx.moveTo(cx - 150, 250);
    ctx.bezierCurveTo(cx - 200, 220, cx - 250, 280, cx - 300, 250);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx + 150, 250);
    ctx.bezierCurveTo(cx + 200, 220, cx + 250, 280, cx + 300, 250);
    ctx.stroke();
    ctx.restore();
}

function drawGoldSeal(ctx, x, y, radius) {
    ctx.save();
    ctx.translate(x, y);

    ctx.beginPath();
    const spikes = 40;
    const outerRadius = radius;
    const innerRadius = radius - 10;
    
    for (let i = 0; i < spikes; i++) {
        let angle = (Math.PI / spikes) * 2 * i;
        ctx.lineTo(Math.cos(angle) * outerRadius, Math.sin(angle) * outerRadius);
        angle += (Math.PI / spikes);
        ctx.lineTo(Math.cos(angle) * innerRadius, Math.sin(angle) * innerRadius);
    }
    ctx.closePath();
    
    const grd = ctx.createLinearGradient(-radius, -radius, radius, radius);
    grd.addColorStop(0, "#FFD700");
    grd.addColorStop(0.5, "#B8860B");
    grd.addColorStop(1, "#FFD700");
    ctx.fillStyle = grd;
    ctx.fill();
    ctx.strokeStyle = "#B8860B";
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(0, 0, radius - 25, 0, Math.PI*2);
    ctx.strokeStyle = "rgba(255,255,255,0.5)";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.restore();
}

function drawTextContent(ctx, canvas, name, type, birdName) {
    ctx.textAlign = 'center';

    ctx.fillStyle = '#1e401f'; 
    ctx.font = '700 110px "Cinzel Decorative", serif'; 
    ctx.fillText('Beak-a-Boo Certificate', canvas.width / 2, 380);

    ctx.fillStyle = '#8B4513'; 
    ctx.font = '700 80px "Cinzel Decorative", serif';
    let rankText = (type === 'EagleEye' || type === 'MasterBirder') ? "Eagle Eye" : type;
    ctx.fillText(rankText + " Achievement", canvas.width / 2, 500);

    ctx.fillStyle = '#555';
    ctx.font = 'italic 50px "Playfair Display", serif';
    ctx.fillText('Presented to:', canvas.width / 2, 650);
    
    ctx.fillStyle = '#1e401f';
    ctx.font = '150px "Great Vibes", cursive';
    ctx.fillText(name, canvas.width / 2, 820);

    ctx.beginPath();
    ctx.moveTo(canvas.width/2 - 300, 840);
    ctx.lineTo(canvas.width/2 + 300, 840);
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#D4AF37';
    ctx.stroke();

    ctx.fillStyle = '#333';
    ctx.font = '40px "Playfair Display", serif';
    let text = "";
    if (type === 'Hatchling') text = `For identifying their first bird: The ${birdName}!`;
    else if (type === 'Fledgling') text = "For successfully identifying 5 distinct bird species.";
    else if (type === 'Brancher') text = "For successfully identifying 10 distinct bird species.";
    else if (type === 'Juvenile') text = "For successfully identifying 20 distinct bird species.";
    else text = "For the incredible feat of identifying all 40 species!";
    ctx.fillText(text, canvas.width / 2, 950);

    const bottomY = 1250;
    
    const today = new Date().toLocaleDateString();
    ctx.font = '50px "Great Vibes", cursive';
    ctx.fillStyle = '#333';
    ctx.fillText(today, 400, bottomY);
    
    ctx.beginPath();
    ctx.moveTo(250, bottomY + 10);
    ctx.lineTo(550, bottomY + 10);
    ctx.stroke();
    
    ctx.font = '30px "Playfair Display"';
    ctx.fillText("Date", 400, bottomY + 60);

    drawGoldSeal(ctx, canvas.width / 2, bottomY - 20, 100);

    ctx.font = '60px "Great Vibes", cursive';
    ctx.fillStyle = '#1e401f';
    ctx.fillText('Shivam Sharma', 1600, bottomY);
    
    ctx.beginPath();
    ctx.moveTo(1400, bottomY + 10);
    ctx.lineTo(1800, bottomY + 10);
    ctx.stroke();
    
    ctx.font = '30px "Playfair Display"';
    ctx.fillStyle = '#333';
    ctx.fillText("President, Beak-a-Boo JA", 1600, bottomY + 60);
}