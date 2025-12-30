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
            this.setupErrorHandling();

            // Wait for DOM to ensure selectors work
            if (document.readyState === 'loading') {
                await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve));
            }

            // Initialize System Modules
            this.initRouter();
            this.initIcons();

            // Core Modules Isolation Check
            await this.bootstrapModules();

            this.state.isLoaded = true;
            console.log("✅ Application Ready");
            console.groupEnd();
        } catch (error) {
            this.handleGlobalError(error);
        }
    },

    // 3. Global Error Boundary Logic
    setupErrorHandling: function () {
        window.onerror = (msg, url, lineNo, columnNo, error) => {
            this.handleGlobalError(error || msg);
            return false;
        };

        window.onunhandledrejection = (event) => {
            this.handleGlobalError(event.reason);
        };
    },

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

    // 4. Feature Modular Initialization
    bootstrapModules: async function () {
        // Core Modules order: Auth -> Profile -> Sidebar -> Map -> Chat
        const modules = [
            { name: 'Auth', ref: window.authManager },
            { name: 'Profile', ref: window.profileManager },
            { name: 'Sidebar', ref: window.sidebarManager },
            { name: 'Map', ref: window.mapManager }
        ];


        for (const mod of modules) {
            try {
                if (mod.ref && typeof mod.ref.init === 'function') {
                    console.log(`Initializing module: ${mod.name}...`);
                    await mod.ref.init();
                }
            } catch (err) {
                console.warn(`Module ${mod.name} failed:`, err);
            }
        }

        // Special handling for ChatApp (Class based)
        try {
            if (typeof ChatApp !== 'undefined') {
                console.log("Initializing ChatApp...");
                window.chatApp = new ChatApp();
                await window.chatApp.init();
            }
        } catch (err) {
            console.error("ChatApp failed:", err);
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
App.init();
