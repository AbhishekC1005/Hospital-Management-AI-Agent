"""RAG function as CrewAI tool."""
from crewai.tools import tool
from agent.tools.rag_tool import rag_tool_instance
import os


@tool("Retrieve Knowledge")
def rag_function_tool(query: str) -> str:
    """
    Retrieve relevant documents from the knowledge base using vector search.
    
    Args:
        query: The search query text to find relevant documents
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        query_embedding = response.data[0].embedding
        
        results = rag_tool_instance.search(query_embedding, limit=5)
        
        if not results:
            return "No relevant documents found in the knowledge base."
        
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
