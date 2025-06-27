from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import MessagesPlaceholder
from langchain import PromptTemplate
from llm_client import get_llm_response
from code_generator import generate_test_code
from test_runner import run_java_test
from rag_system import query_llm_with_rag

import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define tools for the agent
tools = [
    Tool(
        name="GenerateTestCode",
        func=generate_test_code,
        description="Generates Java/TestNG/Selenium test code from a natural language description. Accepts 'query' and optional 'env_domain' for context. Example: 'GenerateTestCode(query=\"Write a login test for Chrome\", env_domain=\"my.stg.charitableimpact.com\")'.",
    ),
    Tool(
        name="RunJavaTest",
        func=run_java_test,
        description="Executes a given block of Java test code and returns 'PASS' or 'FAIL'. Input is the Java code as a string.",
    ),
    Tool(
        name="QueryKnowledgeBase",
        func=query_llm_with_rag, # This already accepts env_domain
        description="Retrieves contextual information from the automation knowledge base. Accepts 'user_query' and optional 'env_domain' for environment-specific context. Example: 'QueryKnowledgeBase(user_query=\"Known login bugs\", env_domain=\"my.qa.charitableimpact.com\")'.",
    )
]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, google_api_key=GOOGLE_API_KEY)

# Agent prompt template (ReAct style)
template = """You are an AI-Powered Test Automation Assistant.
Answer the following questions as best you can. You have access to the following tools:
{tools}

By default, if no specific environment (QA, STAGE, PROD) is mentioned in the user's query, assume the environment is 'PROD' and use its corresponding domain 'my.charitableimpact.com' for any tools that require a domain. If an environment is mentioned, use its specific domain.

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat 3 times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

{chat_history}
Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Modify run_agent_query to accept chat_history and environment
def run_agent_query(query, environment="PROD", chat_history=None):
    from langchain_core.messages import HumanMessage, AIMessage

    formatted_history = []
    if chat_history:
        for msg in chat_history[:-1]:
            if msg["role"] == "user":
                formatted_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_history.append(AIMessage(content=msg["content"]))

    # Map environment to domain for RAG system and tool calls
    env_domain_map = {
        "QA": "my.qa.charitableimpact.com",
        "STAGE": "my.stg.charitableimpact.com",
        "PROD": "my.charitableimpact.com"
    }
    actual_domain = env_domain_map.get(environment.upper(), "my.charitableimpact.com")

    # Pass environment and domain directly as part of the invocation arguments
    # The agent's prompt needs to be updated to make the LLM use these in Action Input.
    response = agent_executor.invoke({"input": query, "chat_history": formatted_history, "environment": environment, "env_domain": actual_domain})

    return response["output"]

print("Agent orchestrator initialized successfully.")