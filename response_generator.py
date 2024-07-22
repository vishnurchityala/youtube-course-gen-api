# Importing all modules required.
import os

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_pinecone.vectorstores import PineconeVectorStore


# Setting the logging to ERROR only mode
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GRPC_LOG_SEVERITY_LEVEL'] = 'ERROR'


def get_response(namespace, prompt,embeddings,index,gemini_api_key):
    # VectorStore for retriever
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings, namespace=namespace, text_key="text_chunk")
    # Creating a chatbot which is particular answering only about a namespace in an Index
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=gemini_api_key),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
    )
    response = qa_chain.invoke(prompt)
    return response["result"]
