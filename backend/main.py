from fastapi import FastAPI

from backend.config import validate_environment
from backend.models.schemas import SupportRequest
from sse_starlette.sse import EventSourceResponse
from backend.services.support_service import (
    run_support_workflow,
    run_support_workflow_stream
)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AutoGen Customer Support API",
    description="Backend API for multi-agent customer support system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AutoGen Customer Support API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/config-check")
def config_check():
    validate_environment()

    return {
        "status": "success",
        "message": "Required API keys are configured"
    }

@app.post("/support")
async def support(request: SupportRequest):
    result = await run_support_workflow(request.query)

    return result

@app.post("/support/stream")
async def support_stream(request: SupportRequest):

    async def event_generator():
        async for event in run_support_workflow_stream(request.query):
            yield event

    return EventSourceResponse(event_generator())