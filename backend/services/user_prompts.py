class UserPrompts:
    """
    User Flow Prompt Templates for LLM Guidance
    These prompts are designed to guide the AI in providing appropriate responses
    for different user authentication and profile management scenarios.
    """
    
    def get_guest_welcome_prompt(self):
        """Welcome message for guest users"""
        return """Namaste! Main aapka local Agra guide hun. Aap guest ke roop mein explore kar sakte hain - main aapko city ke baare mein sab kuch bata sakta hun. Food places, historical monuments, traffic tips, aur local culture ke baare mein jo bhi jaanna ho, bas puchiye! Agar aap personalized recommendations chahte hain aur apni preferences save karna chahte hain, toh aap account bana sakte hain. Abhi ke liye, kya jaanna chahenge Agra ke baare mein?"""
    
    def get_login_assistant_prompt(self):
        """Guidance for login process"""
        return """Login karne ke liye aap apna email ya mobile number use kar sakte hain. Agar aap pehle se registered hain, toh bas apni details enter kariye. Login karne ke baad aapko personalized recommendations milenge jo aapki preferences ke according honge - jaise budget range, travel style, aur language preference. Agar koi problem aa rahi hai login mein, toh guest mode mein bhi explore kar sakte hain."""
    
    def get_signup_assistant_prompt(self):
        """Guidance for signup process"""
        return """Account banane ke liye bas kuch basic details chahiye - naam, email ya mobile number. Iske baad aap apni preferences set kar sakte hain jaise budget range (budget/mid-range/luxury), travel style (solo/family/business), aur language preference. Yeh sab information sirf aapko better recommendations dene ke liye use hoti hai. Aapka data safe rehta hai aur sirf local city guide features ke liye use hota hai."""
    
    def get_profile_description_prompt(self, profile_data):
        """Description of user profile and preferences"""
        first_name = profile_data.get('first_name', 'User')
        budget_range = profile_data.get('budget_range', 'mid_range')
        travel_style = profile_data.get('travel_style', 'solo')
        language_pref = profile_data.get('language_preference', 'hinglish')
        preferred_city = profile_data.get('preferred_city', 'Agra')
        
        return f"""Aapka profile ready hai, {first_name}! Aapki current preferences: Budget Range - {budget_range}, Travel Style - {travel_style}, Language - {language_pref}, Preferred City - {preferred_city}. In preferences ke basis par main aapko customized recommendations deta hun. Jaise agar aapka budget range 'budget' hai toh main street food aur budget-friendly places suggest karunga. Family travel style hai toh family-friendly attractions bataunga. Preferences change karna ho toh profile update kar sakte hain."""
    
    def get_profile_update_confirmation_prompt(self, updated_profile):
        """Confirmation message after profile update"""
        first_name = updated_profile.get('first_name', 'User')
        return f"""Perfect, {first_name}! Aapki profile successfully update ho gayi hai. Ab main aapko updated preferences ke according recommendations dunga. Naye settings ke saath explore karte rahiye - food places, monuments, local culture, sab kuch aapki pasand ke according suggest karunga. Koi aur changes karne hon toh kabhi bhi profile update kar sakte hain."""
    
    def get_privacy_trust_prompt(self):
        """Data privacy and trust information"""
        return """Aapka data privacy hamari priority hai. Hum sirf local city guide features ke liye aapki information use karte hain - better recommendations dene ke liye. Aapka personal data secure rehta hai aur third parties ke saath share nahi kiya jata. Email aur mobile number sirf login ke liye use hote hain. Preferences data sirf personalized suggestions ke liye hai. Aap kabhi bhi apna data delete kar sakte hain ya preferences change kar sakte hain. Humara goal hai aapko best local experience dena, safely aur securely."""
    
    def get_personalization_enabled_prompt(self):
        """Benefits of personalization for logged-in users"""
        return """Personalization enable hai! Ab aapko customized recommendations milenge. Agar aap budget traveler hain toh street food aur affordable places suggest karunga. Family ke saath travel kar rahe hain toh family-friendly spots bataunga. Solo travel hai toh hidden gems aur local experiences focus karunga. Language preference ke according Hindi, Hinglish ya English mein respond karunga. Jitna zyada use karenge, utni better recommendations milti jayengi. Preferences kabhi bhi change kar sakte hain profile section mein."""
    
    def get_guest_signup_suggestion_prompt(self):
        """Suggestion for guests to create account"""
        return """Aap guest mode mein explore kar rahe hain - yeh bilkul theek hai! Lekin agar aap account banayenge toh personalized recommendations mil sakti hain. Jaise aapka budget range, travel style (solo/family), favorite food types - yeh sab preferences save ho jayengi. Phir main aapko exactly wahi suggest karunga jo aapko pasand aayega. Plus, aap apni favorite places save kar sakte hain future reference ke liye. Account banana optional hai, guest mode mein bhi full access hai city guide ka."""
    
    def get_login_success_prompt(self, first_name):
        """Success message after login"""
        return f"""Welcome back, {first_name}! Aap successfully login ho gaye hain. Ab aapko personalized Agra recommendations milenge aapki saved preferences ke according. Main aapki travel style, budget range, aur language preference remember kar chuka hun. Kya explore karna chahenge aaj - food places, historical sites, ya koi specific area? Personalized suggestions ke liye bas puchiye!"""
    
    def get_signup_success_prompt(self, first_name):
        """Success message after successful signup"""
        return f"""Congratulations {first_name}! Aapka account successfully create ho gaya hai. Ab aap personalized Agra city guide experience kar sakte hain. Preferences set kar sakte hain - budget range, travel style, language preference. Yeh sab aapko better recommendations dene ke liye hai. Favorite places save kar sakte hain, aur har visit ke saath recommendations improve hoti jayengi. Chalo shuru karte hain - Agra mein kya explore karna chahenge?"""