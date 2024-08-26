import os
from agents.bidding_dialogue_agent import BiddingDialogueAgent
from simulators.dialogue_simulator import DialogueSimulator
from utils.character_generator import generate_character_description, generate_character_header, generate_character_system_message, generate_character_bidding_template
from utils.bid_parser import ask_for_bid
import numpy as np

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

def select_next_speaker(step: int, agents: list) -> int:
    bids = []
    for agent in agents:
        bid = ask_for_bid(agent)
        bids.append(bid)

    max_value = np.max(bids)
    max_indices = np.where(bids == max_value)[0]
    idx = np.random.choice(max_indices)

    print("Bids:")
    for i, (bid, agent) in enumerate(zip(bids, agents)):
        print(f"\t{agent.name} bid: {bid}")
        if i == idx:
            selected_name = agent.name
    print(f"Selected: {selected_name}")
    print("\n")
    return idx

def main():
    characters = []
    
    for character_name in character_names:
        character_description = generate_character_description(character_name, game_description, word_limit)
        character_header = generate_character_header(character_name, character_description, game_description, topic)
        character_system_message = generate_character_system_message(character_name, character_header, word_limit)
        bidding_template = generate_character_bidding_template(character_header)
        
        characters.append(
            BiddingDialogueAgent(
                name=character_name,
                system_message=character_system_message,
                bidding_template=bidding_template,
            )
        )

    simulator = DialogueSimulator(agents=characters, selection_function=select_next_speaker)
    simulator.reset()

    first_message = "Octavia, Kara, Aaron and Cory, You can now start pitching your ideas for our hackerspace to Jake and the museum director"
    simulator.inject("Moderator", first_message)
    print(f"(Moderator): {first_message}\n")

    max_iters = 20
    for _ in range(max_iters):
        name, message = simulator.step()
        print(f"({name}): {message}\n")

if __name__ == "__main__":
    main()
