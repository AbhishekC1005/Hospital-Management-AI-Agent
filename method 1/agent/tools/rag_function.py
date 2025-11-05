"""RAG tool for ADK agent."""
from agent.tools.rag_tool import RAGTool
import os


# Initialize RAG tool
rag_tool = RAGTool()


def retrieve_documents(query: str) -> str:
    """
    Retrieve relevant documents from the knowledge base using vector search.
    
    Args:
        query: The search query text to find relevant documents
        
    Returns:
        str: Retrieved documents formatted as text with relevance scores
    """
    try:
        # Generate embedding for the query using OpenAI
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Get embedding for query
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        query_embedding = response.data[0].embedding
        
        # Search MongoDB (default limit of 5)
        results = rag_tool.search(query_embedding, limit=5)
        
        if not results:
            return "No relevant documents found in the knowledge base."
        
        # Format results
        formatted_results = []
        for i, doc in enumerate(results, 1):
            text = doc.get("text", "")
            score = doc.get("score", 0)
            metadata = doc.get("metadata", {})
            
            formatted_results.append(
                f"Document {i} (Relevance: {score:.4f}):\n{text}\n"
                f"Metadata: {metadata}\n"
            )
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"Error retrieving documents: {str(e)}"


# Export the function as a tool
rag_function = retrieve_documents
