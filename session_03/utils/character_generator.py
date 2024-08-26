def generate_character_description(character_name: str, game_description: str, word_limit: int) -> str:
    # Implement Ollama call here to generate character description
    return f"Character description for {character_name}"

def generate_character_header(character_name: str, character_description: str, game_description: str, topic: str) -> str:
    return f"""{game_description}
Your name is {character_name}.
Your description is as follows: {character_description}
Your topic is: {topic}.
"""

def generate_character_system_message(character_name: str, character_header: str, word_limit: int) -> str:
    return f"""{character_header}
You will speak in the style of {character_name}, and exaggerate their personality RESPONDING in under 450 characters.
You will come up with creative ideas related to the topic.
Do not say the same things over and over again.
Speak in the first person from the perspective of {character_name}
For describing your own body movements, wrap your description in '*'.
Do not change roles!
Do not speak from the perspective of anyone else.
Speak only from the perspective of {character_name}.
Stop speaking the moment you finish speaking from your perspective.
Never forget to keep your response to {word_limit} words!
Do not add anything else.
"""

def generate_character_bidding_template(character_header: str) -> str:
    return f"""{character_header}

```
{{message_history}}
```

On the scale of 1 to 10, where 1 is least important to the startup pitch and 10 is extremely important and contribute, rank your recent message based on the context. Make sure to be very thorough in your ranking and only rank stuff that is important higher.

```
{{recent_message}}
```

Your response should be an integer delimited by angled brackets, like this: <int>.
Do nothing else.
"""