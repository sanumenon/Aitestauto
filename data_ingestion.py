# This script initializes a ChromaDB client, creates a collection, and adds example documents to the knowledge base.
# It uses the SentenceTransformer model to generate embeddings for the documents.
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer   
# Initialize ChromaDB client
client = chromadb.PersistentClient()
#Get/ create a collection
collection  = client.get_or_create_collection(name="automation_knowledge_base")
# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2') 
# Function to convert large chunk of text as embeddings to the knowledge base
def get_embedding(texts):
    """
    Generate embeddings for a list of texts using the SentenceTransformer model.
    """
    return embedding_model.encode(texts).tolist()

def add_document(doc_id, content, metadata):
    """
    Add a document to the knowledge base with its content and metadata.
    """
    # Generate embeddings for the content
    embedding = get_embedding([content])[0] #Get the content embedding
    # Add the document to the collection
    collection.add(
        ids=[str(doc_id)],
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata]
    )
    
    # collection.delete(ids=['5'])  # Remove the document if it already exists to avoid duplicates
    # collection.delete(ids=['6'])
    # collection.delete(ids=['7'])
    # collection.delete(ids=['8'])
    print(f"Document {doc_id} added to the knowledge base.")  

# Example documents to add to the knowledge base  
add_document(1, "How to write a login test in Selenium Java: Find username field by ID, send keys, find password field by ID, send keys, click login button by ID. Use WebDriverWait for elements.", {"type": "test_case", "framework": "Selenium Java"})
add_document(2, "Bug: Login fails on Firefox due to 'Element not interactable' on username field after page reload on version 100. [WEB-456]", {"type": "bug_report", "browser": "Firefox"})
add_document(3, "Coding Standard: All locators in Page Objects must use By.id or By.cssSelector. Avoid absolute XPaths.", {"type": "guideline", "category": "coding_style"})
add_document(4, "What is Page Object Model: Design pattern to encapsulate UI elements and interactions.", {"type": "concept"})
# add_document(5, "Page Factory is a part of the Selenium library that simplifies the initialization of web elements. It uses @FindBy annotations to locate elements and helps implement the Page Object Model (POM) in a more readable and maintainable way." , {"type": "concept"})
# add_document(6,"What is TestNG ? : TestNG stands for Test Next Generation. It is a testing framework in Java designed to simplify a broad range of testing needs, from unit tests to integration and UI tests. It is especially popular with Selenium users."
# "TestNG provides powerful features like annotations, grouping, data-driven testing, and parallel execution. It improves test structure, readability, and CI/CD integration", {"type": "concept", "framework": "TestNG"})
# add_document(7,"TestNG uses annotations to control test flow:" "`@Test`: Marks a test method."
# " `@BeforeClass` / `@AfterClass`: Run once per class."
# " `@BeforeMethod` / `@AfterMethod`: Run before/after each test method."
# " `@DataProvider`: Feeds multiple sets of data to a test."
# " `@Parameters`: Injects values via XML."
# " `@BeforeSuite`, `@AfterSuite`: Runs before/after the test suite.", {"type": "concept", "framework": "TestNG"})
# add_document(8,"TestNG code eamples : @DataProvider(name = 'loginData')"
# " public Object[][] getData() {"
# "    return new Object[][] { {'user1', 'pass1'}, {'user2', 'pass2'} };"
# "}"
# "@Test(dataProvider = 'loginData')"
# "public void testLogin(String username, String password) {"
# "// use parameters in test}",{"type": "code_example", "language": "Java"})

print(f"Total documents in knowledge base: {collection.count()}")
print(f"Konwledge base preparation completed. You can now query the knowledge base for relevant information.")