from slack_sdk import WebClient
from config import SLACK_TOKEN

def send_message_to_slack(message: str):
    """
    Send message on slack
    """
    client = WebClient(token=SLACK_TOKEN)
    client.chat_postMessage(
        channel="pdf-querier", 
        text=message, 
        username="Answer Assistant"
    )
