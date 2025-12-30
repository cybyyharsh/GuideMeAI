"""
City Configuration for Local AI Agent
Easily change city and customize responses
"""

class CityConfig:
    # Main city configuration
    CITY_NAME = "Agra"
    STATE_NAME = "Uttar Pradesh"
    
    # City identity and culture
    CITY_IDENTITY = """Agra is the city of Mughal heritage and street food culture. Famous for Taj Mahal, but locals live around bustling bazaars, morning bedai-jalebi culture, and evening chaat sessions. People are warm, helpful, and proud of their history. Life revolves around monuments by day and local markets by evening."""
    
    # Language settings
    DEFAULT_LANGUAGE = "Hinglish"
    SUPPORTED_LANGUAGES = ["Hindi", "Hinglish", "English"]
    
    # Response tone settings
    TONE = "friendly_local"  # Options: friendly_local, professional, casual
    
    # Feature flags
    ENABLE_STREET_LEVEL_KNOWLEDGE = True
    ENABLE_LOCAL_TIPS = True
    ENABLE_PRACTICAL_ADVICE = True
    
    @classmethod
    def get_city_showcase(cls):
        """Get city showcase description"""
        return f"""{cls.CITY_NAME} - where Mughal grandeur meets vibrant street life! 
        
Famous for the iconic Taj Mahal, but the real magic lies in morning bedai-jalebi sessions at Deviram Sweets, evening chaat at Sadar Bazaar, and the warm hospitality of locals who treat every visitor like family. 

Yahan history aur modern life ka perfect blend hai!"""
    
    @classmethod
    def get_welcome_message(cls):
        """Get welcome message for the city"""
        return f"""Namaste! Main {cls.CITY_NAME} ka local AI assistant hun, aapka dost!

Main help kar sakta hun:
• Food scene - street food se fine dining tak sab kuch
• Places to visit - famous monuments aur local hidden gems  
• Traffic patterns aur transport ki practical advice
• Stay options aur safe areas ki recommendations
• Local trends aur what's happening around the city

{cls.CITY_NAME} is not just monuments - yahan ka rich street culture, amazing food, aur friendly locals ka experience bhi incredible hai!

Kya puchna hai {cls.CITY_NAME} ke baare mein?"""

# Easy city switching - just change these values
def switch_city(city_name, state_name, city_identity):
    """Function to easily switch to a different city"""
    CityConfig.CITY_NAME = city_name
    CityConfig.STATE_NAME = state_name
    CityConfig.CITY_IDENTITY = city_identity
    
# Example configurations for other cities
CITY_PRESETS = {
    "delhi": {
        "name": "Delhi",
        "state": "Delhi",
        "identity": "Delhi is the heart of India - a bustling metropolis where street food culture thrives alongside political power. From Chandni Chowk's narrow lanes to Connaught Place's circles, every corner tells a story. Delhiites are fast-paced, food-loving, and always ready to help with directions!"
    },
    "mumbai": {
        "name": "Mumbai", 
        "state": "Maharashtra",
        "identity": "Mumbai is the city of dreams and vada pav! Fast-paced life, local trains, and street food on every corner. From Marine Drive's sunset to Juhu Beach's bhel puri, Mumbaikars live life in the fast lane but always have time for good food and helping strangers."
    },
    "jaipur": {
        "name": "Jaipur",
        "state": "Rajasthan", 
        "identity": "Jaipur, the Pink City, where royal heritage meets colorful bazaars. Famous for palaces and forts, but locals love their dal-baati-churma and evening walks in City Palace area. Jaipurites are proud of their culture and always eager to share stories about their royal city."
    }
}