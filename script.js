// --- 1. Bird Catalogue Data ---
const birdsData = [
    // 20 Common Birds of Manitoba
    { name: "Black-capped Chickadee", rarity: "Common", info: "A small, cute bird famous for its distinctive call. Very common year-round.", image: "" },
    { name: "American Robin", rarity: "Common", info: "One of the most widespread and recognized songbirds. Often seen hopping on lawns.", image: "" },
    { name: "House Sparrow", rarity: "Common", info: "A very adaptable and abundant bird, often found in urban areas.", image: "" },
    { name: "Blue Jay", rarity: "Common", info: "A large, beautiful blue, black, and white songbird known for its loud calls.", image: "" },
    { name: "Canada Goose", rarity: "Common", info: "Large waterfowl often seen in parks and on bodies of water.", image: "" },
    { name: "Mallard Duck", rarity: "Common", info: "The classic 'park duck', males have an iconic green head.", image: "" },
    { name: "Downy Woodpecker", rarity: "Common", info: "The smallest North American woodpecker, often found in backyard trees.", image: "" },
    { name: "European Starling", rarity: "Common", info: "Known for its iridescent plumage and complex calls. Often seen in flocks.", image: "" },
    { name: "Red-winged Blackbird", rarity: "Common", info: "Males are easily identified by black plumage and red/yellow shoulder patches.", image: "" },
    { name: "Northern Cardinal", rarity: "Common", info: "The male's brilliant red plumage makes it a favourite at feeders.", image: "" },
    { name: "Grackle (Common)", rarity: "Common", info: "Large black birds with an iridescent sheen, often flocking in large numbers.", image: "" },
    { name: "Mourning Dove", rarity: "Common", info: "Known for its soft, mournful cooing sound.", image: "" },
    { name: "American Crow", rarity: "Common", info: "Intelligent, all-black bird, common across many habitats.", image: "" },
    { name: "White-breasted Nuthatch", rarity: "Common", info: "Often seen walking head-first down tree trunks.", image: "" },
    { name: "Dark-eyed Junco", rarity: "Common", info: "Small sparrow-like bird, often called 'snowbirds' as they arrive in winter.", image: "" },
    { name: "Chickadee (Boreal)", rarity: "Common", info: "Similar to the Black-capped, but preferring coniferous forests.", image: "" },
    { name: "Chipping Sparrow", rarity: "Common", info: "Identified by its reddish-brown cap and distinctive trill song.", image: "" },
    { name: "Baltimore Oriole", rarity: "Common", info: "Known for their brilliant orange and black colours and weaving nests.", image: "" },
    { name: "Warbling Vireo", rarity: "Common", info: "A small bird with a pleasant, warbling song, often heard in treetops.", image: "" },
    { name: "Ruby-throated Hummingbird", rarity: "Common", info: "The only hummingbird species commonly found in Manitoba.", image: "" },

    // 15 Rare Birds of Manitoba
    { name: "Great Grey Owl", rarity: "Rare", info: "Manitoba's Provincial Bird. A large owl found in boreal forests.", image: "" },
    { name: "Piping Plover", rarity: "Rare", info: "Small, endangered shorebird found on sandy beaches.", image: "" },
    { name: "Loggerhead Shrike", rarity: "Rare", info: "A predatory songbird that 'impales' its prey on thorns or wire.", image: "" },
    { name: "Eared Grebe", rarity: "Rare", info: "Aquatic bird with striking gold head plumes during breeding season.", image: "" },
    { name: "Western Meadowlark", rarity: "Rare", info: "Known for its beautiful, flute-like song from open grasslands.", image: "" },
    { name: "Smith's Longspur", rarity: "Rare", info: "A migratory bird often found in the northern parts of the province.", image: "" },
    { name: "Ferruginous Hawk", rarity: "Rare", info: "The largest North American hawk, preferring open prairies.", image: "" },
    { name: "Yellow-billed Cuckoo", rarity: "Rare", info: "A slender bird known for its distinct, repetitive call.", image: "" },
    { name: "Prothonotary Warbler", rarity: "Rare", info: "Brilliant yellow warbler, a stunning sight near wooded swamps.", image: "" },
    { name: "Least Bittern", rarity: "Rare", info: "One of the smallest herons, masters of camouflage in dense marshes.", image: "" },
    { name: "Say's Phoebe", rarity: "Rare", info: "A flycatcher bird found in drier, more western parts of the province.", image: "" },
    { name: "Great Egret", rarity: "Rare", info: "A large, beautiful white wading bird, an uncommon visitor.", image: "" },
    { name: "King Rail", rarity: "Rare", info: "A shy, secretive rail found in large freshwater marshes.", image: "" },
    { name: "Red-headed Woodpecker", rarity: "Rare", info: "A striking woodpecker with a completely red head.", image: "" },
    { name: "Long-billed Curlew", rarity: "Rare", info: "A large shorebird distinguished by its extremely long, curved bill.", image: "" },

    // 5 Ultra Rare Birds of Manitoba
    { name: "Ivory Gull", rarity: "Ultra Rare", info: "An almost entirely white Arctic gull, an extremely rare winter visitor.", image: "" },
    { name: "Gyrfalcon", rarity: "Ultra Rare", info: "The largest of the falcon species, a very rare and powerful Arctic raptor.", image: "" },
    { name: "Whooping Crane", rarity: "Ultra Rare", info: "One of the rarest birds in the world, occasionally seen during migration.", image: "" },
    { name: "Ross's Gull", rarity: "Ultra Rare", info: "A beautiful small gull, pink-tinged during breeding, seen mostly in the north.", image: "" },
    { name: "Kirtland's Warbler", rarity: "Ultra Rare", info: "A highly endangered warbler with very specific breeding needs.", image: "" }
];

