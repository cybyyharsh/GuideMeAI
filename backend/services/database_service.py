import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv(override=True)  # Force reload environment variables

class DatabaseService:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'city_guide')
        self.user = os.getenv('DB_USER', 'root')
        # Force the password since environment loading is problematic
        password_from_env = os.getenv('DB_PASSWORD', '')
        self.password = password_from_env if password_from_env else 'Qwerty00'
        self.port = int(os.getenv('DB_PORT', 3306))
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Execute SELECT query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Query execution error: {e}")
            return None
    
    def get_city_overview(self, city_name):
        """Get city overview information"""
        query = """
        SELECT * FROM city_overview 
        WHERE city_name = %s
        """
        return self.execute_query(query, (city_name,))
    
    def get_place_history(self, place_name, city_name):
        """Get place/monument history"""
        query = """
        SELECT * FROM places_history 
        WHERE place_name = %s AND city_name = %s
        """
        return self.execute_query(query, (place_name, city_name))
    
    def get_market_history(self, market_name, city_name):
        """Get street/market history"""
        query = """
        SELECT * FROM markets_streets 
        WHERE market_name = %s AND city_name = %s
        """
        return self.execute_query(query, (market_name, city_name))
    
    def get_food_info(self, food_name, city_name):
        """Get food information and history"""
        query = """
        SELECT * FROM local_foods 
        WHERE food_name = %s AND city_name = %s
        """
        return self.execute_query(query, (food_name, city_name))
    
    def get_restaurants_by_city(self, city_name):
        """Get restaurants and street food places"""
        query = """
        SELECT * FROM restaurants_streetfood 
        WHERE city_name = %s 
        ORDER BY category, popularity DESC
        """
        return self.execute_query(query, (city_name,))
    
    def get_places_to_visit(self, city_name):
        """Get places to visit in the city"""
        query = """
        SELECT * FROM tourist_places 
        WHERE city_name = %s 
        ORDER BY importance DESC, category
        """
        return self.execute_query(query, (city_name,))
    
    def get_transport_info(self, city_name):
        """Get transport and traffic information"""
        query = """
        SELECT * FROM transport_traffic 
        WHERE city_name = %s
        """
        return self.execute_query(query, (city_name,))
    
    def get_accommodation_info(self, city_name):
        """Get hotel and stay information"""
        query = """
        SELECT * FROM accommodation 
        WHERE city_name = %s 
        ORDER BY category, area
        """
        return self.execute_query(query, (city_name,))
    
    def get_cultural_info(self, city_name):
        """Get cultural traditions and festivals"""
        query = """
        SELECT * FROM culture_traditions 
        WHERE city_name = %s 
        ORDER BY importance DESC
        """
        return self.execute_query(query, (city_name,))
    
    def search_content(self, city_name, search_term):
        """Search across all tables for relevant content"""
        queries = [
            ("places", "SELECT 'place' as type, place_name as name, description FROM places_history WHERE city_name = %s AND (place_name LIKE %s OR description LIKE %s)"),
            ("food", "SELECT 'food' as type, food_name as name, description FROM local_foods WHERE city_name = %s AND (food_name LIKE %s OR description LIKE %s)"),
            ("markets", "SELECT 'market' as type, market_name as name, description FROM markets_streets WHERE city_name = %s AND (market_name LIKE %s OR description LIKE %s)")
        ]
        
        search_pattern = f"%{search_term}%"
        all_results = []
        
        for category, query in queries:
            results = self.execute_query(query, (city_name, search_pattern, search_pattern))
            if results:
                all_results.extend(results)
        
        return all_results