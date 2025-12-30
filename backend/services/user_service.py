import mysql.connector
from mysql.connector import Error
import hashlib
import secrets
import uuid
from datetime import datetime, timedelta
from services.database_service import DatabaseService

class UserService(DatabaseService):
    def __init__(self):
        super().__init__()
    
    def create_guest_session(self, ip_address=None, user_agent=None):
        """Create a guest session"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            session_token = str(uuid.uuid4())
            
            query = """
            INSERT INTO guest_sessions (session_token, ip_address, user_agent)
            VALUES (%s, %s, %s)
            """
            
            cursor = self.connection.cursor()
            cursor.execute(query, (session_token, ip_address, user_agent))
            self.connection.commit()
            
            guest_id = cursor.lastrowid
            cursor.close()
            
            return {
                'guest_id': guest_id,
                'session_token': session_token,
                'user_type': 'guest'
            }
            
        except Error as e:
            print(f"Guest session creation error: {e}")
            return None
    
    def validate_guest_session(self, session_token):
        """Validate guest session token"""
        try:
            query = """
            SELECT guest_id, session_token, created_at, expires_at 
            FROM guest_sessions 
            WHERE session_token = %s AND expires_at > NOW()
            """
            
            result = self.execute_query(query, (session_token,))
            return result[0] if result else None
            
        except Exception as e:
            print(f"Guest session validation error: {e}")
            return None
    
    def create_user(self, user_data):
        """Create a new user account"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            # Insert user data
            user_query = """
            INSERT INTO users (first_name, middle_name, last_name, dob, email, mobile, pin_code, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor = self.connection.cursor()
            cursor.execute(user_query, (
                user_data.get('first_name'),
                user_data.get('middle_name'),
                user_data.get('last_name'),
                user_data.get('dob'),
                user_data.get('email'),
                user_data.get('mobile'),
                user_data.get('pin_code'),
                user_data.get('address')
            ))
            
            user_id = cursor.lastrowid
            
            # Create auth entries
            if user_data.get('email'):
                auth_query = """
                INSERT INTO user_auth (user_id, login_type, login_identifier, is_verified)
                VALUES (%s, 'email', %s, FALSE)
                """
                cursor.execute(auth_query, (user_id, user_data.get('email')))
            
            if user_data.get('mobile'):
                auth_query = """
                INSERT INTO user_auth (user_id, login_type, login_identifier, is_verified)
                VALUES (%s, 'mobile', %s, FALSE)
                """
                cursor.execute(auth_query, (user_id, user_data.get('mobile')))
            
            # Create default preferences
            pref_query = """
            INSERT INTO user_preferences (user_id, preferred_city, language_preference)
            VALUES (%s, 'Agra', 'hinglish')
            """
            cursor.execute(pref_query, (user_id,))
            
            self.connection.commit()
            cursor.close()
            
            return {
                'user_id': user_id,
                'status': 'created',
                'user_type': 'registered'
            }
            
        except Error as e:
            print(f"User creation error: {e}")
            # Handle MySQL duplicate entry errors specifically
            if e.errno == 1062:  # MySQL duplicate entry error code
                error_msg = str(e)
                if 'email' in error_msg:
                    raise Exception("DUPLICATE_EMAIL")
                elif 'mobile' in error_msg:
                    raise Exception("DUPLICATE_MOBILE")
                else:
                    raise Exception("DUPLICATE_ENTRY")
            raise e
    
    def authenticate_user(self, login_identifier, login_type):
        """Authenticate user by email or mobile"""
        try:
            query = """
            SELECT u.user_id, u.first_name, u.last_name, u.email, u.mobile, u.pin_code,
                   ua.auth_id, ua.is_verified
            FROM users u
            JOIN user_auth ua ON u.user_id = ua.user_id
            WHERE ua.login_identifier = %s AND ua.login_type = %s
            """
            
            result = self.execute_query(query, (login_identifier, login_type))
            
            if result:
                user_data = result[0]
                
                # Update last login
                update_query = """
                UPDATE user_auth SET last_login = NOW() 
                WHERE auth_id = %s
                """
                if not self.connection or not self.connection.is_connected():
                    self.connect()
                
                cursor = self.connection.cursor()
                cursor.execute(update_query, (user_data['auth_id'],))
                self.connection.commit()
                cursor.close()
                
                return {
                    'user_id': user_data['user_id'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                    'mobile': user_data['mobile'],
                    'pin_code': user_data['pin_code'],
                    'is_verified': user_data['is_verified'],
                    'user_type': 'registered'
                }
            
            return None
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def get_user_profile(self, user_id):
        """Get complete user profile with preferences"""
        try:
            query = """
            SELECT u.*, up.preferred_city, up.food_preferences, up.budget_range,
                   up.travel_style, up.language_preference
            FROM users u
            LEFT JOIN user_preferences up ON u.user_id = up.user_id
            WHERE u.user_id = %s
            """
            
            result = self.execute_query(query, (user_id,))
            return result[0] if result else None
            
        except Exception as e:
            print(f"Profile retrieval error: {e}")
            return None
    
    def update_user_profile(self, user_id, profile_data):
        """Update user profile information"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            
            # Update user basic info
            if any(key in profile_data for key in ['first_name', 'middle_name', 'last_name', 'email', 'mobile', 'pin_code', 'address']):
                user_fields = []
                user_values = []
                
                for field in ['first_name', 'middle_name', 'last_name', 'email', 'mobile', 'pin_code', 'address']:
                    if field in profile_data:
                        user_fields.append(f"{field} = %s")
                        user_values.append(profile_data[field])
                
                if user_fields:
                    user_query = f"UPDATE users SET {', '.join(user_fields)} WHERE user_id = %s"
                    user_values.append(user_id)
                    cursor.execute(user_query, user_values)
            
            # Update preferences
            pref_keys = ['preferred_city', 'food_preferences', 'budget_range', 'travel_style', 'language_preference', 'tone_preference', 'interests', 'ui_preferences']
            if any(key in profile_data for key in pref_keys):
                pref_fields = []
                pref_values = []
                
                for field in pref_keys:
                    if field in profile_data:
                        pref_fields.append(f"{field} = %s")
                        pref_values.append(profile_data[field])
                
                if pref_fields:
                    # Check if preferences exist
                    check_query = "SELECT pref_id FROM user_preferences WHERE user_id = %s"
                    cursor.execute(check_query, (user_id,))
                    exists = cursor.fetchone()
                    
                    if exists:
                        pref_query = f"UPDATE user_preferences SET {', '.join(pref_fields)} WHERE user_id = %s"
                        pref_values.append(user_id)
                        cursor.execute(pref_query, pref_values)
                    else:
                        # Create new preferences record
                        pref_fields.append("user_id")
                        pref_values.append(user_id)
                        placeholders = ', '.join(['%s'] * len(pref_values))
                        pref_query = f"INSERT INTO user_preferences ({', '.join(pref_fields.replace(' = %s', ''))}) VALUES ({placeholders})"
                        cursor.execute(pref_query, pref_values)
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            print(f"Profile update error: {e}")
            return False
    
    def check_user_exists(self, email=None, mobile=None):
        """Check if user already exists and return detailed information"""
        try:
            result = {
                'exists': False,
                'email_exists': False,
                'mobile_exists': False
            }
            
            if email:
                email_query = "SELECT user_id FROM users WHERE email = %s"
                email_result = self.execute_query(email_query, (email,))
                if email_result:
                    result['exists'] = True
                    result['email_exists'] = True
            
            if mobile:
                mobile_query = "SELECT user_id FROM users WHERE mobile = %s"
                mobile_result = self.execute_query(mobile_query, (mobile,))
                if mobile_result:
                    result['exists'] = True
                    result['mobile_exists'] = True
            
            return result if result['exists'] else None
            
        except Exception as e:
            print(f"User existence check error: {e}")
            raise e
            
        except Exception as e:
            print(f"User existence check error: {e}")
            return False
    
    def get_personalized_recommendations(self, user_id, city_name):
        """Get personalized recommendations based on user preferences"""
        try:
            # Get user preferences
            profile = self.get_user_profile(user_id)
            if not profile:
                return None
            
            budget_range = profile.get('budget_range', 'mid_range')
            travel_style = profile.get('travel_style', 'solo')
            
            # Get restaurants based on budget preference
            restaurant_query = """
            SELECT * FROM restaurants_streetfood 
            WHERE city_name = %s AND category = %s
            ORDER BY popularity DESC
            LIMIT 5
            """
            
            restaurants = self.execute_query(restaurant_query, (city_name, budget_range))
            
            # Get places based on travel style
            if travel_style == 'family':
                place_importance = 'must_visit'
            elif travel_style == 'solo':
                place_importance = 'recommended'
            else:
                place_importance = 'must_visit'
            
            places_query = """
            SELECT * FROM tourist_places 
            WHERE city_name = %s AND importance = %s
            ORDER BY importance DESC
            LIMIT 5
            """
            
            places = self.execute_query(places_query, (city_name, place_importance))
            
            return {
                'restaurants': restaurants,
                'places': places,
                'user_preferences': {
                    'budget_range': budget_range,
                    'travel_style': travel_style,
                    'language_preference': profile.get('language_preference', 'hinglish'),
                    'tone_preference': profile.get('tone_preference', 'detailed'),
                    'interests': profile.get('interests', '')
                }
            }
            
        except Exception as e:
            print(f"Personalization error: {e}")
            return None