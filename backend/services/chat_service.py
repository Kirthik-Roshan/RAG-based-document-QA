from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from services.retrieval_service import (
    retrieve_documents
)

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful assistant.

Answer ONLY using the context.

If answer cannot be found,
say:

I don't know based on the uploaded documents.

Context:
{context}

Question:
{question}
"""
)

def ask_question(question: str):

    docs = retrieve_documents(
        question
    )

    if not docs:

        return {
            "answer":
            "No documents uploaded.",
            "sources": []
        }

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(
        messages
    )

    sources = []

    for doc in docs:

        sources.append(
            {
                "file":
                doc.metadata.get(
                    "source_file",
                    "Unknown"
                ),

                "page":
                doc.metadata.get(
                    "page",
                    "Unknown"
                )
            }
        )

    return {
        "answer":
        response.content,

        "sources":
        sources
    }