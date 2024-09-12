from vector_store import DocumentVectorStore
from llm import OpenAI
from prompts import get_system_prompt, get_user_prompt
from config import logger
from slack import send_message_to_slack
import json

def main():
    # Control point of the system

    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ]

    file_name = "handbook.pdf"

    document_vector_store = DocumentVectorStore()
    document_vector_store.embed_document(file_name)

    logger.info("Document embedded successfully")

    final_information_json = {}

    for question in questions:
        try:
            answer = get_answer(question, document_vector_store)
        except Exception as exc:
            logger.exception(f"Failed to generate answer : {str(exc)}")
            answer = "failed to get answer"

        final_information_json[question] = answer

    logger.info("answer generated...")

    logger.debug(final_information_json)

    send_message_to_slack(json.dumps(final_information_json))

    logger.info("msg sent to slack successfully")


def get_answer(question: str, document_vector_store: DocumentVectorStore) -> str:
    """
    Get the answer for a particular question
    """

    docs = document_vector_store.get_nearest_documents(question)

    llm_instance = OpenAI(document_vector_store)

    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(question, docs)

    prompts = [
        system_prompt,
        user_prompt
    ]

    answer = llm_instance.execute_prompts(prompts)

    return answer


# Execution
main()