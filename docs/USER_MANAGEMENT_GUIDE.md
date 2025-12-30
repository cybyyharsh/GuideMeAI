# User Management System - Complete Implementation Guide

## Overview
The Local AI City Agent now includes a comprehensive user management system with authentication, profile management, and personalized recommendations.

## Features Implemented

### 🔐 Authentication System
- **Guest Sessions**: Anonymous users can use the system with temporary sessions
- **User Registration**: Email or mobile-based signup
- **User Login**: Login with email or mobile number
- **Session Management**: Secure session handling for both guests and registered users

### 👤 User Profile Management
- **Personal Information**: Name, email, mobile, address, pin code
- **Preferences**: Budget range, travel style, language preference, preferred city
- **Profile Updates**: Users can modify their preferences anytime

### ⭐ Personalization Features
- **Budget-Based Recommendations**: Filter suggestions by budget (budget/mid-range/luxury)
- **Travel Style Adaptation**: Customize responses for solo/family/business/group travel
- **Language Preferences**: Support for Hindi, Hinglish, and English
- **Personalized Tips**: Context-aware local tips based on user preferences

## API Endpoints

### Authentication Routes (`/api/auth/`)

#### Create Guest Session
```http
POST /api/auth/guest
Content-Type: application/json

{}
```

#### User Signup
```http
POST /api/auth/signup
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "mobile": "9876543210",
  "pin_code": "110001"
}
```

#### User Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "login_type": "email",
  "login_identifier": "john@example.com"
}
```

#### Get Profile
```http
GET /api/auth/profile?user_id=123
```

#### Update Profile
```http
PUT /api/auth/profile
Content-Type: application/json

{
  "user_id": 123,
  "preferred_city": "Agra",
  "budget_range": "mid_range",
  "travel_style": "family",
  "language_preference": "hinglish"
}
```

### Enhanced Chat Route (`/api/chat/`)

#### Personalized Chat
```http
POST /api/chat/
Content-Type: application/json

{
  "message": "Recommend restaurants",
  "user_id": 123
}
```

#### Guest Chat
```http
POST /api/chat/
Content-Type: application/json

{
  "message": "Tell me about Agra",
  "session_token": "guest-session-token"
}
```

## Database Schema

### User Tables
- **users**: Basic user information
- **user_auth**: Authentication credentials
- **guest_sessions**: Temporary guest sessions
- **user_preferences**: User preferences for personalization

## Frontend Features

### User Interface
- **Authentication Modals**: Login and signup forms
- **Profile Management**: User profile editing interface
- **User Status Display**: Shows current user state (guest/logged in)
- **Personalization Indicators**: Visual indicators for personalized responses

### JavaScript Components
- **AuthManager**: Handles all authentication operations
- **Session Management**: Automatic session handling
- **User Context Integration**: Passes user context to API calls

## User Flow Prompts

The system includes 8 specialized prompts for different user scenarios:

1. **Guest Welcome**: Welcome message for anonymous users
2. **Login Assistant**: Guidance for login process
3. **Signup Assistant**: Help with account creation
4. **Profile Description**: Explains user profile and preferences
5. **Profile Update Confirmation**: Confirms successful profile updates
6. **Privacy & Trust**: Data privacy information
7. **Personalization Enabled**: Benefits of personalized experience
8. **Guest Signup Suggestion**: Encourages account creation

## Testing

### Automated Test Suite
Run the comprehensive test suite:

```bash
python test_user_management_system.py
```

### Manual Testing Steps

1. **Start the Server**:
   ```bash
   cd backend
   python app.py
   ```

2. **Open Frontend**:
   Open `frontend/index.html` in a web browser

3. **Test Guest Mode**:
   - Use the chat without logging in
   - Verify guest session creation

4. **Test User Registration**:
   - Click "Sign Up" button
   - Fill in the form and create account
   - Verify account creation and automatic login

5. **Test Profile Management**:
   - Click "Profile" button
   - Update preferences
   - Verify changes are saved

6. **Test Personalized Responses**:
   - Ask for restaurant recommendations
   - Verify responses match your preferences
   - Look for personalization indicators (⭐)

## Configuration

### Environment Variables
Add to `.env` file:
```
# Database Configuration (if using MySQL)
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=city_guide

# Session Configuration
SESSION_SECRET=your-secret-key
```

### Dependencies
The system requires these Python packages:
```
Flask==2.3.3
Flask-CORS==4.0.0
mysql-connector-python==8.1.0
pymysql==1.1.0
```

## Security Features

- **Session Token Validation**: Secure guest session management
- **Input Validation**: Email and mobile number format validation
- **SQL Injection Protection**: Parameterized queries
- **Data Privacy**: User data is only used for personalization

## Personalization Logic

### Budget-Based Filtering
- **Budget**: Shows street food and budget restaurants
- **Mid-Range**: Balanced mix of options
- **Luxury**: Premium restaurants and experiences

### Travel Style Adaptation
- **Solo**: Hidden gems and local experiences
- **Family**: Family-friendly places and activities
- **Business**: Convenient locations and professional services
- **Group**: Places suitable for larger groups

### Language Preferences
- **Hindi**: Responses in Hindi script
- **Hinglish**: Mix of Hindi and English (default)
- **English**: Pure English responses

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check MySQL server is running
   - Verify database credentials in `.env`
   - Run `python backend/init_database.py` to setup tables

2. **Frontend Not Loading**:
   - Ensure all JavaScript files are included
   - Check browser console for errors
   - Verify API endpoints are accessible

3. **Authentication Not Working**:
   - Check Flask server is running on port 5000
   - Verify CORS is enabled
   - Check network requests in browser dev tools

### Debug Mode
Enable debug logging by setting `DEBUG=True` in Flask configuration.

## Future Enhancements

Potential improvements for the user management system:

1. **Email Verification**: Send verification emails for new accounts
2. **Password Authentication**: Add password-based login
3. **Social Login**: Integration with Google/Facebook login
4. **User Analytics**: Track user preferences and behavior
5. **Recommendation Engine**: ML-based personalized suggestions
6. **Multi-City Support**: User profiles for multiple cities

## Support

For issues or questions about the user management system:

1. Check the test results: `user_management_test_results.json`
2. Review server logs for error messages
3. Verify database connectivity and schema
4. Test individual API endpoints using the test suite

The user management system is now fully integrated and ready for production use!