// --- 2. Initial Setup and Data Display ---
document.addEventListener('DOMContentLoaded', () => {
    const catalogueGrid = document.querySelector('.catalogue-grid');
    
    // Function to assign a rarity class for visual styling
    const getRarityClass = (rarity) => {
        if (rarity === 'Rare') return 'rare-bird';
        if (rarity === 'Ultra Rare') return 'ultra-rare-bird';
        return 'common-bird';
    };

    // Populate the Catalogue Grid
    birdsData.forEach(bird => {
        const card = document.createElement('div');
        card.className = `bird-card ${getRarityClass(bird.rarity.replace(/\s/g, '-').toLowerCase())}`;
        
        card.innerHTML = `
            <div class="bird-image-placeholder">No Image Available - Go Find One!</div>
            <h3>${bird.name}</h3>
            <p><strong>Rarity:</strong> ${bird.rarity}</p>
            <p>${bird.info}</p>
        `;
        catalogueGrid.appendChild(card);
    });

    // Add specific CSS for rarity levels (injecting styles dynamically for simplicity)
    const styleSheet = document.createElement('style');
    styleSheet.innerText = `
        .common-bird { border-left: 5px solid var(--sage-green); }
        .rare-bird { border-left: 5px solid var(--warm-brown); }
        .ultra-rare-bird { border-left: 5px solid var(--olive-green); box-shadow: 0 4px 15px rgba(124, 139, 85, 0.4); }
    `;
    document.head.appendChild(styleSheet);
    
    // --- 3. Certificate Logic Setup ---
    setupCertificateLogic();
});


