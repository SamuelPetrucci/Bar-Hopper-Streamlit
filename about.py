import streamlit as st

class About:
    @staticmethod
    def display():
        
        st.subheader("About")
        st.write("""
        This is a Nightlife Finder app that allows you to discover bars and nightclubs near a particular location. 
        It uses the Google Maps API to search for bars and display them on a folium map, along with 
                 details such as address, website, and opening hours.
        """)

        st.subheader("Future Plans 🚀")
        st.write("""
        Here are some future plans for the Bar-Hopper app:
        - Implement user profiles and authentication for personalized experiences
        - Introduce polling functionality for each location, allowing users to vote on:
            - Demographic of patrons (e.g., young, old)
            - Type of music played
            - Vibe of the place (e.g., rowdy, chill)
        """)


