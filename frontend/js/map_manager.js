// Set global reference but don't auto-init
window.mapManager = {
    map: null,
    markers: [],

    init: async function () {
        try {
            if (this.map) return;
            console.log("📍 Initializing Map Module...");

            const container = document.getElementById('mapView');
            if (!container) throw new Error("Map container 'mapView' not found");

            this.map = L.map('mapView', {
                zoomControl: false
            }).setView([22.5937, 78.9629], 5);

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: "© OpenStreetMap"
            }).addTo(this.map);

            this.bindEvents();
            await this.loadLocations();
        } catch (error) {
            console.error("Map Initialization Error:", error);
        }
    },

    bindEvents: function () {
        document.getElementById('zoomIn')?.addEventListener('click', () => this.map.zoomIn());
        document.getElementById('zoomOut')?.addEventListener('click', () => this.map.zoomOut());
    },

    loadLocations: async function () {
        try {
            const response = await fetch('/api/map/locations');
            const locations = await response.json();
            if (locations && !locations.error) {
                this.plotMarkers(locations);
            }
        } catch (error) {
            console.warn("Could not load map locations (Backend might be offline)");
        }
    },

    plotMarkers: function (locations, clearExisting = true) {
        if (!this.map) return;

        if (clearExisting) {
            this.markers.forEach(m => this.map.removeLayer(m));
            this.markers = [];
        }

        const cityIcon = L.divIcon({
            html: '<div class="w-8 h-8 bg-[#C04000] rounded-full border-2 border-white shadow-xl flex items-center justify-center text-white"><i data-lucide="map-pin" class="w-4 h-4"></i></div>',
            className: 'custom-div-icon',
            iconSize: [32, 32],
            iconAnchor: [16, 32]
        });

        locations.forEach(loc => {
            const lat = loc.latitude || loc.lat;
            const lng = loc.longitude || loc.lng;
            const name = loc.name || loc.place_name || 'Location';

            if (lat && lng) {
                const marker = L.marker([lat, lng], { icon: cityIcon })
                    .bindPopup(`
                        <div class="custom-popup p-2">
                            <h4 class="font-bold text-slate-900">${name}</h4>
                            <button class="marker-btn w-full mt-2" onclick="window.chatApp.triggerQuery('Tell me more about ${name}')">
                                Ask about this place
                            </button>
                        </div>
                    `, { className: 'custom-leaflet-popup' })
                    .addTo(this.map);

                this.markers.push(marker);
            }
        });

        if (typeof lucide !== 'undefined') lucide.createIcons();
    },

    invalidateSize: function () {
        if (this.map) this.map.invalidateSize();
    },

    setView: function (coords, zoom, options) {
        if (this.map) this.map.setView(coords, zoom, options);
    },

    drawRoute: async function (startQuery, endQuery) {
        // Keeping the logic but making it safer
        try {
            const startCoords = await this.getCoordinates(startQuery);
            const endCoords = await this.getCoordinates(endQuery);
            if (!startCoords || !endCoords) throw new Error("Locations not found");

            if (this.currentRouteLayer) this.map.removeLayer(this.currentRouteLayer);

            const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${startCoords.lng},${startCoords.lat};${endCoords.lng},${endCoords.lat}?overview=full&geometries=geojson`;
            const response = await fetch(osrmUrl);
            const data = await response.json();

            if (data.code === 'Ok' && data.routes.length > 0) {
                const route = data.routes[0];
                this.currentRouteLayer = L.geoJSON(route.geometry, {
                    style: { color: '#C04000', weight: 5, opacity: 0.8 }
                }).addTo(this.map);
                this.map.fitBounds(this.currentRouteLayer.getBounds(), { padding: [50, 50] });
                return {
                    distance: (route.distance / 1000).toFixed(1),
                    duration: Math.round(route.duration / 60)
                };
            }
        } catch (e) {
            console.error("Routing error:", e);
            throw e;
        }
    },

    getCoordinates: async function (query) {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
        const data = await res.json();
        return data && data.length > 0 ? { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) } : null;
    }
};
