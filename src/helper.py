from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from langchain_huggingface import HuggingFaceEmbeddings


# extract text from pdf files 
def load_pdf_files(data):
    loader=DirectoryLoader(data,
                            glob="*.pdf",
                              loader_cls=PyPDFLoader
                              )
    docs = loader.load()
    return docs


""" 
This function takes a list of Document objects and returns a new list of Document objects (cleaned data )
here is the source and page content only
"""
def filter_docs(docs : List[Document]) -> List[Document]:
    minimal_docs : List[Document] = []
    for doc in docs:
        src=doc.metadata.get("source")
        minimal_docs.append(Document(
            page_content=doc.page_content,
            metadata={"source": src}
            )
        )
    return minimal_docs


#split the docs into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    text_chunk = text_splitter.split_documents(minimal_docs)
    return text_chunk


"""Download and return the huggingface embeddings model"""
def download_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name
                                      
                                       )
    return embeddings

