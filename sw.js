const CACHE_NAME = 'beak-a-boo-v1';
const ASSETS = [
    './',
    './index.html',
    './assets/css/style.css',
    './assets/js/script.js',
    './assets/js/birds.js',
    './assets/images/logo.png',
    './catalogue/index.html',
    './trails/index.html',
    './about/index.html',
    './quickstart/index.html',
    './certificates/index.html'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(cache => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
        .then(response => {
            return response || fetch(event.request);
        })
    );
});
