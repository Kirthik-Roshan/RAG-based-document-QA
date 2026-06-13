from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.retrieval_service import (
    get_vectorstore
)

def process_pdf(pdf_path: str):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        documents
    )

    filename = pdf_path.split("/")[-1]

    for chunk in chunks:
        chunk.metadata["source_file"] = (
            filename
        )

    vectorstore = get_vectorstore()

    vectorstore.add_documents(
        chunks
    )

    return {
        "success": True,
        "file": filename,
        "chunks_added": len(chunks)
    }