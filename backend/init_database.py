#!/usr/bin/env python3
"""
Database Initialization Script
Run this to set up the database with sample Agra data
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'Qwerty00'),  # Use provided password as default
            port=int(os.getenv('DB_PORT', 3306))
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_sql_file(connection, filename):
    """Execute SQL commands from file"""
    try:
        cursor = connection.cursor()
        
        with open(filename, 'r', encoding='utf-8') as file:
            sql_commands = file.read().split(';')
            
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    connection.commit()
                    print(f"✓ Executed: {command[:50]}...")
                except Error as e:
                    print(f"✗ Error executing command: {e}")
        
        cursor.close()
        print("✓ Database setup completed!")
        
    except Exception as e:
        print(f"Error reading SQL file: {e}")

def insert_sample_data(connection):
    """Insert comprehensive sample data for Agra"""
    try:
        cursor = connection.cursor()
        
        # Use the city_guide database
        cursor.execute("USE city_guide")
        
        # Insert more comprehensive data
        sample_data = [
            # More places history
            """INSERT INTO places_history (city_name, place_name, built_year, built_by, historical_importance, cultural_significance, current_status, interesting_facts, best_visit_time, entry_fee) VALUES
            ('Agra', 'Fatehpur Sikri', '1571-1585', 'Emperor Akbar', 'Capital of Mughal Empire for 14 years, planned city showcasing Akbar\'s vision', 'Blend of Hindu, Islamic, and Persian architecture, symbol of religious tolerance', 'UNESCO World Heritage Site, well-preserved ghost city', 'Abandoned due to water scarcity, Akbar\'s tomb is actually in Sikandra not here', 'Early morning or late afternoon', '₹35 for Indians, ₹550 for foreigners'),
            ('Agra', 'Itimad-ud-Daulah', '1622-1628', 'Nur Jahan for her father', 'First Mughal structure built entirely of marble, precursor to Taj Mahal', 'Called Baby Taj, represents transition in Mughal architecture', 'Well-maintained monument, less crowded', 'First use of pietra dura inlay work in Mughal architecture', 'Morning hours', '₹30 for Indians, ₹310 for foreigners')""",
            
            # More food items
            """INSERT INTO local_foods (city_name, food_name, food_type, origin_story, popularity_reason, eating_style, best_time_to_eat, unique_features, local_habits, average_price) VALUES
            ('Agra', 'Jalebi', 'sweet', 'Brought by Persian traders, perfected in Agra', 'Crispy, syrupy sweet perfect with bedai', 'Eaten hot, often with bedai or as dessert', 'Morning with breakfast or evening snack', 'Made fresh, spiral shape, soaked in sugar syrup', 'Always eaten fresh and hot, locals prefer morning jalebi', '₹40-60 per 100g'),
            ('Agra', 'Dalmoth', 'snack', 'Traditional namkeen from Agra, family recipes passed down', 'Spicy lentil mix, perfect tea-time snack', 'Eaten as snack with tea or as side dish', 'Evening tea time', 'Mix of fried lentils, nuts, and spices', 'Locals buy from specific shops, each has unique taste', '₹150-250 per kg'),
            ('Agra', 'Gajak', 'sweet', 'Winter sweet made during sugarcane season', 'Sesame and jaggery sweet, healthy and tasty', 'Eaten as winter sweet, energy booster', 'Winter months (Nov-Feb)', 'Made from sesame seeds and jaggery, very nutritious', 'Seasonal sweet, locals stock up during winter', '₹100-200 per kg')""",
            
            # More restaurants
            """INSERT INTO restaurants_streetfood (city_name, place_name, category, area_location, famous_for, price_range, best_visit_time, popularity, special_notes) VALUES
            ('Agra', 'Dasaprakash', 'mid_range', 'Sadar Bazaar', 'South Indian food, dosa and idli specialist', '₹200-400 per person', 'Breakfast and lunch', 'high', 'Clean vegetarian restaurant, good for families'),
            ('Agra', 'Mama Chicken', 'budget_restaurant', 'Sadar area', 'Non-veg food, chicken specialties', '₹250-400 per person', 'Lunch and dinner', 'high', 'Famous among locals for chicken dishes'),
            ('Agra', 'Sheroes Hangout', 'mid_range', 'Taj Ganj', 'Cafe run by acid attack survivors, continental food', '₹300-500 per person', 'All day', 'medium', 'Social cause cafe, inspiring story, good ambiance')""",
            
            # Transport information
            """INSERT INTO transport_traffic (city_name, transport_type, peak_hours, off_peak_hours, common_routes, local_transport_options, traffic_patterns, time_saving_tips, cost_information) VALUES
            ('Agra', 'General', 'Morning 8-10 AM, Evening 6-8 PM, Weekend evenings', 'Early morning 6-8 AM, Afternoon 12-3 PM, Night after 9 PM', 'Railway Station to Taj Mahal (6km), Sadar to Taj Ganj (4km), Agra Fort to Fatehpur Sikri (40km)', 'Auto Rickshaw (most common), E-Rickshaw (eco-friendly), City Bus (UPSRTC), Cycle Rickshaw (short distance), Prepaid Taxi (railway station)', 'Main roads crowded during office hours, Tourist areas busy in morning and evening, Sadar Bazaar heavy traffic 5-9 PM', 'Book prepaid taxi at railway station, Negotiate auto fare beforehand, Use e-rickshaw for short distances, Avoid main roads during peak hours', 'Auto: ₹10-15 per km, E-rickshaw: ₹8-12 per km, City Bus: ₹5-15, Cycle rickshaw: ₹30-50 for short trips')""",
            
            # Accommodation areas
            """INSERT INTO accommodation (city_name, area_name, category, area_description, suitable_for, safety_rating, convenience_features, nearby_attractions, local_tips) VALUES
            ('Agra', 'Taj Ganj', 'budget', 'Tourist area right next to Taj Mahal, many budget hotels and hostels', 'Backpackers, budget travelers, first-time visitors', 'high', 'Walking distance to Taj Mahal, many restaurants, travel agencies, ATMs', 'Taj Mahal (walking distance), Agra Fort (3km), Mehtab Bagh (2km)', 'Book in advance during peak season, negotiate rates for longer stays'),
            ('Agra', 'Sadar Bazaar Area', 'budget', 'Local commercial area with guesthouses and budget hotels', 'Budget travelers who want local experience', 'medium', 'Local markets, street food, authentic experience, good connectivity', 'Agra Fort (2km), Jama Masjid (1km), local markets', 'Noisy area but authentic local experience, good for food lovers'),
            ('Agra', 'Fatehabad Road', 'mid_range', 'Modern area with good hotels and restaurants', 'Families, business travelers, comfort seekers', 'high', 'Good restaurants, shopping malls, clean area, taxi availability', 'Taj Mahal (5km), Agra Fort (4km), Sikandra (8km)', 'Quieter than tourist areas, good for families with children'),
            ('Agra', 'Taj East Gate Road', 'luxury', 'Premium area with luxury hotels offering Taj views', 'Luxury travelers, honeymooners, special occasions', 'high', 'Taj view rooms, luxury amenities, fine dining, spa services', 'Taj Mahal (direct view), premium shopping', 'Book Taj view rooms well in advance, very expensive during peak season')""",
            
            # Cultural traditions
            """INSERT INTO culture_traditions (city_name, tradition_name, tradition_type, historical_background, current_practice, local_participation, visitor_experience, importance, seasonal_timing) VALUES
            ('Agra', 'Taj Mahotsav', 'festival', 'Annual cultural festival started in 1992 to promote Agra tourism and local arts', ' 10-day festival showcasing local crafts, food, music and dance', 'High local participation, artisans display their work, cultural performances', 'Visitors can see local crafts, taste authentic food, enjoy cultural shows', 'high', 'February (usually 18-27 Feb)'),
            ('Agra', 'Bateshwar Fair', 'festival', 'Ancient cattle fair and religious gathering at Bateshwar (70km from Agra)', 'Traditional cattle trading, religious rituals, folk performances', 'Rural population participates heavily, urban Agra people visit', 'Experience rural culture, see traditional cattle trading, folk music', 'medium', 'October-November (post-monsoon)'),
            ('Agra', 'Ram Barat', 'celebration', 'Traditional wedding procession style celebration during Ram Navami', 'Processions with decorated horses, traditional music, community participation', 'Local Hindu community organizes and participates actively', 'Colorful processions, traditional music, community celebration', 'medium', 'March-April (Ram Navami)')"""
        ]
        
        for sql_command in sample_data:
            try:
                cursor.execute(sql_command)
                connection.commit()
                print("✓ Inserted sample data batch")
            except Error as e:
                print(f"✗ Error inserting data: {e}")
        
        cursor.close()
        print("✓ Sample data insertion completed!")
        
    except Exception as e:
        print(f"Error inserting sample data: {e}")

def main():
    """Main function to initialize database"""
    print("🏛️  Initializing Agra City Guide Database...")
    
    # Create connection
    connection = create_database_connection()
    if not connection:
        print("❌ Failed to connect to MySQL. Please check your database configuration.")
        return
    
    print("✓ Connected to MySQL")
    
    # Execute schema setup
    print("\n📋 Setting up database schema...")
    execute_sql_file(connection, 'backend/database_setup.sql')
    
    # Insert sample data
    print("\n📊 Inserting comprehensive sample data...")
    insert_sample_data(connection)
    
    # Close connection
    connection.close()
    print("\n🎉 Database initialization completed successfully!")
    print("\n📝 Next steps:")
    print("1. Update your .env file with correct database credentials")
    print("2. Install MySQL dependencies: pip install -r requirements.txt")
    print("3. Start the Flask server: python backend/app.py")

if __name__ == "__main__":
    main()