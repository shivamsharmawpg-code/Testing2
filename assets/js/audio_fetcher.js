async function getBirdAudio(scientificName) {
    // Search Wikimedia Commons for an audio file related to the species
    const searchUrl = `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(scientificName + " audio")}&srnamespace=6&format=json&origin=*`;
    
    try {
        const response = await fetch(searchUrl);
        const data = await response.json();
        
        if (data.query.search.length > 0) {
            const fileName = data.query.search[0].title;
            // Get the actual file URL
            const urlInfoUrl = `https://commons.wikimedia.org/w/api.php?action=query&titles=${encodeURIComponent(fileName)}&prop=imageinfo&iiprop=url&format=json&origin=*`;
            const infoRes = await fetch(urlInfoUrl);
            const infoData = await infoRes.json();
            const pages = infoData.query.pages;
            const pageId = Object.keys(pages)[0];
            return pages[pageId].imageinfo[0].url;
        }
    } catch (e) {
        console.error("Wikimedia fetch error:", e);
    }
    return null;
}

// Example: getBirdAudio("Poecile atricapillus").then(url => console.log(url));
