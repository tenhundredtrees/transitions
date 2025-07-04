#!/usr/bin/env python3
"""
Indian Journalists Database Manager
SQLite-based database management for journalist information
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class JournalistDBManager:
    def __init__(self, db_path: str = "journalists.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def create_database(self, schema_file: str = "create_journalist_db.sql"):
        """Create database from schema file"""
        try:
            with open(schema_file, 'r') as f:
                schema = f.read()
            
            self.cursor.executescript(schema)
            self.conn.commit()
            print("Database created successfully")
        except Exception as e:
            print(f"Error creating database: {e}")
            raise
    
    def add_state(self, state_name: str, state_code: str, population: int = None) -> int:
        """Add a new state"""
        try:
            self.cursor.execute("""
                INSERT INTO states (state_name, state_code, population)
                VALUES (?, ?, ?)
            """, (state_name, state_code, population))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"State {state_name} already exists")
            return None
    
    def add_district(self, state_name: str, district_name: str, district_code: str = None, 
                    population: int = None, is_media_hub: bool = False) -> int:
        """Add a new district"""
        try:
            # Get state_id
            self.cursor.execute("SELECT state_id FROM states WHERE state_name = ?", (state_name,))
            state_result = self.cursor.fetchone()
            if not state_result:
                raise ValueError(f"State {state_name} not found")
            
            state_id = state_result['state_id']
            
            self.cursor.execute("""
                INSERT INTO districts (state_id, district_name, district_code, population, is_media_hub)
                VALUES (?, ?, ?, ?, ?)
            """, (state_id, district_name, district_code, population, is_media_hub))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"District {district_name} in {state_name} already exists")
            return None
    
    def add_journalist_organization(self, district_name: str, org_name: str, org_type: str,
                                  address: str = None, contact_person: str = None,
                                  phone: str = None, email: str = None, website: str = None,
                                  established_year: int = None, membership_count: int = None) -> int:
        """Add a journalist organization"""
        try:
            # Get district_id
            self.cursor.execute("""
                SELECT d.district_id FROM districts d
                JOIN states s ON d.state_id = s.state_id
                WHERE d.district_name = ?
            """, (district_name,))
            district_result = self.cursor.fetchone()
            if not district_result:
                raise ValueError(f"District {district_name} not found")
            
            district_id = district_result['district_id']
            
            self.cursor.execute("""
                INSERT INTO journalist_organizations 
                (district_id, org_name, org_type, address, contact_person, phone, email, website, established_year, membership_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (district_id, org_name, org_type, address, contact_person, phone, email, website, established_year, membership_count))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding organization: {e}")
            return None
    
    def add_media_outlet(self, district_name: str, outlet_name: str, outlet_type: str,
                        primary_language: str = None, address: str = None,
                        phone: str = None, email: str = None, website: str = None,
                        circulation: str = None, established_year: int = None) -> int:
        """Add a media outlet"""
        try:
            # Get district_id
            self.cursor.execute("""
                SELECT d.district_id FROM districts d
                JOIN states s ON d.state_id = s.state_id
                WHERE d.district_name = ?
            """, (district_name,))
            district_result = self.cursor.fetchone()
            if not district_result:
                raise ValueError(f"District {district_name} not found")
            
            district_id = district_result['district_id']
            
            self.cursor.execute("""
                INSERT INTO media_outlets 
                (district_id, outlet_name, outlet_type, primary_language, address, phone, email, website, circulation, established_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (district_id, outlet_name, outlet_type, primary_language, address, phone, email, website, circulation, established_year))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding media outlet: {e}")
            return None
    
    def add_journalist(self, district_name: str, unique_id: str, name: str,
                      designation: str = None, organization: str = None,
                      primary_beat: str = None, specializations: List[str] = None,
                      experience_years: int = None, languages: List[str] = None,
                      education: str = None, awards: List[str] = None,
                      publications: List[str] = None) -> int:
        """Add a journalist"""
        try:
            # Get district_id
            self.cursor.execute("""
                SELECT d.district_id FROM districts d
                JOIN states s ON d.state_id = s.state_id
                WHERE d.district_name = ?
            """, (district_name,))
            district_result = self.cursor.fetchone()
            if not district_result:
                raise ValueError(f"District {district_name} not found")
            
            district_id = district_result['district_id']
            
            # Convert lists to JSON strings
            specializations_json = json.dumps(specializations) if specializations else None
            languages_json = json.dumps(languages) if languages else None
            awards_json = json.dumps(awards) if awards else None
            publications_json = json.dumps(publications) if publications else None
            
            self.cursor.execute("""
                INSERT INTO journalists 
                (district_id, unique_id, name, designation, organization, primary_beat, 
                 specializations, experience_years, languages, education, awards, publications)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (district_id, unique_id, name, designation, organization, primary_beat,
                  specializations_json, experience_years, languages_json, education, awards_json, publications_json))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Journalist with ID {unique_id} already exists")
            return None
        except Exception as e:
            print(f"Error adding journalist: {e}")
            return None
    
    def add_journalist_contact(self, unique_id: str, email: str = None, phone: str = None,
                              mobile: str = None, office_address: str = None,
                              twitter: str = None, linkedin: str = None,
                              facebook: str = None, instagram: str = None) -> int:
        """Add contact details for a journalist"""
        try:
            # Get journalist_id
            self.cursor.execute("SELECT journalist_id FROM journalists WHERE unique_id = ?", (unique_id,))
            journalist_result = self.cursor.fetchone()
            if not journalist_result:
                raise ValueError(f"Journalist with ID {unique_id} not found")
            
            journalist_id = journalist_result['journalist_id']
            
            self.cursor.execute("""
                INSERT INTO journalist_contacts 
                (journalist_id, email, phone, mobile, office_address, twitter, linkedin, facebook, instagram)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (journalist_id, email, phone, mobile, office_address, twitter, linkedin, facebook, instagram))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding contact: {e}")
            return None
    
    def get_journalists_by_district(self, district_name: str, limit: int = 50) -> List[Dict]:
        """Get journalists from a specific district"""
        try:
            self.cursor.execute("""
                SELECT 
                    j.unique_id,
                    j.name,
                    j.designation,
                    j.organization,
                    j.primary_beat,
                    j.experience_years,
                    c.email,
                    c.phone,
                    c.mobile,
                    c.twitter,
                    c.linkedin
                FROM journalists j
                LEFT JOIN journalist_contacts c ON j.journalist_id = c.journalist_id
                JOIN districts d ON j.district_id = d.district_id
                WHERE d.district_name = ? AND j.is_active = 1
                ORDER BY j.name
                LIMIT ?
            """, (district_name, limit))
            
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(row))
            
            return results
        except Exception as e:
            print(f"Error querying journalists: {e}")
            return []
    
    def get_district_summary(self) -> List[Dict]:
        """Get summary statistics for all districts"""
        try:
            self.cursor.execute("SELECT * FROM v_district_summary ORDER BY state_name, district_name")
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(row))
            return results
        except Exception as e:
            print(f"Error getting district summary: {e}")
            return []
    
    def search_journalists(self, search_term: str, limit: int = 50) -> List[Dict]:
        """Search journalists by name, organization, or beat"""
        try:
            search_pattern = f"%{search_term}%"
            self.cursor.execute("""
                SELECT 
                    j.unique_id,
                    j.name,
                    j.designation,
                    j.organization,
                    j.primary_beat,
                    d.district_name,
                    s.state_name,
                    c.email,
                    c.phone,
                    c.twitter
                FROM journalists j
                LEFT JOIN journalist_contacts c ON j.journalist_id = c.journalist_id
                JOIN districts d ON j.district_id = d.district_id
                JOIN states s ON d.state_id = s.state_id
                WHERE (j.name LIKE ? OR j.organization LIKE ? OR j.primary_beat LIKE ?)
                AND j.is_active = 1
                ORDER BY j.name
                LIMIT ?
            """, (search_pattern, search_pattern, search_pattern, limit))
            
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(row))
            
            return results
        except Exception as e:
            print(f"Error searching journalists: {e}")
            return []
    
    def export_to_csv(self, filename: str, query: str, params: tuple = ()):
        """Export query results to CSV"""
        try:
            import csv
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            if not rows:
                print("No data to export")
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows([dict(row) for row in rows])
            
            print(f"Data exported to {filename}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

def main():
    """Main function for testing"""
    db_manager = JournalistDBManager()
    
    try:
        db_manager.connect()
        
        # Create database if it doesn't exist
        if not os.path.exists(db_manager.db_path):
            db_manager.create_database()
        
        # Example usage
        print("Database manager initialized successfully")
        
        # Get district summary
        summary = db_manager.get_district_summary()
        print(f"Found {len(summary)} districts in database")
        
        # Search for journalists
        journalists = db_manager.search_journalists("Delhi", limit=10)
        print(f"Found {len(journalists)} journalists in Delhi")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main() 