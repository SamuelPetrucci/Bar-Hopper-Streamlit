import requests
import folium
from streamlit_folium import folium_static
import streamlit as st
class NightlifeFinder:
    
    #Constructor initializes the GooglAPIKey
    def __init__(self, api_key):
        self.api_key = api_key

    #Locates nightlife in a particular area 
    def get_bars_near_zip(self, location):
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars+and+nightclubs+in+{location}&key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        return data["results"]
    
    #obtains the details on a location (name, adress, website, hours)
    def get_location_details(self, place_id):
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,website,opening_hours,business_status&key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        return data.get("result", {})

    
    def display_bars_map(self, location):
        bars = self.get_bars_near_zip(location)
        geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={self.api_key}"
        geocoding_response = requests.get(geocoding_url)
        geocoding_data = geocoding_response.json()
        
        #Checks If user typed in a valid location
        if geocoding_data.get("status") != "OK" or not geocoding_data.get("results"):
            st.write("No location found. Please enter a valid location.")
            return
        
        location = geocoding_data["results"][0]["geometry"]["location"]

        ## Places the map view in vicinity of the coordinates
        m = folium.Map(location=[location["lat"], location["lng"]], zoom_start=12) 
        for bar in bars:
             ## Drops a marker at each locations coordinates 
            folium.Marker([bar["geometry"]["location"]["lat"], bar["geometry"]["location"]["lng"]],
                          popup=bar["name"]).add_to(m)                                             
        # Display the map in the Streamlit app
        folium_static(m) 

        ## Displays the details of the location 
        st.subheader("Bar Details:")
        for bar in bars:
            location_details = self.get_location_details(bar["place_id"])
            st.write(f"**Name:** {location_details['name']}")
            st.write(f"**Address:** {location_details.get('formatted_address', 'N/A')}")
            st.write(f"**Website:** {location_details.get('website', 'N/A')}")
            if 'opening_hours' in location_details:
                opening_hours = location_details['opening_hours']['weekday_text']
                opening_hours_str = "\n".join(opening_hours)
                st.write(f"**Opening Hours:** \n{opening_hours_str}")
            st.write("---")
    
    def get_user_location_input(self):
        return st.text_input("Enter a Location (City, State) or Zip Code:")

    def display_find_nightlife_button(self):
        return st.button("Find Nightlife")
