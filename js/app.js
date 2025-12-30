/**
 * GuideMeAI - Master Application Controller
 * Handles bootstrapping, module orchestration, and global state.
 */

const App = {
    // 1. Central UI State
    state: {
        selectedState: null,
        selectedCity: null,
        activeFeature: 'guide',
        authStatus: 'guest',
        isLoaded: false,
        isMapVisible: false,
        lastError: null
    },

    // 2. Application Entry Point
    init: async function () {
        try {
            console.group("🚀 GuideMeAI Bootstrap");

            // Basic UI setup
            this.initRouter();
            this.initIcons();

            // Safe module initialization
            this.safe(() => window.authManager?.init());
            this.safe(() => window.profileManager?.init());
            this.safe(() => window.sidebarManager?.init());
            this.safe(() => window.mapManager?.init());

            // Initialize Chat
            this.safe(async () => {
                if (typeof ChatApp !== 'undefined') {
                    window.chatApp = new ChatApp();
                    await window.chatApp.init();
                }
            });

            this.state.isLoaded = true;
            console.log("✅ Application Ready");
            console.groupEnd();
        } catch (error) {
            console.error("App init failed:", error);
            this.showFallbackUI();
        }
    },

    safe: function (fn) {
        try {
            if (typeof fn === "function") fn();
        } catch (e) {
            console.warn(`Feature initialization failed`, e);
        }
    },

    showFallbackUI: function () {
        document.body.innerHTML = `
            <div style="padding:40px;font-family:sans-serif;text-align:center;background:#f8fafc;height:100vh;display:flex;flex-direction:column;justify-content:center;">
                <h2 style="color:#1e293b">GuideMeAI</h2>
                <p style="color:#64748b">Something went wrong while starting the app. Please refresh the page.</p>
                <button onclick="location.reload()" style="padding:10px 20px;background:#2563eb;color:white;border:none;border-radius:8px;cursor:pointer;margin:0 auto;">Reload</button>
            </div>
        `;
    },

    // 3. Global Error Boundary Logic (Retaining original map panel logic)
    handleGlobalError: function (error) {
        console.error("CRITICAL FAILURE:", error);
        this.state.lastError = error;

        const boundary = document.getElementById('error-boundary');
        const message = document.getElementById('error-message');

        if (boundary && message) {
            boundary.style.display = 'flex';
            message.textContent = typeof error === 'string' ? error : (error.message || "An unexpected error occurred.");
        }
    },





    initIcons: function () {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    },

    // 5. Unified Routing Logic
    initRouter: function () {
        const navItems = document.querySelectorAll('.nav-item');
        const views = document.querySelectorAll('.view-section');

        navItems.forEach(link => {
            link.addEventListener('click', (e) => {
                const viewId = link.getAttribute('data-view');
                if (!viewId) return;

                e.preventDefault();
                this.switchView(viewId);
            });
        });

        // Mobile Menu Toggle
        const menuBtn = document.getElementById('mobileMenuBtn');
        const navLinks = document.getElementById('navLinks');
        if (menuBtn && navLinks) {
            menuBtn.addEventListener('click', () => {
                navLinks.classList.toggle('mobile-open');
            });
        }
    },

    switchView: function (viewId) {
        // Update State
        this.state.activeFeature = viewId.replace('view-', '');

        // Update Nav UI
        document.querySelectorAll('.nav-item').forEach(l => {
            l.classList.remove('active');
            if (l.getAttribute('data-view') === viewId) l.classList.add('active');
        });

        // Update View Visibility
        document.querySelectorAll('.view-section').forEach(section => {
            section.classList.remove('active-view');
        });

        const targetView = document.getElementById(viewId);
        if (targetView) targetView.classList.add('active-view');

        // Close Mobile Menu if open
        const navLinks = document.getElementById('navLinks');
        if (navLinks) navLinks.classList.remove('mobile-open');

        // Special Module Hooks
        if (viewId === 'view-sessions' && window.chatApp) {
            window.chatApp.renderSessions();
        }

        console.log(`Switched view to: ${viewId}`);
    }
};

// Start the App
document.addEventListener("DOMContentLoaded", () => {
    App.init();
});

