from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from utils import get_raw_text_from_pdf_file, get_chunked_text_from_raw_text
from config import logger

class DocumentVectorStore:
    """
    Vector store for Document Embeddings and Retrieval
    """

    def __init__(self) -> None:
        self.vector_store = None

    def embed_document(self, file_name: str) -> None:
        """
        Embed the content of document

        1. Load the File
        2. Get the raw text out of it
        3. Divide them based on the chunk based on model max token limit
        4. Create embeddings
        """

        raw_text = get_raw_text_from_pdf_file(file_name=file_name)

        chunked_texts = get_chunked_text_from_raw_text(raw_text=raw_text)

        embeddings = OpenAIEmbeddings()
        db = Chroma.from_texts(chunked_texts, embeddings)
        self.vector_store = db
        logger.info("Document embedded successfully")

    def get_nearest_documents(self, question: str)-> list[str]:
        """
        Get the nearest documents based on the question text
        """

        # Fetching top 2 results
        raw_docs = self.vector_store.similarity_search(question)

        docs = []
        for doc in raw_docs:
            docs.append(doc.page_content)
        return docs             








