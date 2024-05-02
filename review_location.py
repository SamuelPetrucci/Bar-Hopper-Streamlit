import sqlite3
import requests

class ReviewLocation:
    
    def __init__(self, db_path, api_key):
        self.db_path = db_path
        self.api_key = api_key
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS locations 
                               (id INTEGER PRIMARY KEY, name TEXT, place_id TEXT, demographics TEXT, music TEXT, 
                               best_days TEXT, comments TEXT, polls INTEGER DEFAULT 0)''')
        self.connection.commit()

    def lookup_location(self, location_name):
        # Try to find the location in the SQLlite database
        self.cursor.execute("SELECT * FROM locations WHERE name=?", (location_name,))
        location = self.cursor.fetchone()

        # If the location is not found in the local database, search for it in the Google Maps API
        if not location:
            # Use the Google Maps Places API to search for the location
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={location_name}&key={self.api_key}"
            response = requests.get(url)
            data = response.json()

            # Check if any results are returned
            if data.get("status") == "OK" and data.get("results"):
                # Assume the first result is the correct one (you may want to improve this logic)
                result = data["results"][0]
                place_id = result["place_id"]
                
                # Get the location details using the place_id
                location_details = self.get_location_details(place_id)

                # Add the location to the local database
                self.cursor.execute("INSERT INTO locations (name, place_id, demographics, music, best_days, comments) VALUES (?, ?, ?, ?, ?, ?)",
                                    (location_name, place_id, "", "", "", ""))
                self.connection.commit()

                # Fetch the newly added location from the database
                self.cursor.execute("SELECT * FROM locations WHERE name=?", (location_name,))
                location = self.cursor.fetchone()

        return location

    def upload_review(self, location_name, demographics, music, best_days, comment):
        self.cursor.execute("INSERT INTO locations (name, demographics, music, best_days, comments) VALUES (?, ?, ?, ?, ?)",
                            (location_name, demographics, music, best_days, comment))
        self.connection.commit()

    def get_reviews_for_location(self, location_name):
        self.cursor.execute("SELECT demographics, music, best_days, comments FROM locations WHERE name=?", (location_name,))
        reviews = self.cursor.fetchall()
        
        if not reviews:
            return ["No reviews found for this location."]

        formatted_reviews = []
        for review in reviews:
            demographics, music, best_days, comment = review
            formatted_review = f"Demographics: {demographics}\nMusic: {music}\nBest Days to Attend: {best_days}\nComment: {comment}"
            formatted_reviews.append(formatted_review)

        return formatted_reviews

    def get_all_locations(self):
        self.cursor.execute("SELECT name FROM locations")
        locations = self.cursor.fetchall()
        return [location[0] for location in locations]

    def get_location_details(self, place_id):
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,website,opening_hours,business_status&key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        return data.get("result", {})

