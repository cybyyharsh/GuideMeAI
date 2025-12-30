from services.database_service import DatabaseService
from services.location_service import LocationService
from location_data import LOCATION_DATA, CITY_GREETINGS
import json

class PromptBuilder:
    def __init__(self):
        self.db_service = DatabaseService()
        self.location_service = LocationService()
        
    def get_database_context(self, intent, message, city_name, state_name):
        """Fetch relevant context from Database (for Agra/specific cities) or Knowledge Base"""
        context_data = []
        
        # Try Database first (for Agra)
        if city_name and city_name.lower() == "agra":
            try:
                if intent == 'history':
                    all_places = self.db_service.get_places_to_visit(city_name)
                    if all_places:
                        for place in all_places:
                            if place['place_name'].lower() in message.lower():
                                data = self.db_service.get_place_history(place['place_name'], city_name)
                                if data: context_data.append(data[0])
                    if not context_data: context_data = all_places
                elif intent == 'food_culture':
                    restaurants = self.db_service.get_restaurants_by_city(city_name)
                    if restaurants: context_data.extend(restaurants)
                elif intent == 'travel_places':
                    data = self.db_service.get_places_to_visit(city_name)
                    if data: context_data.extend(data)
                
                overview = self.db_service.get_city_overview(city_name)
                if overview: context_data.insert(0, overview[0])
            except Exception as e:
                print(f"Database error: {e}")

        # Supplement with India-wide Knowledge JSON
        state_info = self.location_service.get_location_data(state_name)
        if state_info:
            context_data.append({"info_type": "state_knowledge", "data": state_info})
        
        if not context_data:
            return "KNOWLEDGE BASE: Limited information available locally. Use general knowledge about India."

        context_str = "KNOWLEDGE CONTEXT:\n"
        for item in context_data:
            context_str += json.dumps(item, default=str) + "\n"
        
        return context_str
    
    def get_master_prompt(self):
        """Standard Absolute Behavior Rules for GuideMeAI"""
        return """You are GuideMeAI, an interactive AI assistant. 
        Your primary responsibility is to respond ONLY to explicit user intent.

        ABSOLUTE BEHAVIOR RULES (NON-NEGOTIABLE):
        1. NEVER provide explanations, descriptions, facts, or recommendations unless the user explicitly asks for them.
        2. NEVER assume the user wants information about any city, place, topic, or subject.
        3. NEVER auto-start a topic, narration, or story.
        4. Greetings (hi, hello, namaste) must receive a SHORT greeting ONLY.
        5. Do NOT use default cities or examples unless the user names them first.
        6. Be concise, calm, and human-like. Avoid long introductions.
        7. If unsure about intent -> ask a clarifying question.
        8. Maintain "Hinglish" (mixture of Hindi and English) if the context suggests a local Indian flavor, but stay professional.
        """

    def build_prompt(self, message, intent, user_context=None, location_context=None, mode="text", history=None, profile_data=None):
        """Build prompt using intent-based gating and profile personalization"""
        
        master = self.get_master_prompt()
        
        # Intent Gating Templates
        intent_instructions = ""
        
        if intent == "greeting":
            intent_instructions = "The user has greeted you. Respond with a short greeting and ask what they would like to explore or ask about. Do NOT provide any facts."
        elif intent in ["vague_location", "clarification_needed"]:
            intent_instructions = "The user input is vague or is just a location name. Ask a clarifying question. Do NOT guess the topic."
        elif intent == "travel_places":
            intent_instructions = "The user wants suggestions for places to visit. List top monuments and gems concisely."
        elif intent == "food_culture":
            intent_instructions = "The user asking about food. Highlight local dishes and famous eateries."
        else:
            intent_instructions = f"Answer the user's specific question about the current context concisely."

        # Profile Personalization (Optional/Assistive)
        profile_instr = ""
        if profile_data and profile_data.get('isProfileActive'):
            name = profile_data.get('name')
            lang = profile_data.get('language', 'hinglish')
            interests = profile_data.get('interests', [])
            style = profile_data.get('responseStyle', 'concise')
            home_state = profile_data.get('homeState')

            profile_instr = "\nUSER PROFILE CONTEXT (Use silently for relevance):"
            if name: profile_instr += f"\n- User Name: {name} (Address them naturally if appropriate)"
            if lang: profile_instr += f"\n- Preferred Language: {lang}"
            if interests: profile_instr += f"\n- User Interests: {', '.join(interests)} (Focus on these aspects if relevant to the question)"
            if style: profile_instr += f"\n- Verbosity: {'Be extremely concise' if style == 'concise' else 'Provide descriptive insights'}"
            if home_state: profile_instr += f"\n- Home State: {home_state} (Use to reduce back-and-forth for geographic context)"

            profile_instr += "\nRULES: Never say 'Because you like...' or 'Based on your profile'. User input always overrides profile."

        # Knowledge Context
        knowledge_str = ""
        if intent not in ["greeting", "vague_location", "clarification_needed"] and location_context:
            target_city = location_context.get('city')
            target_state = location_context.get('state')
            knowledge_str = "\n" + self.get_database_context(intent, message, target_city, target_state)

        # Location Context
        loc_context_str = ""
        if location_context and intent not in ["greeting", "clarification_needed"]:
            city = location_context.get('city')
            state = location_context.get('state')
            if city: loc_context_str = f"\nCURRENT LOCATION CONTEXT: {city}, {state}."

        # History
        history_str = ""
        if history:
            history_str = "\nCONVERSATION HISTORY (Last 3 turns):\n" + "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history[-3:]])

        prompt = f"""{master}
        
        {intent_instructions}
        {profile_instr}
        {knowledge_str}
        {loc_context_str}
        {history_str}
        
        USER MESSAGE: {message}
        ASSISTANT:"""
        
        return prompt


