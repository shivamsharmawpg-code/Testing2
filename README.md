# Beak-a-boo: Manitoba Birdwatching Field Guide 🦉

Welcome to the official repository for **Beak-a-boo**, a student-run Junior Achievement company from Windsor Park Collegiate in Winnipeg, Manitoba.

Beak-a-boo is dedicated to helping families explore Manitoba birds with beginner-friendly kits, trail guides, and digital learning resources.

## 🚀 Features

This project is a fully-featured **Progressive Web App (PWA)** built with vanilla web technologies.

*   **Offline Support:** A custom Service Worker caches the site, allowing you to use the bird catalogue and trail maps deep in the woods without cell service!
*   **Personal Bird Journal:** Track your progress using the "Mark as Spotted" feature. Your memory is saved locally on your device (`localStorage`).
*   **Interactive Trail Maps:** Integrated Leaflet maps detailing the best birdwatching trails across Winnipeg.
*   **High-End Design:** Smooth animations powered by GSAP, modern CSS styling, and glassmorphism UI elements.
*   **Certificate Generator:** A dynamic canvas engine that generates highly ornate, downloadable PDF-style certificates for young explorers (complete with a swear-word filter!).

## 📁 Project Structure

We maintain a clean, organized static file architecture:

```
├── assets/
│   ├── css/      # Global stylesheets and modern variables
│   ├── js/       # Core logic, bird data, and PWA setup
│   └── images/   # Optimized webp/jpg assets
├── catalogue/    # The main bird database and journal
├── trails/       # Interactive map and trail guides
├── certificates/ # The dynamic certificate generator engine
├── tools/        # Python utility scripts for build/maintenance
├── manifest.json # PWA configuration
└── sw.js         # Service Worker for offline caching
```

## 🛠️ Development

This is a pure static website. No complex build tools or `npm install` are required to run the basics!

1. Clone the repository.
2. Open `index.html` in your browser.
*(Note: To test the Service Worker and PWA offline features, you must serve the files over a local web server, e.g., `npx serve` or Python's `python -m http.server`).*

## 🌿 Junior Achievement

This project was developed under the Junior Achievement (JA) company program to foster entrepreneurial skills, environmental awareness, and family bonding. 

**Go outside, look up, and play hide-and-seek with nature!**
