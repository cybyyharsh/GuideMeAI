import re

class AgentRouter:
    def __init__(self):
        self.routing_keywords = {
            'food': [
                # English keywords
                'restaurant', 'food', 'eat', 'dining', 'cuisine', 'meal', 'hungry', 'lunch', 'dinner', 'breakfast',
                'snack', 'street food', 'local food', 'specialty', 'famous food',
                # Hindi/Hinglish keywords
                'khana', 'khane', 'restaurant', 'petha', 'bedai', 'jalebi', 'chaat', 'bhookh', 'nashta', 'khaana',
                'mithai', 'sweet', 'namkeen', 'dalmoth', 'famous', 'local'
            ],
            'traffic': [
                # English keywords
                'traffic', 'route', 'drive', 'parking', 'road', 'transportation', 'bus', 'metro', 'subway',
                'how to reach', 'how to go', 'distance', 'travel time',
                # Hindi/Hinglish keywords
                'auto', 'rickshaw', 'transport', 'jaana', 'kaise', 'pahunchna', 'rasta', 'gaadi',
                'kaise jaayein', 'kitna time', 'kitni door', 'fare'
            ],
            'hotels': [
                # English keywords
                'hotel', 'accommodation', 'stay', 'lodge', 'motel', 'booking', 'room', 'sleep',
                'where to stay', 'budget hotel', 'luxury hotel',
                # Hindi/Hinglish keywords
                'hotel', 'rukna', 'room', 'raat', 'theherna', 'accommodation', 'chahiye'
            ],
            'places': [
                # English keywords
                'visit', 'attraction', 'museum', 'park', 'tourist', 'sightseeing', 'landmark', 'activity',
                'places to visit', 'what to see', 'monuments', 'heritage',
                # Hindi/Hinglish keywords
                'ghumna', 'dekhna', 'taj', 'mahal', 'fort', 'jagah', 'visit', 'ghoomna', 'tourist',
                'ghumne', 'dekhneki', 'famous places'
            ]
        }
    
    def route_message(self, message):
        """Determine which agent should handle the message"""
        message_lower = message.lower()
        
        # Count keyword matches for each agent type
        scores = {}
        for agent_type, keywords in self.routing_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                scores[agent_type] = score
        
        # Return agent type with highest score, or 'general' if no matches
        if scores:
            return max(scores, key=scores.get)
        else:
            return 'general'