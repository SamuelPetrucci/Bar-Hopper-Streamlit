import streamlit as st
from nightlife_finder import NightlifeFinder
from about import About
from review_location import ReviewLocation
##from locationSurvey import Review
from Token import GOOGLE_API_KEY

def main():
    finder = NightlifeFinder(GOOGLE_API_KEY)
    about = About()
    review_location = ReviewLocation('review.db', GOOGLE_API_KEY)

    st.image("barhopperlogo.png", width=250)

    page = st.sidebar.selectbox("", ["About", "Find Nightlife", "Review Place"])


    if page == "About":
        about.display()
    elif page == "Find Nightlife":
        location = finder.get_user_location_input()
        if finder.display_find_nightlife_button():
            if location:
                finder.display_bars_map(location)
    elif page == "Review Place":
        location_name = st.text_input("Enter the name of the bar:")
        if st.button("Lookup Location"):
            location = review_location.lookup_location(location_name) ##Finds the location in the database
            if location: 
                st.write(f"Location: {location_name}")
                st.write("Reviews:")
                for review in review_location.get_reviews_for_location(location_name):
                    st.write(f"- {review}")
            else:
                st.write("Location not found.")
    
            # Show the review form
        demographics = st.text_input("Demographics", "")
        music = st.text_input("Music", "")
        best_days = st.text_input("Best Days to Attend", "")
        comment = st.text_area("Comment", "")
        if st.button("Submit Review"):
            review_location.upload_review(location_name, demographics, music, best_days, comment)
            st.success("Review submitted successfully!")

if __name__ == "__main__":
    main()
