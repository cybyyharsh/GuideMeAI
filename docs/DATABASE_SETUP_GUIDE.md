# Database-Driven Local AI City Agent - Setup Guide

## Overview

This system uses MySQL database to store and retrieve verified local information about cities. The AI agent responds based on actual database content, avoiding hallucinations and providing accurate, localized information.

## System Architecture

```
User Query → Agent Router → Query Type Detection → Database Lookup → Response Builder → User
```

### Key Components:

1. **Master System Prompt** - Global guidelines for AI behavior
2. **10 Specialized Prompt Templates** - For different query types
3. **MySQL Database** - Stores verified city information
4. **Database Service** - Handles all database operations
5. **Response Builders** - Format database data into friendly responses

## Database Schema

### Tables:

1. **city_overview** - General city information
2. **places_history** - Monuments and places with history
3. **markets_streets** - Markets and street histories
4. **local_foods** - Food items with origin stories
5. **restaurants_streetfood** - Eating places
6. **tourist_places** - Places to visit
7. **transport_traffic** - Transport patterns
8. **accommodation** - Stay areas and options
9. **culture_traditions** - Cultural events and traditions

## Setup Instructions

### Step 1: Install MySQL

**Windows:**
```bash
# Download MySQL from https://dev.mysql.com/downloads/installer/
# Install MySQL Server and MySQL Workbench
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install mysql-server
```

**Mac:**
```bash
brew install mysql
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask and Flask-CORS
- MySQL connector
- Other required packages

### Step 3: Configure Database

1. Update `.env` file with your MySQL credentials:

```env
DB_HOST=localhost
DB_NAME=city_guide
DB_USER=root
DB_PASSWORD=your_password
DB_PORT=3306
```

### Step 4: Initialize Database

Run the initialization script:

```bash
python backend/init_database.py
```

This will:
- Create the `city_guide` database
- Set up all required tables
- Insert sample data for Agra

### Step 5: Verify Database

Check if data was inserted correctly:

```sql
USE city_guide;
SELECT * FROM city_overview;
SELECT * FROM places_history;
SELECT * FROM local_foods;
```

## Query Types and Responses

### 1. City Overview
**Trigger:** "Tell me about Agra", "City introduction"
**Database:** `city_overview` table
**Response:** Historical background, culture, daily life, unique features

### 2. Place History
**Trigger:** "Taj Mahal history", "When was Agra Fort built"
**Database:** `places_history` table
**Response:** Built year, builder, importance, interesting facts

### 3. Market History
**Trigger:** "Sadar Bazaar history", "Tell me about local markets"
**Database:** `markets_streets` table
**Response:** Origin story, evolution, current significance

### 4. Food History
**Trigger:** "Petha origin", "Why is bedai famous"
**Database:** `local_foods` table
**Response:** Origin story, popularity reason, eating style, local habits

### 5. Restaurant Suggestions
**Trigger:** "Where to eat", "Best restaurants"
**Database:** `restaurants_streetfood` table
**Response:** Categorized list with locations, timings, prices

### 6. Places to Visit
**Trigger:** "Places to visit", "What to see in Agra"
**Database:** `tourist_places` table
**Response:** Must-visit places with reasons and timings

### 7. Traffic & Transport
**Trigger:** "How to reach", "Traffic patterns"
**Database:** `transport_traffic` table
**Response:** Peak hours, transport options, practical tips

### 8. Accommodation
**Trigger:** "Where to stay", "Hotel areas"
**Database:** `accommodation` table
**Response:** Area-wise suggestions with safety and convenience info

### 9. Culture & Traditions
**Trigger:** "Festivals in Agra", "Local traditions"
**Database:** `culture_traditions` table
**Response:** Background, current practice, visitor experience

## Adding New Cities

### Step 1: Add City Data

Insert data for new city in all relevant tables:

```sql
-- City Overview
INSERT INTO city_overview (city_name, state_name, historical_background, ...) VALUES
('Delhi', 'Delhi', 'Capital of India...', ...);

-- Places
INSERT INTO places_history (city_name, place_name, built_year, ...) VALUES
('Delhi', 'Red Fort', '1638-1648', ...);

-- Continue for all tables...
```

### Step 2: Update Configuration

Update `backend/city_config.py`:

```python
CityConfig.CITY_NAME = "Delhi"
CityConfig.STATE_NAME = "Delhi"
CityConfig.CITY_IDENTITY = "Delhi is..."
```

### Step 3: Restart Server

```bash
python backend/app.py
```

## Testing the System

### Test Database Connection:

```python
from backend.services.database_service import DatabaseService

db = DatabaseService()
if db.connect():
    print("✓ Database connected!")
    data = db.get_city_overview("Agra")
    print(data)
else:
    print("✗ Connection failed")
```

### Test API Endpoints:

```bash
# Test city overview
curl -X POST http://localhost:5000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Agra"}'

# Test food query
curl -X POST http://localhost:5000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Where to eat in Agra?"}'

# Test place history
curl -X POST http://localhost:5000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Taj Mahal history"}'
```

## Response Format

All responses follow this structure:

```json
{
  "response": "Formatted response text in Hinglish",
  "agent_type": "food|places|traffic|hotels|general",
  "query_type": "city_overview|place_history|food_history|...",
  "status": "success",
  "language": "Hinglish|Hindi",
  "data_source": "database"
}
```

## Fallback System

If database is unavailable, the system uses hardcoded fallback responses to ensure the service remains available.

## Best Practices

1. **Verify Data** - Always verify information before adding to database
2. **Use Local Names** - Use names exactly as locals say them
3. **Keep Updated** - Regularly update prices, timings, and seasonal information
4. **Add Context** - Include interesting facts and local tips
5. **Hinglish Tone** - Maintain friendly, conversational Hinglish tone

## Troubleshooting

### Database Connection Issues:

```python
# Check MySQL service
# Windows: Services → MySQL
# Linux: sudo systemctl status mysql
# Mac: brew services list

# Test connection
mysql -u root -p
USE city_guide;
SHOW TABLES;
```

### Missing Data:

```sql
-- Check if data exists
SELECT COUNT(*) FROM city_overview WHERE city_name = 'Agra';
SELECT COUNT(*) FROM places_history WHERE city_name = 'Agra';

-- Re-run initialization if needed
python backend/init_database.py
```

### Import Errors:

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## Future Enhancements

1. **Admin Panel** - Web interface to manage database content
2. **Multi-language Support** - Full Hindi, English, regional languages
3. **Image Integration** - Store and serve place images
4. **User Feedback** - Collect and incorporate user feedback
5. **Analytics** - Track popular queries and improve responses
6. **Real-time Updates** - Integration with live data sources

## Support

For issues or questions:
1. Check database connection and credentials
2. Verify sample data is inserted correctly
3. Check Flask server logs for errors
4. Test individual database queries

## License

This system is designed for educational and local tourism purposes.