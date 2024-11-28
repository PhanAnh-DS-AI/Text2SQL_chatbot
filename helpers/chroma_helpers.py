import uuid
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

def load_markdown_file(file_path: str, encoding: str = 'utf-8'):
    """
    Load a markdown file and return its content.
    """
    loader = TextLoader(file_path, encoding=encoding)
    docs = loader.load()
    return docs[0].page_content


def split_markdown_text(faq_text: str, headers_to_split_on=None):
    """
    Split markdown text based on headers and further split into smaller chunks.
    """
    if headers_to_split_on is None:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
    
    # Header splitter
    split_header = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    header_documents = split_header.split_text(faq_text)
    
    # Text splitter
    spliter_text = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    documents = spliter_text.split_documents(header_documents)
    
    return documents

def create_chroma_client(db_path: str):
    """
    Create a Chroma persistent client.
    """
    return chromadb.PersistentClient(path=db_path)

def create_huggingface_embedding(model_name: str, model_kwargs=None, encode_kwargs=None):
    """
    Create HuggingFace embeddings.
    """
    if model_kwargs is None:
        model_kwargs = {'device': 'cpu'}
    if encode_kwargs is None:
        encode_kwargs = {'normalize_embeddings': False}
    
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
def ingest_data_to_chroma(chroma, documents, embedding_function, collection_metadata=None):
    """
    Add formatted documents to Chroma.
    """
    if collection_metadata is None:
        collection_metadata = {}
    
    formatted_documents = [
        Document(
            page_content=doc.page_content, 
            metadata={**doc.metadata, **collection_metadata} 
        )
        for doc in documents
    ]
    
    chroma.add_documents(
        documents=formatted_documents,
        ids=[str(uuid.uuid4()) for _ in range(len(documents))],
        embeddings=embedding_function.embed_documents([doc.page_content for doc in formatted_documents])
    )
    
def setup_chroma(
    file_path: str, 
    db_path: str, 
    model_name: str, 
    collection_name: str, 
    headers_to_split_on=None):

    # Load markdown file
    faq_text = load_markdown_file(file_path)
    
    # Split text into chunks
    documents = split_markdown_text(faq_text, headers_to_split_on=headers_to_split_on)
    
    # Create Chroma client
    chroma_client = create_chroma_client(db_path)
    
    # Create embedding model
    hf = create_huggingface_embedding(model_name)
    
    # Create Chroma collection
    collection_metadata = {"source": file_path}
    chroma = Chroma(
        collection_name=collection_name,
        embedding_function=hf,
        client=chroma_client,
        collection_metadata=collection_metadata
    )
    
    ingest_data_to_chroma(chroma, documents, hf, collection_metadata)
    return chroma

# Setup Chroma with markdown file
file_path = "./Data/swiss_faq.md"
db_path = "./chroma_langchain_db/vector_db"
model_name = "sentence-transformers/all-MiniLM-L12-v1"
collection_name = "swiss_faq_vectordb"

"""chroma_db = setup_chroma(
    file_path=file_path,
    db_path=db_path,
    model_name=model_name,
    collection_name=collection_name
)"""
