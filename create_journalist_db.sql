-- Indian Journalists Database Schema
-- SQLite Database Creation Script

-- Create database tables with proper relationships

-- States table
CREATE TABLE states (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_name TEXT NOT NULL UNIQUE,
    state_code TEXT(2) NOT NULL UNIQUE,
    population INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Districts table
CREATE TABLE districts (
    district_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_id INTEGER NOT NULL,
    district_name TEXT NOT NULL,
    district_code TEXT(3),
    population INTEGER,
    is_media_hub BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES states(state_id),
    UNIQUE(state_id, district_name)
);

-- Journalist organizations table
CREATE TABLE journalist_organizations (
    org_id INTEGER PRIMARY KEY AUTOINCREMENT,
    district_id INTEGER NOT NULL,
    org_name TEXT NOT NULL,
    org_type TEXT CHECK(org_type IN ('club', 'union', 'association', 'guild', 'federation')),
    address TEXT,
    contact_person TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    established_year INTEGER,
    membership_count INTEGER,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);

-- Media outlets table
CREATE TABLE media_outlets (
    outlet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    district_id INTEGER NOT NULL,
    outlet_name TEXT NOT NULL,
    outlet_type TEXT CHECK(outlet_type IN ('newspaper', 'magazine', 'tv', 'radio', 'digital', 'news_agency')),
    primary_language TEXT,
    address TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    circulation TEXT,
    established_year INTEGER,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);

-- Press clubs table
CREATE TABLE press_clubs (
    club_id INTEGER PRIMARY KEY AUTOINCREMENT,
    district_id INTEGER NOT NULL,
    club_name TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    membership_fee TEXT,
    facilities TEXT, -- JSON array of facilities
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);

-- Journalists table
CREATE TABLE journalists (
    journalist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    district_id INTEGER NOT NULL,
    outlet_id INTEGER,
    unique_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    designation TEXT,
    organization TEXT,
    primary_beat TEXT,
    specializations TEXT, -- JSON array of specializations
    experience_years INTEGER,
    languages TEXT, -- JSON array of languages
    education TEXT,
    awards TEXT, -- JSON array of awards
    publications TEXT, -- JSON array of publications
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (district_id) REFERENCES districts(district_id),
    FOREIGN KEY (outlet_id) REFERENCES media_outlets(outlet_id)
);

-- Contact details table
CREATE TABLE journalist_contacts (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    journalist_id INTEGER NOT NULL,
    email TEXT,
    phone TEXT,
    mobile TEXT,
    office_address TEXT,
    twitter TEXT,
    linkedin TEXT,
    facebook TEXT,
    instagram TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (journalist_id) REFERENCES journalists(journalist_id)
);

-- Create indexes for better performance
CREATE INDEX idx_districts_state ON districts(state_id);
CREATE INDEX idx_districts_name ON districts(district_name);
CREATE INDEX idx_journalists_district ON journalists(district_id);
CREATE INDEX idx_journalists_outlet ON journalists(outlet_id);
CREATE INDEX idx_journalists_name ON journalists(name);
CREATE INDEX idx_journalists_unique_id ON journalists(unique_id);
CREATE INDEX idx_organizations_district ON journalist_organizations(district_id);
CREATE INDEX idx_outlets_district ON media_outlets(district_id);
CREATE INDEX idx_contacts_journalist ON journalist_contacts(journalist_id);

-- Create views for common queries
CREATE VIEW v_journalists_with_contacts AS
SELECT 
    j.journalist_id,
    j.unique_id,
    j.name,
    j.designation,
    j.organization,
    j.primary_beat,
    j.experience_years,
    d.district_name,
    s.state_name,
    c.email,
    c.phone,
    c.mobile,
    c.twitter,
    c.linkedin
FROM journalists j
JOIN districts d ON j.district_id = d.district_id
JOIN states s ON d.state_id = s.state_id
LEFT JOIN journalist_contacts c ON j.journalist_id = c.journalist_id
WHERE j.is_active = 1;

CREATE VIEW v_district_summary AS
SELECT 
    s.state_name,
    d.district_name,
    COUNT(j.journalist_id) as journalist_count,
    COUNT(jo.org_id) as organization_count,
    COUNT(mo.outlet_id) as outlet_count,
    COUNT(pc.club_id) as press_club_count
FROM districts d
JOIN states s ON d.state_id = s.state_id
LEFT JOIN journalists j ON d.district_id = j.district_id AND j.is_active = 1
LEFT JOIN journalist_organizations jo ON d.district_id = jo.district_id AND jo.is_active = 1
LEFT JOIN media_outlets mo ON d.district_id = mo.district_id AND mo.is_active = 1
LEFT JOIN press_clubs pc ON d.district_id = pc.district_id AND pc.is_active = 1
GROUP BY d.district_id;

-- Insert sample data for testing
INSERT INTO states (state_name, state_code, population) VALUES 
('Delhi', 'DL', 16787941),
('Maharashtra', 'MH', 112374333),
('Tamil Nadu', 'TN', 72147030),
('Karnataka', 'KA', 61095297),
('West Bengal', 'WB', 91276115);

INSERT INTO districts (state_id, district_name, district_code, population, is_media_hub) VALUES 
(1, 'New Delhi', 'NDL', 249998, 1),
(1, 'South Delhi', 'SDL', 2731929, 1),
(1, 'North Delhi', 'NDL', 887978, 0),
(2, 'Mumbai', 'MUM', 12478447, 1),
(2, 'Pune', 'PUN', 3115431, 1),
(3, 'Chennai', 'CHN', 7090000, 1),
(4, 'Bangalore', 'BLR', 12000000, 1),
(5, 'Kolkata', 'KOL', 4486679, 1); 