import os
import logging

logger = logging.getLogger(__name__)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
SLACK_TOKEN = os.getenv("SLACK_TOKEN", None)

if not OPENAI_API_KEY:
    logger.error("OPEN_API_KEY not found")
    raise Exception(
        "OPENAI_API_KEY Not set"
    )

if not SLACK_TOKEN:
    logger.error("SLACK_TOKEN not found")
    raise Exception(
        "SLACK_TOKEN not set"
    )

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


GPT_4o_MINI_MAX_TOKEN_LIMIT = 1600
OPENAI_MODEL_NAME = "gpt-4o-mini"