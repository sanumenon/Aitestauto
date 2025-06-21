import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from llm_client import get_llm_response # Import the LLM client function - A python script that is already created to get responses from the LLM.
# Initialize ChromaDB client
client = chromadb.PersistentClient()
# Get or create a collection
collection = client.get_or_create_collection(name="automation_knowledge_base")
# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')   
# Function to convert large chunk of text as embeddings to the knowledge base
def retrive_context(query_text, n_results=3):
    """
    Retrieve relevant context from the knowledge base for a given query.
    
    Args:
        query_text (str): The input query text to search for relevant documents.
        n_results (int): The number of top results to return.
        
    Returns:
        list: A list of relevant documents from the knowledge base.
    """
    # Generate embeddings for the query
    query_embedding = embedding_model.encode([query_text]).tolist()[0]
    
    # Query the collection for similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas"]  # Include documents and metadata in the results
    )
    context=[]
    for i in range(len(results['documents'][0])):
        doc= results['documents'][0][i]
        meta= results['metadatas'][0][i]
        context.append(
            f"Document ID: {results['ids'][0][i]}, Type: {meta.get('type')}\nContent: {doc}"
        )
    return "\n\n".join(context)

def query_llm_with_rag(user_query):
    """
    Query the LLM with a user query and relevant context from the knowledge base.
    
    Args:
        user_query (str): The user's query to be answered by the LLM.
        
    Returns:
        str: The response from the LLM.
    """
    # Retrieve relevant context from the knowledge base
    context = retrive_context(user_query)
    
    # Prepare the prompt for the LLM
    prompt = f"""You are an expert Test Automation Engineer. Use the following context to answer the user's query.
        If the context does not contain enough information, state that.

        Context:
        {context}

        User Query: {user_query}
        """
    
    # Get response from the LLM
    return get_llm_response(prompt)
 
# Example usage
if __name__ == "__main__":
   # user_query = "How to write a login test in Selenium Java using Page Object Model with testng in the url https://www.facebook.com/?"
    #user_query = "Explain page factory in selenium java with an example ?"

   # user_query = "Explain about testng framewok with an example in an experts view point and summarise in 5 lines?"
   # user_query = "summarise page factory in selenium java using pom and testng in 5 lines for an expert programmer?"
   # user_query ="Explain about selenium wait in an expert's view point and summarise in 5 lines?"
    user_query = "how to write a dynamic xpath in selenium java with an example?"
    response = query_llm_with_rag(user_query)
    print(f"LLM Response: {response}")
    # You can also test with other queries to see how the RAG system performs.
    # For example:
    # user_query = "What is Page Object Model?"
    # response = query_llm_with_rag(user_query)
    # print(f"LLM Response: {response}")    