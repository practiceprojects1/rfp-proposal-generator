"""
FastAPI REST API for RFP Proposal Generator with AWS Bedrock support.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend, CompositeBackend, StateBackend
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

# Import custom tools
from tools.rfp_search import search_sam_gov, search_grants_gov, get_rfp_details
from tools.rfp_analysis import analyze_rfp_relevance, check_processed_rfps, mark_rfp_processed
from tools.proposal_generator import generate_proposal


# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = "default"
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    thread_id: str


class HealthResponse(BaseModel):
    status: str
    model: str
    backend: str


# Initialize FastAPI app
app = FastAPI(
    title="RFP Proposal Generator API",
    description="AI-powered federal RFP search and proposal generation using Deep Agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global agent instance
agent = None
checkpointer = None
store = None


def create_backend(runtime):
    """Create composite backend for hybrid storage."""
    return CompositeBackend(
        default=StateBackend(runtime),
        routes={
            "/proposals/": FilesystemBackend(
                root_dir=os.path.join(os.path.dirname(__file__), "proposals"),
                virtual_mode=True
            )
        }
    )


def get_system_prompt():
    """Get system prompt with Bedrock-specific instructions."""
    return """You are an expert federal contracting specialist and proposal writer for Cognition, Inc.

Your mission is to:
1. Search for federal RFPs that are relevant to Devin AI's capabilities
2. Analyze RFPs to determine fit and relevance
3. Generate tailored proposals highlighting Devin AI's strengths
4. Track which RFPs have been processed to avoid duplicates

Devin AI Key Capabilities:
- Autonomous software engineering and code generation
- Multi-step task planning and execution
- Real-time debugging and error resolution
- Support for multiple programming languages
- AI/ML development expertise
- DevOps and CI/CD automation
- Security and compliance features

When working:
1. Use search_sam_gov or search_grants_gov to find opportunities
2. Use get_rfp_details to fetch full RFP information
3. Use check_processed_rfps to avoid duplicate work
4. Use analyze_rfp_relevance to determine if an RFP is a good fit
5. Use generate_proposal to create tailored proposals
6. Use mark_rfp_processed to track completed work
7. Use write_todos to plan multi-step tasks
8. Use filesystem tools to save and manage proposals

Always be thorough and professional in your analysis and proposal generation.
Provide concise, actionable responses.
"""


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup."""
    global agent, checkpointer, store

    print("Initializing RFP Proposal Generator Agent...")

    # Determine which model to use
    model = os.getenv("MODEL", "anthropic:claude-sonnet-4-5")

    # If using AWS Bedrock, use the Bedrock model string
    if os.getenv("USE_BEDROCK", "false").lower() == "true":
        model = "bedrock:anthropic.claude-3-sonnet-20240229-v1:0"
        print("Using AWS Bedrock for model inference")

    # Create checkpointer for conversation persistence
    checkpointer = MemorySaver()

    # Create store for long-term memory
    store = InMemoryStore()

    # Create the deep agent
    agent = create_deep_agent(
        name="rfp-proposal-agent",
        model=model,
        tools=[
            search_sam_gov,
            search_grants_gov,
            get_rfp_details,
            analyze_rfp_relevance,
            check_processed_rfps,
            mark_rfp_processed,
            generate_proposal
        ],
        system_prompt=get_system_prompt(),
        backend=create_backend,
        checkpointer=checkpointer,
        store=store,
        skills=["./skills/"]
    )

    print("Agent initialized successfully!")


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    model = os.getenv("MODEL", "anthropic:claude-sonnet-4-5")
    if os.getenv("USE_BEDROCK", "false").lower() == "true":
        model = "AWS Bedrock (Claude 3 Sonnet)"

    return HealthResponse(
        status="healthy",
        model=model,
        backend="Deep Agents"
    )


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "agent": agent is not None,
        "checkpointer": checkpointer is not None,
        "store": store is not None
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the RFP Proposal Generator agent."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        config = {"configurable": {"thread_id": request.thread_id}}

        result = agent.invoke({
            "messages": [{"role": "user", "content": request.message}]
        }, config=config)

        # Extract the last message content
        response_text = result["messages"][-1].content

        return ChatResponse(
            response=response_text,
            thread_id=request.thread_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    async def generate():
        try:
            config = {"configurable": {"thread_id": request.thread_id}}

            for chunk in agent.stream({
                "messages": [{"role": "user", "content": request.message}]
            }, config=config):
                if "messages" in chunk:
                    for message in chunk["messages"]:
                        if hasattr(message, 'content'):
                            yield f"data: {message.content}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    from fastapi.responses import StreamingResponse
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/rfp/search")
async def search_rfps(keywords: str, days_back: int = 30, limit: int = 10):
    """Search for RFPs directly."""
    try:
        result = search_sam_gov.invoke({
            "keywords": keywords,
            "days_back": days_back,
            "limit": limit
        })
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rfp/analyze")
async def analyze_rfp(rfp_details: dict):
    """Analyze an RFP for relevance."""
    try:
        import json
        result = analyze_rfp_relevance.invoke({
            "rfp_details": json.dumps(rfp_details)
        })
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/proposal/generate")
async def generate_proposal_endpoint(rfp_details: dict):
    """Generate a proposal for an RFP."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        import json
        # Create a mock runtime for the tool
        from langchain.tools import ToolRuntime

        class MockRuntime:
            def invoke_tool(self, name, args):
                # This would need proper implementation
                pass

        runtime = MockRuntime()
        result = generate_proposal.invoke({
            "rfp_details": json.dumps(rfp_details),
            "runtime": runtime
        })
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)