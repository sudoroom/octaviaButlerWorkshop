from typing import List, Callable
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
class DialogueAgent:
    def __init__(
        self,
        name: str,
        system_message: SystemMessage,
        model: ChatOllama,
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.prefix = f"{self.name}: "
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        # chatOpenAI
        # message = self.model(
        #     [
        #         self.system_message,
        #         HumanMessage(content="\n".join(self.message_history + [self.prefix])),
        #     ]
        # )
        # return message.content
        # messages = [
        #     ("system", flatten_content(self.system_message.content)),
        #     ("human", "\n".join(self.message_history + [self.prefix]))
        # ]
        # # response = self.model.invoke(prompt)
        # final_message = self.model.invoke(messages)
        # return final_message
        system_content_flattened = flatten_content(self.system_message.content)
        human_content_flattened =  "\n".join(self.message_history + [self.prefix])
        prompt = f"System: {system_content_flattened}\n\Human: {human_content_flattened}"
        # print(prompt)
        final_message = self.model.invoke(prompt)
        return final_message
        
                                   
      

    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")

def flatten_content(content):
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return " ".join(str(item) for item in content)
    else:
        raise ValueError(f"Unexpected content type: {type(content)}")
    
class DialogueSimulator:
    def __init__(
        self,
        agents: List[DialogueAgent],
        selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._step = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def inject(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        # increment time
        self._step += 1

    def step(self) -> tuple[str, str]:
        # 1. choose the next speaker
        speaker_idx = self.select_next_speaker(self._step, self.agents)
        speaker = self.agents[speaker_idx]

        # 2. next speaker sends message
        message = speaker.send()

        # 3. everyone receives message
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        # 4. increment time
        self._step += 1

        return speaker.name, message