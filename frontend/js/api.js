/**
 * Global API Service
 */
window.API = {
    BASE_URL: "/api",

    async request(endpoint, method = "POST", body = null) {
        const options = {
            method,
            headers: { "Content-Type": "application/json" }
        };

        if (body) options.body = JSON.stringify(body);

        try {
            const url = endpoint.startsWith('/') ? `${this.BASE_URL}${endpoint}` : `${this.BASE_URL}/${endpoint}`;
            const res = await fetch(url, options);

            if (!res.ok) {
                const errorData = await res.json().catch(() => ({ error: "Network Error" }));
                const err = new Error(errorData.message || errorData.error || `HTTP ${res.status}`);
                err.status = res.status;
                throw err;
            }

            return await res.json();
        } catch (err) {
            console.error("🌐 API Error:", err);
            throw err;
        }
    },

    sendChatMessage(message, context = {}) {
        return this.request("/chat/", "POST", { message, ...context });
    },

    createGuestSession() {
        return this.request("/auth/guest");
    },

    signup(data) {
        return this.request("/auth/signup", "POST", data);
    },

    login(data) {
        return this.request("/auth/login", "POST", data);
    }
};
