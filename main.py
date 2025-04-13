from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain.tools import tool
import uvicorn
from tools import tools
from load_prompts import load_system_prompt
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
     timeout=60.0
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Important: set to False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Initialize LLM and memory
llm = init_chat_model("mistral-large-latest", model_provider="mistralai")
memory = InMemoryChatMessageHistory(session_id="main-session")

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", load_system_prompt('prompts/hura-chatbot-system-prompt.md')),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Create agent and executor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Pydantic models for request and response
class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class QueryResponse(BaseModel):
    response: str
    status: str = "success"

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        config = {"configurable": {"session_id": request.session_id}}
        result = agent_with_chat_history.invoke(
            {"input": request.query},
            config
        )
        
        return QueryResponse(
            response=result['output'],
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)