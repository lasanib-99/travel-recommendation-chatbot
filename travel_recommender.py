# LLM logic and response generation

from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

from prompt import TRAVEL_PROMPT
from config import MODEL_ID, HF_API_KEY

# Initialize memory and LLM with conversation chain
def init_conversation_chain():

    # Initialize the HuggingFace LLM
    llm = HuggingFaceEndpoint(

        repo_id = MODEL_ID,
        huggingfacehub_api_token = HF_API_KEY,
        temperature = 0.8,
        max_length = 500
        
    )

    # Create the prompt template
    prompt = PromptTemplate(

        template = "{input}", 
        input_variables = ["input"]

    )

    # Create conversation memory
    memory = ConversationBufferMemory(
        memory_key = "history",  # Track the chat history
        
    )

    # Return the LLM chain with memory
    return LLMChain( 
        
        llm = llm, 
        prompt = prompt, 
        memory = memory
           
    )

def format_response(response: str) -> str:
    """
    Cleans up and formats the response to ensure it matches the required format without redundancy.
    """
    # Remove unwanted terms like "AI:" or extra verbose details
    cleaned_response = response.replace("AI:", "").strip()

    # Extract the sections using well-defined markers
    itinerary_start = "Travel Itinerary:"
    question_start = "Regarding your question:"

    # Initialize variables for the sections
    itinerary = ""
    question_answer = ""

    # Locate and extract the travel itinerary section
    if itinerary_start in cleaned_response:
        itinerary = cleaned_response.split(itinerary_start, 1)[1]
        if question_start in itinerary:
            itinerary = itinerary.split(question_start, 1)[0].strip()
        else:
            itinerary = itinerary.strip()

    # Locate and extract the response to the user's question
    if question_start in cleaned_response:
        question_answer = cleaned_response.split(question_start, 1)[1].strip()
        # Stop at the first unintended text after the question answer
        stop_markers = ["What are the", "In conclusion", "Thank you"]
        for marker in stop_markers:
            if marker in question_answer:
                question_answer = question_answer.split(marker, 1)[0].strip()

    # Build the final formatted response
    formatted_response = f"{itinerary_start}\n{itinerary}"
    if question_answer:
        formatted_response += f"\n\n{question_start}\n{question_answer}"

    # Add proper line breaks between sections if missing
    formatted_response = formatted_response.replace("\nDay ", "\n\nDay ")

    return formatted_response.strip()

# Function to get travel recommendations
def get_travel_recoms(conversation_chain, num_days: int, country: str, question: str = "") -> str:

    # Combine inputs into a single string
    history = conversation_chain.memory.load_memory_variables({}).get("history", "")
    
    # Prepare a single input string by formatting the prompt
    input_string = TRAVEL_PROMPT.format(
        history = history,
        country = country,
        num_days = num_days,
        question = question
    )
    
    # Invoke the chain with the single input key
    raw_response = conversation_chain.predict(input = input_string)
    
    # Ensure the output only contains the relevant response
    response = format_response(raw_response)
    
    # Return the formatted response
    return response