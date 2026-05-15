from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# --------------------------------------------------
# 1. Load environment variables from .env
# --------------------------------------------------
load_dotenv()


# --------------------------------------------------
# 2. Configuration
# --------------------------------------------------
PDF_PATH = "document.pdf"              # Replace with your PDF filename
CHROMA_DIR = "./chroma_db"             # Folder where vectors are stored
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4.1-mini"


# --------------------------------------------------
# 3. Load PDF
# --------------------------------------------------
print("Loading PDF...")
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()
print(f"Loaded {len(documents)} pages")


# --------------------------------------------------
# 4. Split into chunks
# --------------------------------------------------
print("Splitting document into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")


# --------------------------------------------------
# 5. Create embeddings model
# --------------------------------------------------
print("Initializing embeddings model...")
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)


# --------------------------------------------------
# 6. Create and persist Chroma vector store
# --------------------------------------------------
print("Creating vector store...")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DIR,
)

# Save to disk
vectorstore.persist()
print(f"Vector store saved to {CHROMA_DIR}")


# --------------------------------------------------
# 7. Create retriever
# --------------------------------------------------
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)


# --------------------------------------------------
# 8. Initialize LLM
# --------------------------------------------------
print("Initializing LLM...")
llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0,
)


# --------------------------------------------------
# 9. Prompt template
# --------------------------------------------------
prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.
Answer the question using only the provided context.
If the answer is not present in the context, say:
"I don't know based on the provided document."

Context:
{context}

Question:
{question}
"""
)


# --------------------------------------------------
# 10. Question-answer loop
# --------------------------------------------------
print("\nRAG system is ready.")
print("Type 'exit' to quit.\n")

while True:
    question = input("Ask a question: ").strip()

    if question.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    if not question:
        continue

    # Retrieve relevant chunks
    retrieved_docs = retriever.invoke(question)

    # Combine retrieved text into one context string
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Build prompt
    messages = prompt.format_messages(
        context=context,
        question=question,
    )

    # Generate answer
    response = llm.invoke(messages)

    # Print answer
    print("\nAnswer:")
    print(response.content)

    # Print source pages
    print("\nRetrieved Sources:")
    for i, doc in enumerate(retrieved_docs, start=1):
        page = doc.metadata.get("page", "Unknown")
        source = doc.metadata.get("source", PDF_PATH)
        print(f"{i}. {source} | Page {page}")

    print("\n" + "-" * 60 + "\n")