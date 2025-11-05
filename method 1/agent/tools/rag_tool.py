"""RAG tool for retrieving embeddings from MongoDB vector search."""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Reload environment variables to get latest values
load_dotenv(override=True)


class RAGTool:
    """Tool for retrieving relevant documents using MongoDB vector search."""
    
    def __init__(self):
        # Load fresh environment variables
        self.mongo_uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DATABASE", "rag_database")
        self.collection_name = os.getenv("MONGODB_COLLECTION", "documents")
        self.index_name = os.getenv("MONGODB_VECTOR_INDEX", "vector_index")
        self.client = None
        self.collection = None
        
    def connect(self):
        """Connect to MongoDB."""
        if not self.client:
            self.client = MongoClient(self.mongo_uri)
            self.collection = self.client[self.db_name][self.collection_name]
    
    def search(self, query_embedding: list[float], limit: int = 5) -> list[dict]:
        """
        Search for similar documents using vector search.
        
        Args:
            query_embedding: The embedding vector for the query
            limit: Number of results to return
            
        Returns:
            list[dict]: List of matching documents with scores
        """
        self.connect()
        
        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.index_name,
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": limit * 10,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        return results
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self.client = None
