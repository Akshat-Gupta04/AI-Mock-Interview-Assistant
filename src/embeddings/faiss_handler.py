import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings

def create_faiss_index(data):
    """Create a FAISS index for dynamic topics."""
    embedding_model = OpenAIEmbeddings()
    embeddings = [embedding_model.embed_query(item) for item in data]
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

def query_faiss_index(index, query):
    """Query a FAISS index with user input."""
    embedding_model = OpenAIEmbeddings()
    query_vector = embedding_model.embed_query(query)
    distances, indices = index.search(np.array([query_vector]), k=5)
    return distances, indices