// --- 4. Certificate Generation Logic ---
function setupCertificateLogic() {
    const certButtons = document.querySelectorAll('.cert-btn');
    const oathArea = document.getElementById('cert-oath-area');
    const nameInput = document.getElementById('user-name-input');
    const confirmBtn = document.getElementById('oath-confirm-btn');
    const canvas = document.getElementById('certificate-canvas');

    let currentCertType = '';

    // Step 1: Handle button click to reveal oath
    certButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            currentCertType = e.target.dataset.certType;
            oathArea.classList.remove('hidden');
            canvas.classList.add('hidden'); // Hide any previous certificate
            nameInput.value = ''; // Clear previous name
            
            // Update the confirmation button text based on the certificate type
            confirmBtn.innerText = `I Solemnly Swear & Generate ${currentCertType} Certificate`;
        });
    });

    // Step 2: Handle oath confirmation and name submission
    confirmBtn.addEventListener('click', () => {
        const userName = nameInput.value.trim();

        if (userName === '') {
            alert('Please enter your name to personalize the certificate!');
            return;
        }

        if (!currentCertType) {
            alert('Please select a certificate type first.');
            return;
        }

        // Proceed to generate certificate
        generateCertificate(userName, currentCertType);
        oathArea.classList.add('hidden'); // Hide the input form
        canvas.classList.remove('hidden'); // Show the generated certificate
        
        // Give time for the certificate to render, then offer download
        setTimeout(() => {
            const downloadLink = document.createElement('a');
            downloadLink.href = canvas.toDataURL('image/png');
            downloadLink.download = `BeakABoo_${currentCertType}_Certificate_${userName.replace(/\s/g, '_')}.png`;
            downloadLink.click();
        }, 100);
    });
}

// Step 3: Function to draw and generate the certificate on the Canvas
function generateCertificate(name, type) {
    const canvas = document.getElementById('certificate-canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas dimensions (A standard letter/A4 aspect ratio)
    canvas.width = 1000;
    canvas.height = 750;

    // --- Background and Border ---
    ctx.fillStyle = '#E2EAD8'; // Light mint green (Background)
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Outer border (Warm Brown)
    ctx.strokeStyle = '#9F7D4F'; 
    ctx.lineWidth = 40;
    ctx.strokeRect(20, 20, canvas.width - 40, canvas.height - 40);

    // Inner border (Olive Green)
    ctx.strokeStyle = '#7C8B55'; 
    ctx.lineWidth = 10;
    ctx.strokeRect(50, 50, canvas.width - 100, canvas.height - 100);

    // --- Text Content ---
    
    // Title
    ctx.fillStyle = '#7C8B55'; // Olive green
    ctx.font = '700 70px "Playfair Display", serif';
    ctx.textAlign = 'center';
    ctx.fillText('Beak-a-Boo Official Certificate', canvas.width / 2, 150);

    // Subtitle
    let certTitle = '';
    if (type === 'Common') certTitle = 'Certified Common Bird Finder';
    else if (type === 'Rare') certTitle = 'Certified Rare Bird Spotter';
    else if (type === 'UltraRare') certTitle = 'Master Birder of Manitoba';

    ctx.fillStyle = '#9F7D4F'; // Warm brown
    ctx.font = '700 40px "Roboto", sans-serif';
    ctx.fillText(certTitle, canvas.width / 2, 230);

    // Issued to
    ctx.fillStyle = '#333333';
    ctx.font = '30px "Roboto", sans-serif';
    ctx.fillText('This honor is hereby presented to:', canvas.width / 2, 350);

    // User Name
    ctx.fillStyle = '#7C8B55'; // Olive green
    ctx.font = '700 60px "Playfair Display", serif';
    ctx.fillText(name.toUpperCase(), canvas.width / 2, 450);

    // Achievement text
    ctx.fillStyle = '#333333';
    ctx.font = '24px "Roboto", sans-serif';
    let achievementText;
    if (type === 'Common') achievementText = 'For successfully finding and identifying 20+ Common Birds of Manitoba.';
    else if (type === 'Rare') achievementText = 'For demonstrating excellent dedication by spotting 15+ Rare Birds.';
    else if (type === 'UltraRare') achievementText = 'For the masterful achievement of tracking down 5 Ultra Rare Bird species.';

    ctx.fillText(achievementText, canvas.width / 2, 530);

    // Date
    ctx.font = '20px "Roboto", sans-serif';
    ctx.fillText(`Date Issued: ${new Date().toLocaleDateString()}`, canvas.width / 2, 600);

    // Signature Line Placeholder
    ctx.strokeStyle = '#333333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(300, 680);
    ctx.lineTo(700, 680);
    ctx.stroke();
    
    ctx.font = '20px "Roboto", sans-serif';
    ctx.fillText('The Beak-a-Boo Discovery Team', canvas.width / 2, 705);
}