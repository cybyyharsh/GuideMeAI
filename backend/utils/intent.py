def detect_intent(message: str) -> str:
    msg = message.lower().strip()

    # 1. Greeting Intent
    greetings = ["hi", "hello", "namaste", "hey", "good morning", "good evening", "hola"]
    if msg in greetings or any(msg == g for g in greetings):
        return "greeting"

    # 2. Vague or Incomplete Intent (Gating)
    # If it's just a location name without a question
    vague_locations = ["mumbai", "delhi", "agra", "jaipur", "goa", "kerala", "india"]
    if msg in vague_locations:
        return "vague_location"
    
    # If it's too short and not a greeting
    if len(msg.split()) < 3 and msg not in greetings:
        # Check if it's a known monument or topic
        specific_keywords = ["petha", "taj", "fort", "food", "history"]
        if not any(k in msg for k in specific_keywords):
            return "clarification_needed"

    # 3. Explicit Category Detection
    # Comparison (A vs B)
    if " vs " in msg or " compare " in msg or " better " in msg and (" or " in msg):
        return "comparison"

    # Seasonal / Festival
    if any(word in msg for word in ["festival", "celebration", "ritual", "mela", "utsav", "when is", "seasonal"]):
        return "seasonal_festival"

    # Travel / Places to visit
    if any(word in msg for word in ["visit", "attractions", "sightseeing", "what to see", "places to", "explore", "tourist"]):
        return "travel_places"

    # History
    if any(word in msg for word in ["history", "who built", "kab bana", "significance", "importance", "ancient", "heritage"]):
        return "history"

    # Food & Culture
    if any(word in msg for word in ["food", "eat", "restaurant", "cuisine", "dish", "specialty", "culture", "tradition", "local life"]):
        return "food_culture"

    return "general_exploration"

