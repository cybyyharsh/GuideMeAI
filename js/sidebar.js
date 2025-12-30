
// Sidebar Functionality Module
window.sidebarManager = {
    currentRating: 0,

    init: function () {
        try {
            console.log('📂 Initializing Sidebar Module...');
            this.showMenu();
            if (typeof lucide !== 'undefined') lucide.createIcons();
            this.bindEvents();
        } catch (e) {
            console.error("Sidebar Init Error", e);
        }
    },

    bindEvents: function () {
        // Any specific events not handled by inline onclicks
    },

    // proxy methods (keeping original names for compatibility with current HTML)
    navigateTo: function (panelId) {
        // Hide Main Menu
        const menu = document.getElementById('sidebar-menu');
        const title = document.getElementById('sidebarTitle');
        if (menu) menu.classList.add('hidden');

        // Hide all panels first
        ['panel-distance', 'panel-experience', 'panel-feedback'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.add('hidden');
            if (el) el.classList.remove('flex');
        });

        // Show Target Panel
        const target = document.getElementById(panelId);
        if (target) {
            target.classList.remove('hidden');
            target.classList.add('flex');
        }

        if (title) title.textContent = 'Back to Menu';
    },

    showMenu: function () {
        // Show Main Menu
        const menu = document.getElementById('sidebar-menu');
        if (menu) menu.classList.remove('hidden');

        // Hide all panels
        ['panel-distance', 'panel-experience', 'panel-feedback'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.add('hidden');
            if (el) el.classList.remove('flex');
        });

        const title = document.getElementById('sidebarTitle');
        if (title) title.textContent = 'Menu';
    },

    openProfile: function () {
        const closeBtn = document.getElementById('closeSidebar');
        if (closeBtn) closeBtn.click();

        if (typeof authManager !== 'undefined') {
            setTimeout(() => authManager.showProfileModal(), 300);
        }
    },

    calculateDistance: async function () {
        const start = document.getElementById('distStart').value;
        const end = document.getElementById('distEnd').value;
        const resDiv = document.getElementById('distResult');
        const resVal = document.getElementById('distValue');
        const resRoute = document.getElementById('distanceRoute');
        const btn = document.querySelector('#panel-distance button');

        if (!start || !end) return alert('Enter both locations.');

        btn.textContent = 'Calculating...';
        btn.disabled = true;

        try {
            if (!window.mapManager) throw new Error("Map not ready.");
            const routeData = await window.mapManager.drawRoute(start, end);
            resVal.textContent = `${routeData.distance} km`;
            if (resRoute) {
                const hours = Math.floor(routeData.duration / 60);
                const mins = routeData.duration % 60;
                resRoute.textContent = hours > 0 ? `${hours}h ${mins}m` : `${mins} min`;
            }
            resDiv.classList.remove('hidden');
        } catch (error) {
            alert(error.message || "Calculation failed.");
        } finally {
            btn.textContent = 'Calculate Distance';
            btn.disabled = false;
        }
    },

    submitExperience: function () {
        const loc = document.getElementById('expLoc').value;
        const text = document.getElementById('expText').value;
        if (!loc || !text) return alert('Fill all fields.');

        const btn = document.querySelector('#panel-experience button');
        btn.textContent = 'Sharing...';
        btn.disabled = true;

        setTimeout(() => {
            btn.textContent = '✓ Shared';
            setTimeout(() => {
                btn.textContent = 'Share Experience';
                btn.disabled = false;
                document.getElementById('experienceForm').reset();
                this.showMenu();
            }, 1500);
        }, 1000);
    },

    rate: function (n) {
        this.currentRating = n;
        for (let i = 1; i <= 5; i++) {
            const star = document.getElementById(`star${i}`);
            if (star) {
                if (i <= n) {
                    star.classList.add('text-yellow-400', 'fill-current');
                    star.classList.remove('text-slate-200');
                } else {
                    star.classList.remove('text-yellow-400', 'fill-current');
                    star.classList.add('text-slate-200');
                }
            }
        }
    },

    submitFeedback: function () {
        const msg = document.getElementById('feedbackMsg').value;
        if (this.currentRating === 0) return alert('Please rate us.');

        const btn = document.querySelector('#panel-feedback button');
        btn.textContent = 'Sending...';
        btn.disabled = true;

        setTimeout(() => {
            btn.textContent = '✓ Thank You';
            setTimeout(() => {
                btn.textContent = 'Send Feedback';
                btn.disabled = false;
                document.getElementById('feedbackMsg').value = '';
                this.rate(0);
                this.showMenu();
            }, 1500);
        }, 1000);
    }
};

// Map Sidebar object to global window property for HTML access
window.Sidebar = window.sidebarManager;

