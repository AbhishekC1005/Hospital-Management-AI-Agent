"""Script to add documents to MongoDB with embeddings."""
from pymongo import MongoClient
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def add_sample_documents():
    """Add sample documents with embeddings to MongoDB."""
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DATABASE", "rag_db")
    collection_name = os.getenv("MONGODB_COLLECTION", "documents")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    mongo_client = MongoClient(mongo_uri)
    collection = mongo_client[db_name][collection_name]
    openai_client = OpenAI(api_key=openai_api_key)
    
    # Clear existing documents (optional - comment out if you want to keep existing data)
    print("Clearing existing documents...")
    collection.delete_many({})
    
    # Sample documents
    documents = [
        {
            "text": "Python is a high-level programming language known for its simplicity and readability.",
            "metadata": {"category": "programming", "language": "python"},
            "file_md5": "doc1"
        },
        {
            "text": "Machine learning is a subset of AI that enables systems to learn from data.",
            "metadata": {"category": "ai", "topic": "machine_learning"},
            "file_md5": "doc2"
        },
        {
            "text": "MongoDB is a NoSQL database that stores data in flexible, JSON-like documents.",
            "metadata": {"category": "database", "type": "nosql"},
            "file_md5": "doc3"
        },
        {
            "text": "Google ADK is a framework for building AI agents with tools and function calling.",
            "metadata": {"category": "ai", "topic": "agents"},
            "file_md5": "doc4"
        },
        {
            "text": "my name is abhishek",
            "metadata": {"category": "ai", "topic": "embeddings"},
            "file_md5": "doc5"
        }
    ]
    
    # Generate embeddings and insert
    added_count = 0
    for doc in documents:
        try:
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=doc["text"]
            )
            doc["embedding"] = response.data[0].embedding
            
            collection.insert_one(doc)
            print(f"✓ Added: {doc['text'][:60]}...")
            added_count += 1
        except Exception as e:
            print(f"✗ Error adding document: {e}")
    
    print(f"\n✓ Successfully added {added_count}/{len(documents)} documents!")
    mongo_client.close()


if __name__ == "__main__":
    add_sample_documents()
