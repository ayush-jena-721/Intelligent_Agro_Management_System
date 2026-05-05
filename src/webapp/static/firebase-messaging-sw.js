// Firebase Messaging Service Worker
// Handles background notifications when browser is closed

importScripts('https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.0/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyDH9GJ6Mlya2_3-RBQhvcZMdkB5CnWbrLo",
    authDomain: "megh-dristi.firebaseapp.com",
    databaseURL: "https://megh-dristi-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "megh-dristi",
    storageBucket: "megh-dristi.firebasestorage.app",
    messagingSenderId: "356932827712",
    appId: "1:356932827712:web:a3002d53fa8c47c1b4bda5"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/icon-192x192.png',
        badge: '/badge-72x72.png',
        tag: payload.data?.type || 'general',
        requireInteraction: payload.data?.type === 'critical',
        data: payload.data,
        actions: [
            {
                action: 'open',
                title: 'Open Dashboard'
            },
            {
                action: 'dismiss',
                title: 'Dismiss'
            }
        ]
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'open' || !event.action) {
        const urlToOpen = new URL('/dashboard', self.location.origin).href;
        
        event.waitUntil(
            clients.matchAll({type: 'window'}).then((windowClients) => {
                for (let client of windowClients) {
                    if (client.url === urlToOpen && 'focus' in client) {
                        return client.focus();
                    }
                }
                if (clients.openWindow) {
                    return clients.openWindow(urlToOpen);
                }
            })
        );
    }
});