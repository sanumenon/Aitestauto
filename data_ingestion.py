# This script initializes a ChromaDB client, creates a collection, and adds example documents to the knowledge base.
# It uses the SentenceTransformer model to generate embeddings for the documents.
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer   

# Initialize ChromaDB client
# It's good practice to pass a path for persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Get/ create a collection
collection  = client.get_or_create_collection(name="automation_knowledge_base")

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2') 

# Function to convert large chunk of text as embeddings to the knowledge base
def get_embedding(texts):
    """
    Generate embeddings for a list of texts using the SentenceTransformer model.
    """
    return embedding_model.encode(texts).tolist()

def add_document(doc_id, content, metadata=None): # Make metadata optional if not always provided
    """
    Add a document to the knowledge base with its content and metadata.
    Adds a 'domain' field to metadata if specified.
    """
    if metadata is None:
        metadata = {}
    
    # Generate embeddings for the content
    embedding = get_embedding([content])[0] 
    
    # Add the document to the collection
    collection.add(
        ids=[str(doc_id)],
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata]
    )
    print(f"Document {doc_id} added to the knowledge base with metadata: {metadata}.")  

# Example documents to add to the knowledge base
# Now, include a 'domain' field in the metadata for domain-specific documents
# For general documents, you might omit 'domain' or set it to 'general'
# You would ingest more of your specific project documentation here with correct domains

# General documents (applicable to all environments, or no specific domain)
add_document(1, "How to write a login test in Selenium Java: Find username field by ID, send keys, find password field by ID, send keys, click login button by ID. Use WebDriverWait for elements.", {"type": "test_case", "framework": "Selenium Java", "domain": "general"})
add_document(3, "Coding Standard: All locators in Page Objects must use By.id or By.cssSelector. Avoid absolute XPaths.", {"type": "guideline", "category": "coding_style", "domain": "general"})
add_document(4, "What is Page Object Model: Design pattern to encapsulate UI elements and interactions.", {"type": "concept", "domain": "general"})

# Stage environment specific document
add_document(5, "Bug: STAGE environment login issue. Users redirected to 'invalid_session' page after 3 failed attempts. [WEB-457]", {"type": "bug_report", "environment": "STAGE", "domain": "my.stg.charitableimpact.com"})
add_document(6, "Feature: STAGE environment new dashboard layout for beta users. Test element ID 'betaDashboardWelcome'.", {"type": "feature_doc", "environment": "STAGE", "domain": "my.stg.charitableimpact.com"})

# QA environment specific document
add_document(7, "Bug: QA environment 'Sign in with Google' button sometimes not clickable. Investigate JavaScript errors. [WEB-458]", {"type": "bug_report", "environment": "QA", "domain": "my.qa.charitableimpact.com"})

# Production environment specific document
add_document(8, "Alert: PROD environment critical user flow: payment processing response times exceeding 500ms under load. Monitor 'paymentGatewayResponse' metric. [PROD-CRITICAL-1]", {"type": "alert", "environment": "PROD", "domain": "my.charitableimpact.com"})

# Example of a bug report that might be general
add_document(2, "Bug: Login fails on Firefox due to 'Element not interactable' on username field after page reload on version 100. [WEB-456]", {"type": "bug_report", "browser": "Firefox", "domain": "general"})


# Clean up existing collection before adding documents (optional, for fresh start)
# collection.delete(ids=['1', '2', '3', '4', '5', '6', '7', '8'])

print(f"Total documents in knowledge base: {collection.count()}")
print("Knowledge base preparation completed. You can now query the knowledge base for relevant information.")