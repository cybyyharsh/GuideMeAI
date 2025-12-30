import json
import os

class LocationService:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'india_knowledge.json')
        self.knowledge = self._load_data()
        self.states = self.knowledge.get('states', {})
        self.city_to_state = self.knowledge.get('city_to_state', {})

    def _load_data(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading india_knowledge.json: {e}")
            return {"states": {}, "city_to_state": {}}

    def infer_location(self, message):
        """Rule-based location inference from message"""
        msg = message.lower()
        
        # Check for city names
        for city, state in self.city_to_state.items():
            if city.lower() in msg:
                return {"city": city, "state": state}
        
        # Check for state names
        for state in self.states.keys():
            if state.lower() in msg:
                return {"city": self.states[state]['capital'], "state": state}
        
        # Check for famous monuments
        for state, data in self.states.items():
            for monument in data.get('monuments', []):
                if monument.lower() in msg:
                    # Some monuments are in specific cities, but we'll return the state capital as a safe fallback
                    # unless we want to map monuments to cities too. For now, state is enough.
                    return {"city": data['capital'], "state": state}

        return None

    def get_location_data(self, state_name):
        return self.states.get(state_name)

    def get_all_states(self):
        return list(self.states.keys())

    def get_cities_in_state(self, state_name):
        state_data = self.states.get(state_name)
        return state_data.get('cities', []) if state_data else []
