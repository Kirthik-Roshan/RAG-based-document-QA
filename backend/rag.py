from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

CHROMA_DIR = "./chroma_db"

# ----------------------------------
# Embeddings Model
# ----------------------------------

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# ----------------------------------
# LLM
# ----------------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

# ----------------------------------
# Prompt
# ----------------------------------

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful RAG assistant.

Answer ONLY using the provided context.

If the answer is not found in the context, reply:

"I don't know based on the uploaded documents."

Context:
{context}

Question:
{question}
"""
)

# ----------------------------------
# PDF Ingestion
# ----------------------------------

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

        chunk.metadata["source_file"] = filename

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    vectorstore.add_documents(chunks)

    return {
        "success": True,
        "file": filename,
        "chunks_added": len(chunks)
    }

# ----------------------------------
# Question Answering
# ----------------------------------

def ask_question(question: str):

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    retrieved_docs = retriever.invoke(
        question
    )

    if not retrieved_docs:

        return {
            "answer": "No documents available.",
            "sources": []
        }

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)

    sources = []

    for doc in retrieved_docs:

        sources.append(
            {
                "file": doc.metadata.get(
                    "source_file",
                    "Unknown"
                ),
                "page": doc.metadata.get(
                    "page",
                    "Unknown"
                )
            }
        )

    return {
        "answer": response.content,
        "sources": sources
    }