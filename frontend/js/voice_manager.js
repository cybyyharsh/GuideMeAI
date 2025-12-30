/**
 * Voice Module - Handles STT and TTS
 */
window.voiceManager = {
    recognition: null,
    isListening: false,
    isSpeaking: false,
    synth: window.speechSynthesis,
    onInput: null,
    onStateChange: null,

    init: function (onInput, onStateChange) {
        try {
            console.log("🎤 Initializing Voice Module...");
            this.onInput = onInput;
            this.onStateChange = onStateChange;

            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                this.recognition = new SpeechRecognition();
                this.recognition.continuous = false;
                this.recognition.interimResults = false;
                this.recognition.lang = 'en-IN';

                this.recognition.onstart = () => {
                    this.isListening = true;
                    this.updateUI("listening");
                };

                this.recognition.onend = () => {
                    this.isListening = false;
                    this.updateUI("idle");
                };

                this.recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    if (transcript && this.onInput) this.onInput(transcript);
                };

                this.recognition.onerror = (event) => {
                    console.error("Speech Error:", event.error);
                    this.isListening = false;
                    this.updateUI("error");
                };
            } else {
                console.warn("Speech API Not Supported");
                this.updateUI("unsupported");
            }
        } catch (e) {
            console.error("Voice Init Failed", e);
        }
    },

    toggleListening: function () {
        if (!this.recognition) return alert("Voice recognition not supported in this browser.");

        if (this.isListening) {
            this.recognition.stop();
        } else {
            this.stopSpeaking();
            try {
                this.recognition.start();
            } catch (e) {
                console.error("Recognition start failed", e);
            }
        }
    },

    playResponse: function (text) {
        if (!this.synth) return;
        this.stopSpeaking();

        this.isSpeaking = true;
        this.updateUI("speaking");

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-IN';
        utterance.onend = () => {
            this.isSpeaking = false;
            this.updateUI("idle");
        };
        utterance.onerror = () => {
            this.isSpeaking = false;
            this.updateUI("error");
        };

        this.synth.speak(utterance);
    },

    stopSpeaking: function () {
        if (this.synth) this.synth.cancel();
        this.isSpeaking = false;
        this.updateUI("idle");
    },

    updateUI: function (status) {
        if (this.onStateChange) {
            this.onStateChange(status, {
                isListening: this.isListening,
                isSpeaking: this.isSpeaking
            });
        }
    }
};

