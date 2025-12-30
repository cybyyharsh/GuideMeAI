from flask import Blueprint, jsonify
from services.database_service import DatabaseService

bp = Blueprint('map', __name__, url_prefix='/api/map')
db = DatabaseService()

@bp.route('/locations', methods=['GET'])
def get_locations():
    """Fetch all cities and historical places with coordinates for the map."""
    try:
        # Fetch cities
        cities_query = "SELECT city_name as name, latitude, longitude, 'city' as type, historical_background as description FROM city_overview WHERE latitude IS NOT NULL"
        cities = db.execute_query(cities_query)
        
        # Fetch historical places
        places_query = "SELECT place_name as name, latitude, longitude, 'historical_place' as type, historical_importance as description FROM places_history WHERE latitude IS NOT NULL"
        places = db.execute_query(places_query)
        
        # Combine results
        locations = (cities or []) + (places or [])
        
        return jsonify(locations)
    except Exception as e:
        print(f"Error fetching map locations: {e}")
        return jsonify({'error': str(e)}), 500
