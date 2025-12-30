/**
 * User Profile Management Module
 * Privacy-safe design for personalization without intrusiveness.
 */
window.profileManager = {
    profile: {
        name: "",
        language: "hinglish",
        homeState: "",
        interests: [],
        responseStyle: "concise"
    },

    init: async function () {
        try {
            console.log("👤 Initializing Profile Module...");
            this.loadProfile();
            this.populateStateDropdown();
            this.setupFormListeners();
            this.syncFormWithProfile();
        } catch (e) {
            console.error("Profile Init Failed", e);
        }
    },

    loadProfile: function () {
        const saved = localStorage.getItem('userProfile');
        if (saved) {
            this.profile = { ...this.profile, ...JSON.parse(saved) };
        }
    },

    saveProfile: function (data) {
        this.profile = { ...this.profile, ...data };
        localStorage.setItem('userProfile', JSON.stringify(this.profile));
        this.notifySuccess();
    },

    populateStateDropdown: function () {
        const select = document.getElementById('profState');
        if (!select || !window.HERITAGE_DATA) return;

        // Clear existing except first
        select.innerHTML = '<option value="">Select your home state</option>';

        const states = window.HERITAGE_DATA.map(d => d.state).sort();
        states.forEach(state => {
            const option = document.createElement('option');
            option.value = state;
            option.textContent = state;
            select.appendChild(option);
        });
    },

    setupFormListeners: function () {
        const form = document.getElementById('profileForm');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const interests = Array.from(document.querySelectorAll('#profInterests input[type="checkbox"]:checked'))
                .map(cb => cb.value);

            const style = document.querySelector('input[name="profStyle"]:checked')?.value || "concise";

            const data = {
                name: document.getElementById('profName').value.trim(),
                language: document.getElementById('profLang').value,
                homeState: document.getElementById('profState').value,
                interests: interests,
                responseStyle: style
            };

            this.saveProfile(data);
        });
    },

    syncFormWithProfile: function () {
        const fields = {
            profName: this.profile.name,
            profLang: this.profile.language,
            profState: this.profile.homeState
        };

        for (const [id, val] of Object.entries(fields)) {
            const el = document.getElementById(id);
            if (el) el.value = val;
        }

        // Checklist
        document.querySelectorAll('#profInterests input[type="checkbox"]').forEach(cb => {
            cb.checked = this.profile.interests.includes(cb.value);
        });

        // Radios
        const radio = document.querySelector(`input[name="profStyle"][value="${this.profile.responseStyle}"]`);
        if (radio) radio.checked = true;
    },

    getProfileContext: function () {
        // Return only what's needed for AI personalization
        return {
            ...this.profile,
            isProfileActive: !!(this.profile.name || this.profile.homeState || this.profile.interests.length > 0)
        };
    },

    notifySuccess: function () {
        // Simple UI feedback
        const btn = document.querySelector('#profileForm button[type="submit"]');
        if (!btn) return;

        const originalText = btn.textContent;
        btn.textContent = "Profile Saved! ✅";
        btn.classList.add('bg-green-600');

        setTimeout(() => {
            btn.textContent = originalText;
            btn.classList.remove('bg-green-600');
        }, 2000);
    }
};
