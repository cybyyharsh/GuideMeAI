-- City Guide Database Schema
-- Run this script to set up the database structure

CREATE DATABASE IF NOT EXISTS city_guide;
USE city_guide;

-- ========================================
-- USER MANAGEMENT TABLES (NEW EXTENSION)
-- ========================================

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    dob DATE,
    email VARCHAR(150) UNIQUE,
    mobile VARCHAR(20) UNIQUE,
    pin_code VARCHAR(10),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User Login Table (Auth Layer)
CREATE TABLE IF NOT EXISTS user_auth (
    auth_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    login_type ENUM('email','mobile','guest') NOT NULL,
    login_identifier VARCHAR(150),
    is_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Guest Session Table
CREATE TABLE IF NOT EXISTS guest_sessions (
    guest_id INT AUTO_INCREMENT PRIMARY KEY,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 24 HOUR)
);

-- User Preferences Table (for personalization)
CREATE TABLE IF NOT EXISTS user_preferences (
    pref_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    preferred_city VARCHAR(100),
    food_preferences TEXT,
    budget_range ENUM('budget','mid_range','luxury') DEFAULT 'mid_range',
    travel_style ENUM('solo','family','business','group') DEFAULT 'solo',
    language_preference ENUM('hindi','hinglish','english') DEFAULT 'hinglish',
    tone_preference ENUM('concise', 'detailed') DEFAULT 'detailed',
    interests TEXT,
    ui_preferences JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========================================
-- EXISTING CITY GUIDE TABLES (UNCHANGED)
-- ========================================

-- City Overview Table
CREATE TABLE IF NOT EXISTS city_overview (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_name VARCHAR(100) NOT NULL,
    historical_background TEXT,
    cultural_significance TEXT,
    daily_life_description TEXT,
    unique_features TEXT,
    population INT,
    best_time_to_visit VARCHAR(200),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Places and Monuments History
CREATE TABLE IF NOT EXISTS places_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    place_name VARCHAR(200) NOT NULL,
    built_year VARCHAR(50),
    built_by VARCHAR(200),
    historical_importance TEXT,
    cultural_significance TEXT,
    current_status TEXT,
    interesting_facts TEXT,
    best_visit_time VARCHAR(100),
    entry_fee VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Markets and Streets History
CREATE TABLE IF NOT EXISTS markets_streets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    market_name VARCHAR(200) NOT NULL,
    area_type ENUM('market', 'street', 'bazaar') DEFAULT 'market',
    historical_origin TEXT,
    evolution_story TEXT,
    current_significance TEXT,
    popular_items TEXT,
    best_visit_time VARCHAR(100),
    local_tips TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Local Foods Information
CREATE TABLE IF NOT EXISTS local_foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    food_name VARCHAR(200) NOT NULL,
    food_type ENUM('street_food', 'restaurant_food', 'sweet', 'snack') DEFAULT 'street_food',
    origin_story TEXT,
    popularity_reason TEXT,
    eating_style TEXT,
    best_time_to_eat VARCHAR(100),
    unique_features TEXT,
    local_habits TEXT,
    average_price VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restaurants and Street Food Places
CREATE TABLE IF NOT EXISTS restaurants_streetfood (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    place_name VARCHAR(200) NOT NULL,
    category ENUM('street_food', 'budget_restaurant', 'mid_range', 'fine_dining') DEFAULT 'street_food',
    area_location VARCHAR(200),
    famous_for TEXT,
    price_range VARCHAR(100),
    best_visit_time VARCHAR(100),
    local_popularity INT DEFAULT 0,
    popularity ENUM('low', 'medium', 'high', 'very_high') DEFAULT 'medium',
    special_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tourist Places and Attractions
CREATE TABLE IF NOT EXISTS tourist_places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    place_name VARCHAR(200) NOT NULL,
    category ENUM('monument', 'museum', 'park', 'religious', 'market', 'hidden_gem') DEFAULT 'monument',
    importance ENUM('must_visit', 'recommended', 'optional') DEFAULT 'recommended',
    why_visit TEXT,
    best_visit_time VARCHAR(100),
    duration_needed VARCHAR(50),
    entry_fee VARCHAR(100),
    local_tips TEXT,
    avoid_mistakes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transport and Traffic Information
CREATE TABLE IF NOT EXISTS transport_traffic (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    transport_type VARCHAR(100),
    peak_hours VARCHAR(200),
    off_peak_hours VARCHAR(200),
    common_routes TEXT,
    local_transport_options TEXT,
    traffic_patterns TEXT,
    time_saving_tips TEXT,
    cost_information TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accommodation Information
CREATE TABLE IF NOT EXISTS accommodation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    area_name VARCHAR(200) NOT NULL,
    category ENUM('budget', 'mid_range', 'luxury') DEFAULT 'mid_range',
    area_description TEXT,
    suitable_for TEXT,
    safety_rating ENUM('low', 'medium', 'high') DEFAULT 'medium',
    convenience_features TEXT,
    nearby_attractions TEXT,
    local_tips TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Culture and Traditions
CREATE TABLE IF NOT EXISTS culture_traditions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    tradition_name VARCHAR(200) NOT NULL,
    tradition_type ENUM('festival', 'custom', 'celebration', 'ritual') DEFAULT 'festival',
    historical_background TEXT,
    current_practice TEXT,
    local_participation TEXT,
    visitor_experience TEXT,
    importance ENUM('low', 'medium', 'high') DEFAULT 'medium',
    seasonal_timing VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Data for Agra
INSERT INTO city_overview (city_name, state_name, historical_background, cultural_significance, daily_life_description, unique_features, population, best_time_to_visit, latitude, longitude) VALUES
('Agra', 'Uttar Pradesh', 
'Agra was the capital of Mughal Empire from 1556 to 1658. Founded by Sultan Sikandar Lodi in 1504, it became the center of Mughal power under Akbar, Jahangir, and Shah Jahan.',
'Known worldwide for Taj Mahal, Agra represents Mughal architecture and Indo-Islamic culture. The city is a UNESCO World Heritage site with three monuments.',
'Daily life revolves around tourism and local markets. Mornings start with bedai-jalebi culture, evenings come alive in Sadar Bazaar. People are warm and helpful to visitors.',
'Home to Taj Mahal, Agra Fort, and Fatehpur Sikri. Famous for petha sweets, leather goods, and marble handicrafts. Street food culture is very strong.',
1685000, 'October to March - pleasant weather, clear skies for monument photography', 27.1767, 78.0081);

INSERT INTO places_history (city_name, place_name, built_year, built_by, historical_importance, cultural_significance, current_status, interesting_facts, best_visit_time, entry_fee, latitude, longitude) VALUES
('Agra', 'Taj Mahal', '1632-1653', 'Emperor Shah Jahan', 'Built as mausoleum for wife Mumtaz Mahal, symbol of eternal love', 'UNESCO World Heritage Site, Wonder of the World, represents Mughal architecture peak', 'Active monument with millions of visitors yearly', 'Changes color throughout the day - pinkish at dawn, white at noon, golden at sunset', 'Sunrise and sunset for best lighting', '₹50 for Indians, ₹1100 for foreigners', 27.1751, 78.0421),
('Agra', 'Agra Fort', '1565-1573', 'Emperor Akbar', 'Main residence of Mughal emperors, military stronghold', 'Red sandstone fort showcasing Mughal military architecture', 'UNESCO World Heritage Site, well-maintained', 'Shah Jahan was imprisoned here by his son Aurangzeb, could see Taj Mahal from his prison', 'Morning hours to avoid heat', '₹35 for Indians, ₹550 for foreigners', 27.1795, 78.0211);

INSERT INTO local_foods (city_name, food_name, food_type, origin_story, popularity_reason, eating_style, best_time_to_eat, unique_features, local_habits, average_price) VALUES
('Agra', 'Petha', 'sweet', 'Started in Mughal era, made from ash gourd (petha vegetable)', 'Unique sweet that stays fresh for days, perfect travel sweet', 'Eaten as dessert or snack, often bought as gift', 'Anytime, especially after meals', 'Made from ash gourd, comes in many flavors - plain, chocolate, coconut', 'Locals buy it for relatives when traveling, tourists take it as souvenir', '₹200-500 per kg'),
('Agra', 'Bedai', 'street_food', 'Traditional breakfast from Mughal period, popular among locals', 'Crispy, flaky bread perfect with spicy potato curry', 'Eaten hot with aloo sabzi and jalebi', 'Morning 7-10 AM', 'Deep fried bread that puffs up, served with spicy potato curry', 'Essential morning breakfast, eaten at street stalls with hands', '₹30-50 per plate');

INSERT INTO restaurants_streetfood (city_name, place_name, category, area_location, famous_for, price_range, best_visit_time, popularity, special_notes) VALUES
('Agra', 'Deviram Sweets', 'street_food', 'Near Raja Mandi', 'Famous bedai-jalebi, morning breakfast specialist', '₹30-80 per person', 'Morning 7-10 AM', 'very_high', 'Most famous breakfast spot, locals queue up every morning'),
('Agra', 'Panchhi Petha', 'street_food', 'Multiple locations', 'Original Agra petha, established brand', '₹200-500 per kg', 'Anytime', 'very_high', 'Most authentic petha shop, tourists favorite for gifts'),
('Agra', 'Joney\'s Place', 'budget_restaurant', 'Taj Ganj area', 'Budget North Indian food, backpacker favorite', '₹150-300 per person', 'Lunch and dinner', 'high', 'Popular with budget travelers, good Indian food');

-- Add more sample data as needed...