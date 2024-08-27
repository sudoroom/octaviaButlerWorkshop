from langchain.output_parsers import RegexParser
import tenacity
class BidOutputParser(RegexParser):
    def get_format_instructions(self) -> str:
        return "Your response should be an integer delimited by angled brackets, like this: <int>."


@tenacity.retry(
    stop=tenacity.stop_after_attempt(2),
    wait=tenacity.wait_none(),  # No waiting time between retries
    retry=tenacity.retry_if_exception_type(ValueError),
    before_sleep=lambda retry_state: print(
        f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
    ),
    retry_error_callback=lambda retry_state: 0,
)  # Default value when all retries are exhausted
def ask_for_bid(agent) -> int:
    """
    Ask for agent bid and parses the bid into the correct format.
    """
    bid_string = agent.bid()
    bid = int(bid_parser.parse(bid_string)["bid"])
    return bid

bid_parser = BidOutputParser(
    regex=r"<(\d+)>", output_keys=["bid"], default_output_key="bid"
)


def generate_character_bidding_template(character_header):
    bidding_template = f"""{character_header}

```
{{message_history}}
```

On the scale of 1 to 10, where 1 is least important to the startup pitch and 10 is extremely important and contribute, rank your recent message based on the context. Make sure to be very through in your ranking and only rank stuff that is important higher.

```
{{recent_message}}
```

{bid_parser.get_format_instructions()}
Do nothing else.
    """
    return bidding_template