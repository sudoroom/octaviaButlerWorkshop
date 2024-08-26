from typing import Callable, List
import tenacity
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import RegexParser
from langchain.prompts import PromptTemplate
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
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
