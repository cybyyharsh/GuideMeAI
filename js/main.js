class ChatApp {
    constructor() {
        this.cacheSelectors();
        this.locationContext = { city: "Agra", state: "Uttar Pradesh", country: "India" };
        this.conversationHistory = [];
    }

    cacheSelectors() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.voicePageBtn = document.getElementById('voicePageBtn');
        this.voiceStatus = document.getElementById('voiceStatus');
        this.voiceTranscript = document.getElementById('voiceTranscript');
        this.miniVoiceBtn = document.getElementById('miniVoiceBtn');
        this.storyFab = document.getElementById('storyFab');
        this.storyView = document.getElementById('view-story');
        this.storyContent = document.getElementById('storyContent');
        this.closeStoryBtn = document.getElementById('closeStoryBtn');
    }

    init() {
        try {
            console.log("💬 Initializing Chat & Explorer...");
            this.bindEvents();
            this.initHeritageExplorer();
            this.initVoiceLinking();
        } catch (e) {
            console.error("ChatApp Init Failed:", e);
        }
    }

    initVoiceLinking() {
        if (window.voiceManager) {
            window.voiceManager.init(
                (text) => this.handleVoiceInput(text),
                (status, context) => this.handleVoiceState(status, context)
            );
        }
    }

    bindEvents() {
        this.sendButton?.addEventListener('click', () => this.sendMessage());
        this.messageInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        this.miniVoiceBtn?.addEventListener('click', () => {
            App.switchView('view-voice');
            window.voiceManager.toggleListening();
        });

        this.voicePageBtn?.addEventListener('click', () => {
            window.voiceManager.toggleListening();
        });

        document.getElementById('closeMapBtn')?.addEventListener('click', () => this.toggleMap(false));

        this.storyFab?.addEventListener('click', () => this.openStoryMode());
        this.closeStoryBtn?.addEventListener('click', () => this.closeStoryMode());
        document.getElementById('exportStoryBtn')?.addEventListener('click', () => this.exportStory());

        this.storyView?.addEventListener('scroll', () => this.handleStoryScroll());
    }

    // --- MAP & UI HELPERS ---

    toggleMap(show) {
        const panel = document.getElementById('mapPanel');
        if (!panel) return;

        if (show) {
            panel.classList.add('visible');
            setTimeout(() => {
                if (window.mapManager) window.mapManager.invalidateSize();
            }, 300);
        } else {
            panel.classList.remove('visible');
        }
    }

    // --- HERITAGE EXPLORER (Modern Discovery Grid) ---

    initHeritageExplorer() {
        const grid = document.getElementById('stateGrid');
        if (!grid || !window.HERITAGE_DATA) return;

        grid.innerHTML = '';

        // Flatten cities for the explorer
        const cities = [];
        window.HERITAGE_DATA.forEach(state => {
            state.cities.forEach(city => {
                cities.push({ ...city, state: state.state });
            });
        });

        cities.forEach((city, index) => {
            const card = document.createElement('div');
            card.className = 'heritage-card';

            // Randomly assign a badge for flavor
            const badges = ['Heritage', 'Popular', 'Trending', 'Must Visit', 'Ancient'];
            const badge = index % 4 === 0 ? `<div class="card-badge">${badges[index % 5]}</div>` : '';

            card.innerHTML = `
                ${badge}
                <img src="${city.image}" alt="${city.monument}" loading="lazy" 
                     onerror="this.src='images/fallback.jpg'">

                <div class="card-overlay"></div>
                <div class="city-pill">${city.city}</div>
            `;

            card.addEventListener('click', () => {
                const query = `Tell me about ${city.city} heritage`;
                if (this.messageInput) {
                    this.messageInput.value = query;
                    this.messageInput.focus();
                    // Scroll to chat
                    App.switchView('view-guide');
                }

                // Update context silently
                this.locationContext = {
                    city: city.city,
                    state: city.state,
                    monument: city.monument,
                    country: "India"
                };

                if (window.mapManager) {
                    window.mapManager.setView([city.lat, city.lng], 12, { animate: true });
                    window.mapManager.plotMarkers([{
                        name: city.monument,
                        lat: city.lat,
                        lng: city.lng,
                        type: 'monument'
                    }]);
                }
            });

            grid.appendChild(card);
        });
    }


    // --- CHAT LOGIC ---


    async sendMessage(isVoice = false) {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Basic Greeting Detection
        const lowerMsg = message.toLowerCase();
        if (["hi", "hello", "hey", "namaste", "hola"].includes(lowerMsg)) {
            this.addMessage(message, 'user');
            this.messageInput.value = '';
            this.addMessage("Hello! I'm your GuideMeAI companion. What would you like to explore today?", 'bot');
            this.addSuggestionChips(['Explore a city', 'Find places', 'Ask history', 'Get directions']);
            return;
        }

        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.showTypingIndicator();
        this.setInputState(false);

        this.conversationHistory.push({ role: 'user', content: message, timestamp: new Date() });

        try {
            const userContext = typeof authManager !== 'undefined' ? authManager.getUserContext() : {};
            const profileContext = typeof profileManager !== 'undefined' ? profileManager.getProfileContext() : {};

            const response = await API.sendChatMessage(message, {
                ...userContext,
                profile: profileContext,
                location_context: this.locationContext,
                mode: isVoice ? 'voice' : 'text',
                history: this.conversationHistory.slice(-6)
            });

            this.hideTypingIndicator();

            if (!response) {
                this.addMessage("I'm running in offline mode right now (API disconnected). You can still browse the Heritage Explorer!", 'bot');
                return;
            }

            if (response.location_context) this.locationContext = response.location_context;


            this.addMessage(response.response, 'bot', response.agent_type);
            this.conversationHistory.push({ role: 'assistant', content: response.response, timestamp: new Date() });

            // Trigger suggestion chips on greeting
            if (response.intent === 'greeting') {
                this.addSuggestionChips(['Explore a city', 'Find places', 'Ask history', 'Get directions']);
            }

            if (response.map_data?.places && window.mapManager) {
                window.mapManager.plotMarkers(response.map_data.places);
            }

            if (isVoice || window.voiceManager.isListening) {
                window.voiceManager.playResponse(this.cleanForSpeech(response.response));
            }
        } catch (error) {
            console.error('Chat Error:', error);
            this.hideTypingIndicator();
            this.addMessage("Sorry, I'm having trouble connecting to the guide service.", 'bot');
        } finally {
            this.setInputState(true);
        }
    }

    addMessage(content, sender, agentType = null) {
        if (!this.chatMessages) return;

        const msgDiv = document.createElement('div');
        msgDiv.className = `msg-row ${sender}`;

        if (sender === 'bot') {
            msgDiv.innerHTML = `
                <div class="msg-card bot">
                    <div class="msg-content">${this.formatContent(content)}</div>
                    <div class="speaker-icon" onclick="window.voiceManager.playResponse(\`${this.cleanForSpeech(content).replace(/`/g, "'")}\`)">
                        <i data-lucide="volume-2" class="w-3 h-3"></i> Listen
                    </div>
                </div>
            `;
        } else {
            msgDiv.innerHTML = `<div class="msg-card user"><div class="msg-content"><p>${content}</p></div></div>`;
        }

        this.chatMessages.appendChild(msgDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    addSuggestionChips(suggestions) {
        const chipContainer = document.createElement('div');
        chipContainer.className = 'suggestion-chips';

        suggestions.forEach(text => {
            const btn = document.createElement('button');
            btn.className = 'chip';
            btn.innerText = text;
            btn.onclick = () => {
                if (this.messageInput) {
                    this.messageInput.value = text;
                    this.sendMessage();
                    chipContainer.remove();
                }
            };
            chipContainer.appendChild(btn);
        });

        this.chatMessages.appendChild(chipContainer);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }


    // --- VOICE UI SYNC ---

    handleVoiceState(status, context) {
        if (!this.voiceStatus) return;

        this.voicePageBtn?.classList.remove('listening', 'speaking');
        this.voiceStatus.textContent = "Click mic to speak";

        if (context.isListening) {
            this.voicePageBtn?.classList.add('listening');
            this.voiceStatus.textContent = "Listening...";
        } else if (context.isSpeaking) {
            this.voicePageBtn?.classList.add('speaking');
            this.voiceStatus.textContent = "Speaking...";
        }
    }

    handleVoiceInput(text) {
        if (this.voiceTranscript) this.voiceTranscript.textContent = `"${text}"`;
        this.messageInput.value = text;
        this.sendMessage(true);
    }

    // --- FORMATTING HELPERS ---

    cleanForSpeech(text) {
        return text.replace(/\*\*/g, '').replace(/•/g, '').replace(/\n+/g, '. ').substring(0, 500);
    }

    formatContent(content) {
        // Basic Markdown Support
        let html = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/• (.*?)(?=\n|$)/g, '<li>$1</li>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>');

        if (html.includes('<li>')) html = `<ul class="list-disc ml-4">${html}</ul>`;
        return html;
    }

    showTypingIndicator() {
        const div = document.createElement('div');
        div.id = 'typingIndicator';
        div.className = 'msg-row';
        div.innerHTML = `<div class="msg-card"><div class="flex space-x-1"><div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce"></div><div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce [animation-delay:0.1s]"></div><div class="w-2 h-2 bg-slate-300 rounded-full animate-bounce [animation-delay:0.2s]"></div></div></div>`;
        this.chatMessages?.appendChild(div);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    hideTypingIndicator() {
        document.getElementById('typingIndicator')?.remove();
    }

    setInputState(enabled) {
        if (this.messageInput) this.messageInput.disabled = !enabled;
        if (enabled) this.messageInput?.focus();
    }

    renderSessions() {
        const list = document.getElementById('sessionsList');
        if (!list) return;
        list.innerHTML = this.conversationHistory.length === 0 ? '<div class="p-4 text-center text-slate-400">No history yet.</div>' : '';
        this.conversationHistory.forEach(msg => {
            const item = document.createElement('div');
            item.className = 'session-item p-3 border-b border-slate-100 flex justify-between items-center';
            item.innerHTML = `<span><strong>${msg.role}:</strong> ${msg.content.substring(0, 50)}...</span>`;
            list.appendChild(item);
        });
    }

    // --- STORY MODE (Placeholder for now) ---
    openStoryMode() { this.storyView?.classList.add('active'); }
    closeStoryMode() { this.storyView?.classList.remove('active'); }
    handleStoryScroll() { }
    exportStory() { alert("Story feature in development!"); }
}
