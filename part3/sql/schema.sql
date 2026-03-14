-- =====================================================
-- HBnB DATABASE SCHEMA
-- This script creates all tables required for the app
-- =====================================================


-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email VARCHAR(128) UNIQUE NOT NULL,

    first_name VARCHAR(128) NOT NULL,

    last_name VARCHAR(128) NOT NULL,

    password VARCHAR(128) NOT NULL,

    is_admin BOOLEAN DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- PLACES TABLE
-- =========================
CREATE TABLE places (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name VARCHAR(128) NOT NULL,

    description TEXT,

    price FLOAT NOT NULL,

    latitude FLOAT,

    longitude FLOAT,

    owner_id INTEGER NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key linking place owner
    FOREIGN KEY (owner_id) REFERENCES users(id)
);


-- =========================
-- REVIEWS TABLE
-- =========================
CREATE TABLE reviews (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    text TEXT NOT NULL,

    rating INTEGER NOT NULL,

    user_id INTEGER NOT NULL,

    place_id INTEGER NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys linking review
    FOREIGN KEY (user_id) REFERENCES users(id),

    FOREIGN KEY (place_id) REFERENCES places(id)
);


-- =========================
-- AMENITIES TABLE
-- =========================
CREATE TABLE amenities (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name VARCHAR(128) UNIQUE NOT NULL,

    description TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- PLACE_AMENITY TABLE
-- (Many-to-many relationship)
-- =========================
CREATE TABLE place_amenity (

    place_id INTEGER NOT NULL,

    amenity_id INTEGER NOT NULL,

    PRIMARY KEY (place_id, amenity_id),

    FOREIGN KEY (place_id) REFERENCES places(id),

    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);


-- =====================================================
-- INITIAL DATA
-- =====================================================


-- Insert ADMIN USER
INSERT INTO users (
    email,
    first_name,
    last_name,
    password,
    is_admin
) VALUES (
    'admin@hbnb.com',
    'Admin',
    'User',
    'hashedpassword123',
    1
);


-- Insert default amenities
INSERT INTO amenities (name, description) VALUES
('WiFi', 'Wireless internet access'),
('Pool', 'Swimming pool'),
('Parking', 'Free parking space'),
('Air Conditioning', 'Cooling system'),
