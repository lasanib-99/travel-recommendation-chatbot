# Streamlit application

import streamlit as st
from travel_recommender import init_conversation_chain, get_travel_recoms

# Initialize Streamlit app
st.set_page_config(page_title = "Global Travel Recommendations", layout = "wide")

# Title and instructions

st.title("Chatbot for Global Travel Recommendations")

st.write("Plan your trip with tailored recommendations based on the country and duration!")

# Initialize the conversation chain and memory
if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = init_conversation_chain()

# Input fields for country, number of days

country = st.text_input("Enter the country you are visiting:", placeholder = "Ex: Japan")

num_days = st.text_input("Enter the number of days you plan to stay there:", placeholder = "Ex: 5")

question = st.text_area("Do you have any other questions? (Optional)", placeholder = "Ex: Are there any heritage sites?")

# Submit button
if st.button("Get Recommendations"):

    if country.strip() and num_days.strip().isdigit() and int(num_days) > 0:

        with st.spinner("Fetching travel recommendations..."):

            try:
                
                # Get travel recommendations based on the initial inputs
                response = get_travel_recoms(

                    st.session_state.conversation_chain,
                    num_days = int(num_days),
                    country = country.strip(),
                    question = question.strip() if question.strip() else "No specific question."

                )

                # Display response
                st.subheader("Your travel recommendations:")
                st.write(response)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        st.error("Please enter a valid country name and a positive number of days.")


# Clear chat history button
if st.button("Clear Chat History"):

    # Clear the conversation memory
    st.session_state.conversation_chain.memory.clear()