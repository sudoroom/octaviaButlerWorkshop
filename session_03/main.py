from typing import Callable, List
import tenacity
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import RegexParser
from langchain.prompts import PromptTemplate
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

from agents.bidding_dialogue_agent import BiddingDialogueAgent
from agents.dialogue_agent import DialogueAgent
from simulators.dialogue_simulator import DialogueSimulator
from utils.character_generator import generate_character_header, generate_character_system_message, generate_character_description
 

import os
from dotenv import load_dotenv

load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Define your characters, topic, and word limit here
character_names = [
    "Octavia Butler - Science Fiction Writer",
    "Kara Walker - Artist",
    "Aaron Swartz - persecuted entrepreneur and innovator",
    "Cory Doctorow - Writer",
    "Art Critic - Jason",
    "Hackerspace Director - Jake"
]
topic = "How do we create hackerspace projects in Oakland at SudoRoom that show the true uniqueness of Oakland in a creative way with leftwing ideals and art so that they are not just the standard hackerspace tech products?"
word_limit = 30

game_description = f"""Here is the topic for the hackerspace topic idea to art critic Jason and hackerspace director Jake: {topic}.
The participants are: {', '.join(character_names)}."""

print("Testing BiddingDialogueAgent")
characters = []

## todo: change the model
model=ChatOpenAI(temperature=0.4)

character_descriptions = [
    generate_character_description(character_name, game_description, word_limit) for character_name in character_names
]
character_headers = [
    generate_character_header(character_name, character_description, game_description, topic)
    for character_name, character_description in zip(
        character_names, character_descriptions
    )
]
character_system_messages = [
    generate_character_system_message(character_name, character_headers, topic, word_limit)
    for character_name, character_headers in zip(character_names, character_headers)
]

for character_name, character_system_message, bidding_template in zip(
    character_names, character_system_messages, character_bidding_templates
):
    characters.append(
    BiddingDialogueAgent(
        name=character_name,
        system_message=character_system_message,
        model=model,
        bidding_template=bidding_template,
    )
)
    
    # debugging hack in python
for agent in characters:
    print(f"\nAll attributes of {agent.name}'s BiddingDialogueAgent:")
