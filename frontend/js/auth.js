// Authentication Management Module
window.authManager = {
    currentUser: null,
    sessionToken: null,

    init: function () {
        try {
            console.log("🔐 Initializing Auth Module...");
            this.loadSession();
            this.setupEventListeners();
            if (!this.currentUser) this.createGuestSession();
            this.updateUI();
        } catch (e) {
            console.error("Auth Init Failed", e);
        }
    },

    setupEventListeners: function () {
        const addListener = (id, event, callback) => {
            document.getElementById(id)?.addEventListener(event, callback);
        };

        addListener('loginBtn', 'click', () => this.showLoginModal());
        addListener('signupBtn', 'click', () => this.showSignupModal());
        addListener('profileBtn', 'click', () => this.showProfileModal());
        addListener('logoutBtn', 'click', () => this.logout());

        // Modal logic
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) e.target.style.display = 'none';
        });
    },

    async createGuestSession() {
        try {
            const data = await API.createGuestSession();
            if (data.status === 'success') {
                this.sessionToken = data.session_data.session_token;
                localStorage.setItem('sessionToken', this.sessionToken);
            }
        } catch (error) {
            console.warn('Guest session creation failed (Check API)');
        }
    },

    showLoginModal() { /* ... Logic ... */ },
    showSignupModal() { /* ... Logic ... */ },
    showProfileModal() { /* ... Logic ... */ },

    logout: function () {
        this.currentUser = null;
        localStorage.removeItem('currentUser');
        this.createGuestSession();
        this.updateUI();
    },

    loadSession: function () {
        const savedUser = localStorage.getItem('currentUser');
        if (savedUser) this.currentUser = JSON.parse(savedUser);
        this.sessionToken = localStorage.getItem('sessionToken');
    },

    updateUI: function () {
        // Update state in App
        if (window.App) App.state.authStatus = this.currentUser ? 'member' : 'guest';
    },

    getUserContext: function () {
        if (this.currentUser) return { user_id: this.currentUser.user_id, user_type: 'registered' };
        return { session_token: this.sessionToken, user_type: 'guest' };
    }
};
