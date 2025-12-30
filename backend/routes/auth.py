from flask import Blueprint, request, jsonify
from services.user_service import UserService
from services.user_prompts import UserPrompts
import re
from datetime import datetime
import uuid

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def handle_simple_signup(user_data, first_name):
    """Handle signup when database is unavailable"""
    try:
        # Simulate successful user creation
        fake_user_data = {
            'user_id': int(str(uuid.uuid4().int)[:8]),  # Generate a fake user ID
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'email': user_data.get('email'),
            'mobile': user_data.get('mobile'),
            'status': 'created',
            'user_type': 'registered'
        }
        
        success_message = f"Welcome {first_name}! Your account has been created successfully. Note: This is demo mode - data is not permanently stored."
        
        return jsonify({
            'status': 'success',
            'user_data': fake_user_data,
            'success_message': success_message,
            'user_type': 'registered'
        })
        
    except Exception as e:
        return jsonify({'error': f'Simple signup error: {str(e)}'}), 500

@bp.route('/guest', methods=['POST', 'OPTIONS'])
def create_guest_session():
    """Create a guest session for anonymous users"""
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    try:
        # Try database first, fall back to simple mode
        try:
            user_service = UserService()
            user_prompts = UserPrompts()
            
            # Test database connection
            if not user_service.connect():
                raise Exception("Database unavailable")
            
            # Get client info
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
            user_agent = request.headers.get('User-Agent')
            
            # Create guest session
            session_data = user_service.create_guest_session(ip_address, user_agent)
            
            if session_data:
                # Get welcome prompt for guest
                welcome_message = user_prompts.get_guest_welcome_prompt()
                
                return jsonify({
                    'status': 'success',
                    'session_data': session_data,
                    'welcome_message': welcome_message,
                    'user_type': 'guest'
                })
            else:
                raise Exception("Failed to create guest session")
                
        except Exception as e:
            print(f"Database guest session failed: {e}, using simple mode")
            # Simple guest session without database
            import uuid
            session_data = {
                'guest_id': int(str(uuid.uuid4().int)[:8]),
                'session_token': str(uuid.uuid4()),
                'user_type': 'guest'
            }
            
            welcome_message = 'Welcome! You are browsing as a guest. Create an account for personalized recommendations.'
            
            return jsonify({
                'status': 'success',
                'session_data': session_data,
                'welcome_message': welcome_message,
                'user_type': 'guest'
            })
            
    except Exception as e:
        print(f"Guest session error: {e}")
        return jsonify({'error': 'Failed to create guest session'}), 500

