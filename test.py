'''

import folium.map
from Token import GOOGLE_API_KEY
import streamlit as st
import requests
from streamlit_folium import folium_static

# Function to fetch bars near a zip code using the Google Maps API
def get_bars_near_zip(location):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars+and+nightclubs+in+{location}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data["results"]

# Function to fetch additional details for a location using the Google Maps Place Details API
def get_location_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,website,opening_hours,business_status&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("result", {})


# Streamlit app
def main():
  st.title("Nightlife Finder")
  zip_code = st.text_input("Enter a Location (City, State) or Zip Code:")
  if st.button("Find Nighlife"):
      if zip_code:
        bars = get_bars_near_zip(zip_code)
        # Create a map centered around the zip code area

        # Get the latitude and longitude of the zip code using the Google Maps Geocoding API
        geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={GOOGLE_API_KEY}"
        geocoding_response = requests.get(geocoding_url)
        geocoding_data = geocoding_response.json()
        location = geocoding_data["results"][0]["geometry"]["location"]

        # Create a map centered around the zip code area
        m = folium.Map(location=[location["lat"], location["lng"]], zoom_start=12)
        for bar in bars:
                # Add a marker for each bar
            folium.Marker([bar["geometry"]["location"]["lat"], bar["geometry"]["location"]["lng"]],
                              popup=bar["name"]).add_to(m)
            # Display the map in the Streamlit app
        folium_static(m)

        # Display additional details for each location
        st.subheader("Bar Details:")
        for bar in bars:
            location_details = get_location_details(bar["place_id"])
            st.write(f"**Name:** {location_details['name']}")
            st.write(f"**Address:** {location_details.get('formatted_address', 'N/A')}")
            st.write(f"**Website:** {location_details.get('website', 'N/A')}")
            st.write(f"**Business Status:** {location_details.get('business_status', 'N/A')}")
            if 'opening_hours' in location_details:
                opening_hours = location_details['opening_hours']['weekday_text']
                opening_hours_str = "\n".join(opening_hours)
                st.write(f"**Opening Hours:** \n{opening_hours_str}")
            st.write("---")

                


if __name__ == "__main__":
    main()
'''



