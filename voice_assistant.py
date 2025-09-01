import os
import uuid  # Import the uuid library to generate a unique ID
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# Load environment variables from your .env file
load_dotenv()

# Get your Agent ID and API Key from the environment variables
# Make sure your .env file has AGENT_ID="..." and API_KEY="..."
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

# --- Verify that keys were loaded ---
if not AGENT_ID or not API_KEY:
    print("Error: AGENT_ID or API_KEY not found in .env file.")
    print("Please make sure your .env file is in the same directory and contains the correct variables.")
    exit()
else:
    # --- ADDED FOR DEBUGGING ---
    # This will show you a part of the key being loaded to help verify it.
    print("--- Debug Information ---")
    print(f"Successfully loaded credentials.")
    print(f"Agent ID Loaded (partial): {AGENT_ID[:5]}...{AGENT_ID[-5:]}")
    print(f"API Key Loaded (partial): {API_KEY[:5]}...{API_KEY[-5:]}")
    print("Please verify the partial API key above matches the one on the ElevenLabs website.")
    print("-----------------------\n")


# --- Configure the AI's persona and initial message ---
user_name = "Khushboo"
schedule = "College at 09:00; call with mehek at 17:00"
prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
first_message = f"Hello {user_name}, how can I help you today?"

conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

# --- FIX: Add a unique user_id to the configuration ---
# The library now seems to require a user_id for the session.
config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
    user_id=str(uuid.uuid4()),  # Add a randomly generated user ID
)

# --- Initialize the ElevenLabs client ---
client = ElevenLabs(api_key=API_KEY)

# --- Define callback functions to see the conversation in the terminal ---
def print_agent_response(response: str):
    """Prints the agent's spoken response."""
    print(f"Agent: {response}")

def print_interrupted_response(original: str, corrected: str):
    """Handles cases where the agent is interrupted."""
    print(f"Agent interrupted, truncated response: {corrected}")

def print_user_transcript(transcript: str):
    """Prints the user's transcribed speech."""
    print(f"User: {transcript}")

# --- Create the conversation object once with all settings ---
print("Creating conversation object...")
conversation = Conversation(
    client,
    agent_id=AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

# --- Start the interactive session ---
print("\nStarting conversation session. Speak into your microphone to begin.")
print("The assistant will respond through your speakers.")
print("Press Ctrl+C to end the session.\n")
try:
    conversation.start_session()
except KeyboardInterrupt:
    print("\nSession ended by user.")
finally:
    print("Conversation closed.")


