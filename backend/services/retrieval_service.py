from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_DIR = "./chroma_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

def retrieve_documents(
    question: str,
    k: int = 5
):
    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever.invoke(question)