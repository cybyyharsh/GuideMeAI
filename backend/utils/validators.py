import re

def validate_message(message):
    """Validate user message input"""
    if not message or not isinstance(message, str):
        return False, "Message must be a non-empty string"
    
    if len(message.strip()) == 0:
        return False, "Message cannot be empty or only whitespace"
    
    if len(message) > 1000:
        return False, "Message too long (max 1000 characters)"
    
    return True, "Valid message"

def validate_agent_type(agent_type):
    """Validate agent type"""
    valid_types = ['food', 'traffic', 'hotels', 'places', 'general']
    
    if agent_type not in valid_types:
        return False, f"Invalid agent type. Must be one of: {', '.join(valid_types)}"
    
    return True, "Valid agent type"