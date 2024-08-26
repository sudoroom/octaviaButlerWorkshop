from agents.dialogue_agent import DialogueAgent

class BiddingDialogueAgent(DialogueAgent):
    def __init__(self, name: str, system_message: str, bidding_template: str) -> None:
        super().__init__(name, system_message)
        self.bidding_template = bidding_template

    def bid(self) -> str:
        prompt = self.bidding_template.format(
            message_history="\n".join(self.message_history),
            recent_message=self.message_history[-1],
        )
        bid_string = self.ollama_call(prompt)
        return bid_string