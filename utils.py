from PyPDF2 import PdfReader
from config import GPT_4o_MINI_MAX_TOKEN_LIMIT
from langchain.text_splitter import CharacterTextSplitter

def get_raw_text_from_pdf_file(file_name: str)-> str:
    """
    Get the raw text/content from pdf file
    """

    pdf_reader = PdfReader(file_name)

    raw_text = ""
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    return raw_text

def get_chunked_text_from_raw_text(raw_text: str) -> list[str]:
    """
    Get raw text chunks
    """

    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = int(GPT_4o_MINI_MAX_TOKEN_LIMIT/2),
        chunk_overlap  = 50,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)

    return texts