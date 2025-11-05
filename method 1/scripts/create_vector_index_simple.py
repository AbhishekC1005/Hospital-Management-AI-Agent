"""Create vector search index using pymongo (simplified approach)."""
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import os
from dotenv import load_dotenv
import time

load_dotenv()


def create_vector_search_index():
    """Create Atlas Vector Search index using pymongo."""
    
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DATABASE", "rag_database")
    collection_name = os.getenv("MONGODB_COLLECTION", "documents")
    index_name = os.getenv("MONGODB_VECTOR_INDEX", "vector_index")
    
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(mongo_uri)
    
    try:
        # Test connection
        client.admin.command('ping')
        print("✓ Connected successfully!")
        
        db = client[db_name]
        collection = db[collection_name]
        
        # Check document count
        doc_count = collection.count_documents({})
        print(f"Documents in collection: {doc_count}")
        
        if doc_count == 0:
            print("\n⚠ Warning: No documents found!")
            print("Run: python scripts/add_documents.py")
            return
        
        # Delete existing index if it exists
        print(f"\nChecking for existing index '{index_name}'...")
        try:
            existing_indexes = list(collection.list_search_indexes())
            for idx in existing_indexes:
                if idx.get('name') == index_name:
                    print(f"Deleting existing index '{index_name}'...")
                    collection.drop_search_index(index_name)
                    print("✓ Deleted")
                    time.sleep(2)  # Wait a bit
                    break
        except Exception as e:
            print(f"Note: {e}")
        
        # Create vector search index using SearchIndexModel
        print(f"\nCreating vector search index '{index_name}'...")
        
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "numDimensions": 1536,
                        "similarity": "cosine"
                    }
                ]
            },
            name=index_name,
            type="vectorSearch"
        )
        
        result = collection.create_search_index(model=search_index_model)
        
        print(f"✓ Index creation initiated: {result}")
        print("\n⏳ Waiting for index to become active...")
        print("This usually takes 1-3 minutes...")
        
        # Poll for index status
        max_wait = 180  # 3 minutes
        wait_time = 0
        
        while wait_time < max_wait:
            time.sleep(5)
            wait_time += 5
            
            try:
                indexes = list(collection.list_search_indexes())
                for idx in indexes:
                    if idx.get('name') == index_name:
                        status = idx.get('status', idx.get('queryable'))
                        print(f"  Status: {status} ({wait_time}s)")
                        
                        if status in ['READY', 'ACTIVE', True]:
                            print(f"\n✓ Vector search index is now active!")
                            print(f"\nTest it with: python test_rag.py")
                            return
                        break
            except Exception as e:
                print(f"  Checking... ({wait_time}s)")
        
        print(f"\n⚠ Index created but still building after {max_wait}s")
        print("Check status in Atlas UI or run: python scripts/check_index.py")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you're using MongoDB Atlas (not local MongoDB)")
        print("2. Verify your connection string in .env")
        print("3. Check that your IP is whitelisted in Atlas")
        print("\nIf this fails, create the index manually:")
        print("1. Go to Atlas UI → Browse Collections")
        print(f"2. Select {db_name}.{collection_name}")
        print("3. Click 'Search Indexes' → 'Create Search Index'")
        print("4. Choose 'Atlas Vector Search'")
        print(f"5. Name: {index_name}")
        print("6. Vector field: embedding, 1536 dimensions, cosine similarity")
        
    finally:
        client.close()


if __name__ == "__main__":
    create_vector_search_index()
