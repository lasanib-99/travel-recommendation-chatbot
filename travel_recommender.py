import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from redis import Redis
from langchain.memory import ConversationSummaryMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from prompt import TRAVEL_PROMPT
from config import MODEL_ID, HF_API_KEY
from utils import validate_user_input

# Streamlit app setup
st.set_page_config(page_title="Global Travel Planner", layout="wide")

# Initialize Redis client
def initialize_redis():
    try:
        return Redis(host="localhost", port=6379, decode_responses=True)
    except Exception as e:
        st.error(f"Redis connection failed: {e}")
        return None

redis_client = initialize_redis()

if redis_client is None:
    st.error("Failed to connect to Redis. The app will not work without Redis.")
    st.stop()

# Initialize the conversation chain
def init_conversation_chain(redis_client):
    chat_memory = None

    # Initialize LLM for memory
    llm = HuggingFaceEndpoint(
        repo_id=MODEL_ID,
        huggingfacehub_api_token=HF_API_KEY,
        temperature=0.1
    )

    try:
        # Attempt to use RedisChatMessageHistory if compatible
        chat_memory = RedisChatMessageHistory(
            redis=redis_client,
            key_prefix="chat_history"
        )
    except TypeError as e:
        # Fallback: Direct usage of ConversationSummaryMemory
        st.warning("Falling back to direct Redis usage for memory.")

    # Use ConversationSummaryMemory directly when RedisChatMessageHistory fails
    memory = (
        ConversationSummaryMemory(llm=llm, memory_key="summary")
        if not chat_memory
        else ConversationSummaryMemory(chat_memory=chat_memory, llm=llm)
    )

    # Define the prompt template
    prompt = PromptTemplate(
        template=TRAVEL_PROMPT,
        input_variables=["input"]
    )

    # Return the initialized LLM chain
    return LLMChain(llm=llm, memory=memory, prompt=prompt)

# Initialize session state for conversation chain
if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = init_conversation_chain(redis_client)

# Initialize Streamlit session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "initial_submitted" not in st.session_state:
    st.session_state.initial_submitted = False

# Generate travel recommendations
def get_travel_recoms(chain, country, num_days, question="", history=""):
    try:
        # Combine the inputs into a single string
        input_data = f"""
        Context:
        {history}

        Details:
        - Country: {country}
        - Number of Days: {num_days}
        - User's Question: {question}
        """
        # Generate a response from the LLM chain
        response = chain.predict(input=input_data)
        return response.strip()
    
    except Exception as e:
        return f"Error generating response: {e}"

# Title and instructions
st.title("Chatbot for Global Travel Recommendations")
st.write("Plan your trip with personalized recommendations tailored to your preferences!")

# Clear chat history and reset
def clear_chat():
    st.session_state.chat_history = []
    st.session_state.initial_submitted = False
    if hasattr(st.session_state.conversation_chain.memory, "clear"):
        st.session_state.conversation_chain.memory.clear()
    st.session_state.pop("country", None)
    st.session_state.pop("num_days", None)
    st.session_state.pop("additional_question", None)

# Input section for initial user input
if not st.session_state.get("initial_submitted", False):
    country = st.text_input("Which country are you visiting?", placeholder="Ex: Japan")
    num_days = st.text_input("How many days will you stay?", placeholder="Ex: 5")
    question = st.text_area("Do you have any specific questions about your trip?", placeholder="Ex: Are there any heritage sites?")

    # Submit button
    if st.button("Get Recommendations"):
        if validate_user_input(num_days, country):
            with st.spinner("Fetching travel recommendations..."):
                try:
                    # Store the country and num_days in session state
                    st.session_state["country"] = country.strip()
                    st.session_state["num_days"] = int(num_days.strip())

                    # Extract history from the conversation chain memory
                    memory_vars = st.session_state.conversation_chain.memory.load_memory_variables({})
                    history = memory_vars.get("summary", "")

                    # Fetch recommendations
                    response = get_travel_recoms(
                        chain=st.session_state.conversation_chain,
                        country=country.strip(),
                        num_days=int(num_days.strip()),
                        question=question.strip() if question.strip() else "No specific question.",
                        history=history
                    )

                    # Update session state and display the response immediately
                    st.session_state.chat_history.append({
                        "input": f"Country: {country}, Days: {num_days}, Question: {question}",
                        "response": response
                    })
                    st.session_state["initial_submitted"] = True
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.error("Please provide a valid country and number of days.")

# Follow-up question and chat history display
else:
    st.write("### Trip Recommendations")
    latest_chat = st.session_state.chat_history[-1] 
    st.write(f"**Details:** {latest_chat['input']}")
    st.write(f"**Response:** {latest_chat['response']}")

    # Follow-up question input
    additional_question = st.text_area("Have more questions? Ask below!", key="additional_question")
    if st.button("Submit Follow-Up Question"):
        if additional_question.strip():
            with st.spinner("Generating follow-up response..."):
                try:
                    # Extract history from the conversation chain memory
                    memory_vars = st.session_state.conversation_chain.memory.load_memory_variables({})
                    history = memory_vars.get("summary", "")

                    # Generate follow-up response
                    response = get_travel_recoms(
                        chain=st.session_state.conversation_chain,
                        country=st.session_state["country"],  
                        num_days=st.session_state["num_days"], 
                        question=additional_question.strip(),
                        history=history
                    )

                    # Append response to chat history
                    st.session_state.chat_history.append({
                        "input": f"Follow-Up Question: {additional_question}",
                        "response": response
                    })
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.error("Please enter a valid question.")

# Clear chat history button
if st.button("Clear Chat History"):
    clear_chat()