@bp.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    """User registration endpoint"""
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    try:
        print("Signup request received")  # Debug log
        data = request.get_json()
        print(f"Request data: {data}")  # Debug log
        
        # Normalize and validate input data
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip().lower() if data.get('email') else None
        mobile = data.get('mobile', '').strip() if data.get('mobile') else None
        dob = data.get('dob') if data.get('dob') else None
        pin_code = data.get('pin_code', '').strip() if data.get('pin_code') else None
        address = data.get('address', '').strip() if data.get('address') else None
        
        # Validate required fields
        if not first_name:
            return jsonify({'error': 'First name is required'}), 400
        if not last_name:
            return jsonify({'error': 'Last name is required'}), 400
        
        # Validate email or mobile (at least one required)
        if not email and not mobile:
            return jsonify({'error': 'Either email or mobile number is required'}), 400
        
        # Validate email format if provided
        if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'error': 'Please enter a valid email address'}), 400
        
        # Validate mobile format if provided (Indian mobile numbers)
        if mobile:
            # Remove any non-digit characters
            mobile = re.sub(r'\D', '', mobile)
            if not re.match(r'^[6-9]\d{9}$', mobile):
                return jsonify({'error': 'Please enter a valid 10-digit mobile number starting with 6-9'}), 400
        
        # Validate date of birth format if provided
        if dob:
            try:
                from datetime import datetime
                datetime.strptime(dob, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Date of birth must be in YYYY-MM-DD format'}), 400
        
        # Create user data object
        user_data = {
            'first_name': first_name,
            'middle_name': None,  # Not collected in current form
            'last_name': last_name,
            'dob': dob,
            'email': email,
            'mobile': mobile,
            'pin_code': pin_code,
            'address': address
        }
        
        # Try database operations, fall back to simple mode if database unavailable
        try:
            user_service = UserService()
            user_prompts = UserPrompts()
            
            # Test database connection first
            if not user_service.connect():
                print("Database connection failed, using simple signup mode")
                return handle_simple_signup(user_data, first_name)
            
            # Check if user already exists with better error handling
            print("Checking if user exists...")  # Debug log
            existing_user = user_service.check_user_exists(email, mobile)
            if existing_user:
                if existing_user.get('email_exists') and existing_user.get('mobile_exists'):
                    return jsonify({'error': 'An account already exists with this email and mobile number'}), 409
                elif existing_user.get('email_exists'):
                    return jsonify({'error': 'An account already exists with this email address'}), 409
                elif existing_user.get('mobile_exists'):
                    return jsonify({'error': 'An account already exists with this mobile number'}), 409
            
            print("Creating user...")  # Debug log
            result = user_service.create_user(user_data)
            print(f"User creation result: {result}")  # Debug log
            
            if result:
                # Get signup success prompt
                try:
                    success_message = user_prompts.get_signup_success_prompt(first_name)
                except Exception as e:
                    print(f"Error getting success prompt: {e}")  # Debug log
                    success_message = f"Welcome {first_name}! Your account has been created successfully."
                
                return jsonify({
                    'status': 'success',
                    'user_data': result,
                    'success_message': success_message,
                    'user_type': 'registered'
                })
            else:
                print("User creation returned None, falling back to simple mode")
                return handle_simple_signup(user_data, first_name)
                
        except Exception as e:
            print(f"Database operation error: {e}")  # Debug log
            # Handle specific duplicate entry errors
            error_str = str(e)
            if error_str == "DUPLICATE_EMAIL":
                return jsonify({'error': 'An account already exists with this email address'}), 409
            elif error_str == "DUPLICATE_MOBILE":
                return jsonify({'error': 'An account already exists with this mobile number'}), 409
            elif error_str == "DUPLICATE_ENTRY":
                return jsonify({'error': 'An account with these details already exists'}), 409
            elif 'Duplicate entry' in error_str:
                if 'email' in error_str:
                    return jsonify({'error': 'An account already exists with this email address'}), 409
                elif 'mobile' in error_str:
                    return jsonify({'error': 'An account already exists with this mobile number'}), 409
                else:
                    return jsonify({'error': 'An account with these details already exists'}), 409
            # If database is unavailable, fall back to simple mode
            elif 'Access denied' in error_str or 'Connection' in error_str or 'mysql' in error_str.lower():
                print("Database unavailable, using simple signup mode")
                return handle_simple_signup(user_data, first_name)
            
            # For any other error, fall back to simple mode
            print("Unknown error, falling back to simple mode")
            return handle_simple_signup(user_data, first_name)
            
    except Exception as e:
        print(f"Signup error: {e}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({'error': 'Server error occurred. Please try again.'}), 500

@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """User login endpoint (email or mobile)"""
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    try:
        data = request.get_json()
        user_service = UserService()
        user_prompts = UserPrompts()
        
        login_identifier = data.get('login_identifier', '').strip()
        login_type = data.get('login_type')  # 'email' or 'mobile'
        
        if not login_identifier or not login_type:
            return jsonify({'error': 'Login identifier and type are required'}), 400
        
        # Normalize identifier
        if login_type == 'email':
            login_identifier = login_identifier.lower()
        elif login_type == 'mobile':
            login_identifier = re.sub(r'\D', '', login_identifier)
        else:
            return jsonify({'error': 'Login type must be email or mobile'}), 400
        
        print(f"Login attempt: type={login_type}, identifier={login_identifier}")
        
        # Authenticate user
        user_data = user_service.authenticate_user(login_identifier, login_type)
        
        if user_data:
            print(f"Login successful for user: {user_data.get('user_id')}")
            # Get login success prompt
            try:
                success_message = user_prompts.get_login_success_prompt(user_data.get('first_name'))
            except:
                success_message = f"Welcome back, {user_data.get('first_name')}!"
            
            return jsonify({
                'status': 'success',
                'user_data': user_data,
                'success_message': success_message,
                'user_type': 'registered'
            })
        else:
            print("Login failed: Invalid credentials")
            return jsonify({'error': 'Invalid credentials or user not found'}), 401
            
    except Exception as e:
        print(f"Login server error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@bp.route('/profile', methods=['GET', 'OPTIONS'])
def get_profile():
    """Get user profile information"""
    try:
        # In a real app, you'd get user_id from JWT token or session
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        user_service = UserService()
        user_prompts = UserPrompts()
        
        profile_data = user_service.get_user_profile(user_id)
        
        if profile_data:
            # Get profile description prompt
            profile_message = user_prompts.get_profile_description_prompt(profile_data)
            
            return jsonify({
                'status': 'success',
                'profile_data': profile_data,
                'profile_message': profile_message
            })
        else:
            return jsonify({'error': 'User profile not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['PUT', 'OPTIONS'])
def update_profile():
    """Update user profile information"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        user_service = UserService()
        user_prompts = UserPrompts()
        
        # Remove user_id from update data
        update_data = {k: v for k, v in data.items() if k != 'user_id'}
        
        success = user_service.update_user_profile(user_id, update_data)
        
        if success:
            # Get updated profile
            updated_profile = user_service.get_user_profile(user_id)
            
            # Get update confirmation prompt
            confirmation_message = user_prompts.get_profile_update_confirmation_prompt(updated_profile)
            
            return jsonify({
                'status': 'success',
                'profile_data': updated_profile,
                'confirmation_message': confirmation_message
            })
        else:
            return jsonify({'error': 'Failed to update profile'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/privacy-info', methods=['GET', 'OPTIONS'])
def get_privacy_info():
    """Get data privacy and trust information"""
    try:
        user_prompts = UserPrompts()
        privacy_message = user_prompts.get_privacy_trust_prompt()
        
        return jsonify({
            'status': 'success',
            'privacy_message': privacy_message
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/personalization-status', methods=['GET', 'OPTIONS'])
def get_personalization_status():
    """Get personalization enabled status and benefits"""
    try:
        user_id = request.args.get('user_id')
        user_prompts = UserPrompts()
        
        if user_id:
            # User is logged in
            personalization_message = user_prompts.get_personalization_enabled_prompt()
        else:
            # Guest user
            personalization_message = user_prompts.get_guest_signup_suggestion_prompt()
        
        return jsonify({
            'status': 'success',
            'personalization_message': personalization_message,
            'is_personalized': bool(user_id)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/test', methods=['GET', 'OPTIONS'])
def test_auth():
    """Test endpoint to verify auth routes are working"""
    return jsonify({
        'status': 'success',
        'message': 'Auth routes are working',
        'timestamp': str(datetime.now())
    })

@bp.route('/signup-simple', methods=['POST', 'OPTIONS'])
def signup_simple():
    """Simplified signup for testing without database"""
    try:
        data = request.get_json()
        
        # Basic validation
        if not data.get('first_name') or not data.get('last_name'):
            return jsonify({'error': 'First name and last name are required'}), 400
        
        if not data.get('email') and not data.get('mobile'):
            return jsonify({'error': 'Either email or mobile number is required'}), 400
        
        # Simulate successful user creation
        fake_user_data = {
            'user_id': 12345,
            'status': 'created',
            'user_type': 'registered'
        }
        
        return jsonify({
            'status': 'success',
            'user_data': fake_user_data,
            'success_message': f"Welcome {data.get('first_name')}! Your account has been created successfully.",
            'user_type': 'registered'
        })
        
    except Exception as e:
        return jsonify({'error': f'Simple signup error: {str(e)}'}), 500

@bp.route('/validate-session', methods=['POST', 'OPTIONS'])
def validate_session():
    """Validate guest session token"""
    try:
        data = request.get_json()
        session_token = data.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Session token is required'}), 400
        
        user_service = UserService()
        session_data = user_service.validate_guest_session(session_token)
        
        if session_data:
            return jsonify({
                'status': 'valid',
                'session_data': session_data
            })
        else:
            return jsonify({'error': 'Invalid or expired session'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500