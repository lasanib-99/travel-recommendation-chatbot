# Travel Recommendation Chatbot

## Overview
This repository contains two applications for travel planning:
1. **Tourism Support Chatbot:** A simple chatbot that provides travel recommendations for Sri Lanka.
2. **LLM-Based Travel Recommender:** A customizable travel recommendation generator for any country, using a large language model (LLM) integrated with a Streamlit web interface.

## Features
### Tourism Support Chatbot
- Developed using Python and Streamlit.
- Specializes in Sri Lankan tourism.
- Provides answers to questions about top attractions, travel tips, and more.

### LLM-Based Travel Recommender
- Utilizes Hugging Face's Phi-3-mini-4k-instruct model for intelligent travel planning.
- Generates personalized travel itineraries based on the destination and trip duration.
- Includes support for chat history, improving responses over time.

## File Structure

travel-recommendation-chatbot ├── app.py # Streamlit app script ├── travel_recommender.py # Core logic for LLM-based recommendations ├── prompt.py # Travel recommendation prompt definition ├── config.py # API configuration and setup ├── requirements.txt # Required Python packages └── .env # API keys (not included in the repository)

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/travel-recommendation-chatbot.git
   cd travel-recommendation-chatbot

2. **Install Dependencies:**

Ensure you have Python 3.8+ and pip installed.
  pip install -r requirements.txt

3. **Set Up Environment Variables:**

Create a .env file in the root directory

HF_TOKEN=<your-hugging-face-api-key>

Run the Application:
  streamlit run app.py

## Usage
1. Navigate to the Streamlit app in your browser.
2. Input the country and trip duration to get tailored recommendations.
3. Optionally ask specific travel-related questions.

## Example Output

Input:

Country: Japan

Days: 5

Question: Are there any heritage sites?

Output:

1. Travel Itinerary:
   - Day 1: Visit Tokyo's bustling Shibuya and historical Asakusa district.
   - Day 2: Explore Kyoto's temples and Arashiyama Bamboo Grove.
   - Day 3: Spend a day in Nara, famous for its deer park and Todai-ji Temple.
   - Day 4: Head to Osaka for street food and the vibrant Dotonbori area.
   - Day 5: Relax at a traditional onsen (hot spring) near Mount Fuji.

2. Regarding your question:
   - Japan has numerous UNESCO World Heritage Sites, including Himeji Castle, Hiroshima Peace Memorial, and the Historic Villages of Shirakawa-go. Be sure to explore Kyoto's iconic Golden Pavilion.
