from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI # For Gemini as agent LLM
from langchain import PromptTemplate
from llm_client import get_llm_response # Fallback for non-agentic LLM if needed
from code_generator import generate_test_code
from test_runner import run_java_test
from rag_system import query_llm_with_rag # Our RAG query function

import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define tools for the agent
tools = [
        Tool(
            name="GenerateTestCode",
            func=generate_test_code,
            description="Generates Java/TestNG/Selenium test code from a natural language description. Input should be a detailed query like 'Write a login test for Chrome'.",
        ),
        Tool(
            name="RunJavaTest",
            func=run_java_test,
            description="Executes a given block of Java test code and returns 'PASS' or 'FAIL'. Input is the Java code as a string.",
        ),
        Tool(
            name="QueryKnowledgeBase",
            func=query_llm_with_rag,
            description="Retrieves contextual information from the automation knowledge base. Input should be a query about concepts, past bugs, or guidelines.",
        )
    ]

# Initialize the LLM for the agent's reasoning
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, google_api_key=GOOGLE_API_KEY)

# Agent prompt template (ReAct style is good for tool use)
# Refined based on LangChain's create_react_agent default.
template = """Answer the following questions as best you can. You have access to the following tools:
    {tools}
    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat 5 times)
    Thought: I now know the final answer
    Final Answer: the final anllmswer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)


# Create the agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True) # handle_parsing_errors to catch bad LLM output

def run_agent_query(query):
    response = agent_executor.invoke({"input": query})
    return response["output"]

# Test
#print(run_agent_query("Generate a Selenium Java TestNG test for a user registering on a page with email, password, confirmPassword, and registerButton IDs."))
#print(run_agent_query("Explain the importance of test data management."))