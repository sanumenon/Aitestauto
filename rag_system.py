import chromadb
from sentence_transformers import SentenceTransformer
from llm_client import get_llm_response # Import the LLM client function

# Initialize ChromaDB client (must match path in data_ingestion.py)
client = chromadb.PersistentClient(path="./chroma_db")
# Get or create a collection
collection = client.get_or_create_collection(name="automation_knowledge_base")
# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')   

def retrieve_context(query_text, domain_filter=None, n_results=3):
    """
    Retrieve relevant context from the knowledge base for a given query,
    optionally filtered by domain.
    
    Args:
        query_text (str): The input query text to search for relevant documents.
        domain_filter (str, optional): The domain to filter documents by.
                                       If None, general documents are preferred.
        n_results (int): The number of top results to return.
        
    Returns:
        list: A list of relevant documents from the knowledge base.
    """
    query_embedding = embedding_model.encode([query_text]).tolist()[0]
    
    # Build the where clause for filtering
    where_clause = {}
    if domain_filter:
        # Prioritize domain-specific documents, fallback to general if not enough found
        # This is a strategy: query for exact domain, then augment with general.
        # Or query with OR condition
        where_clause = {
            "$or": [
                {"domain": domain_filter},
                {"domain": "general"} # Always include general documents
            ]
        }
        # For strict domain only: where_clause = {"domain": domain_filter}


    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_clause, # Apply the filter here
        include=["documents", "metadatas", "distances"] # Include distances for debugging
    )
    
    context = []
    # Filter and sort results to prioritize exact domain matches if needed
    # (ChromaDB's query 'where' might not guarantee exact domain first, so manual sort)
    relevant_docs = []
    if results['ids'] and results['ids'][0]:
        for i in range(len(results['ids'][0])):
            doc_id = results['ids'][0][i]
            doc_content = results['documents'][0][i]
            doc_meta = results['metadatas'][0][i]
            doc_distance = results['distances'][0][i]
            relevant_docs.append({
                "id": doc_id,
                "content": doc_content,
                "meta": doc_meta,
                "distance": doc_distance
            })
    
    # Sort to prioritize exact domain match, then by distance
    def sort_key(doc_item):
        is_exact_match = (doc_item['meta'].get('domain') == domain_filter)
        # Give exact matches a higher 'priority' by making their sort key smaller
        # (distance is smaller for more similar, so smaller for exact match means better)
        # We negate distance because ChromaDB gives lower distance for higher similarity
        priority_score = (0 if is_exact_match else 1) * 1000 + doc_item['distance']
        return priority_score

    if domain_filter:
        relevant_docs.sort(key=sort_key)
    else:
        # If no domain filter, sort only by distance
        relevant_docs.sort(key=lambda x: x['distance'])


    for doc_item in relevant_docs[:n_results]: # Take top N after sorting
        context.append(
            f"Document ID: {doc_item['id']}, Type: {doc_item['meta'].get('type')}, Domain: {doc_item['meta'].get('domain', 'N/A')}\nContent: {doc_item['content']}"
        )
    return "\n\n".join(context)


def query_llm_with_rag(user_query, env_domain=None):
    """
    Query the LLM with a user query and relevant context from the knowledge base,
    filtered by environment domain.
    
    Args:
        user_query (str): The user's query to be answered by the LLM.
        env_domain (str, optional): The domain of the current environment.
                                     e.g., 'my.stg.charitableimpact.com'
                                     If None, it defaults to 'my.charitableimpact.com' (production)
                                     and includes general documents.
        
    Returns:
        str: The response from the LLM.
    """
    # Determine the domain filter based on the environment
    actual_domain_filter = None
    if env_domain:
        actual_domain_filter = env_domain
    else:
        # Default to production domain if no domain is explicitly provided
        actual_domain_filter = "my.charitableimpact.com"
        
    print(f"Retrieving context for domain: {actual_domain_filter}")
    context = retrieve_context(user_query, domain_filter=actual_domain_filter)
    
    prompt = f"""You are an expert Test Automation Engineer. Use the following context to answer the user's query.
        If the context does not contain enough information, state that.

        Context:
        {context}

        User Query: {user_query}
        """
    
    return get_llm_response(prompt)

# Example usage with environment domains
#if __name__ == "__main__":
    # print("\n--- Query for STAGE environment ---")
    # user_query_stage = "How to write a login test for payment flow? Mention any known bugs."
    # response_stage = query_llm_with_rag(user_query_stage, env_domain="my.stg.charitableimpact.com")
    # print(f"LLM Response (STAGE): {response_stage}")

    # print("\n--- Query for QA environment ---")
    # user_query_qa = "I'm having trouble with the Google sign-in button. Any bugs?"
    # response_qa = query_llm_with_rag(user_query_qa, env_domain="my.qa.charitableimpact.com")
    # print(f"LLM Response (QA): {response_qa}")

    # print("\n--- Query for PROD environment (default) ---")
    # user_query_prod = "What's the status of payment processing performance?"
    # response_prod = query_llm_with_rag(user_query_prod) # Uses default production domain
    # print(f"LLM Response (PROD): {response_prod}")

    # print("\n--- General Query (no specific domain filter) ---")
    # user_query_general = "Explain Page Object Model."
    # response_general = query_llm_with_rag(user_query_general, env_domain="my.charitableimpact.com") # Will still look for general if domain not found
    # print(f"LLM Response (General): {response_general}")
#print(f"Knowledge base and LLM query system initialized successfully.")
print("Knowledge base and LLM query system initialized successfully.")
print("You can now use the query_llm_with_rag function to get responses")