import re
import tenacity

class BidOutputParser:
    def __init__(self):
        self.regex = r"<(\d+)>"
        self.output_keys = ["bid"]
        self.default_output_key = "bid"

    def parse(self, text: str) -> dict:
        match = re.search(self.regex, text)
        if match:
            return {self.default_output_key: int(match.group(1))}
        raise ValueError(f"Could not parse bid from: {text}")

    def get_format_instructions(self) -> str:
        return "Your response should be an integer delimited by angled brackets, like this: <int>."

bid_parser = BidOutputParser()

@tenacity.retry(
    stop=tenacity.stop_after_attempt(2),
    wait=tenacity.wait_none(),
    retry=tenacity.retry_if_exception_type(ValueError),
    before_sleep=lambda retry_state: print(f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."),
    retry_error_callback=lambda retry_state: 0,
)
def ask_for_bid(agent) -> int:
    bid_string = agent.bid()
    bid = int(bid_parser.parse(bid_string)["bid"])
    return bid