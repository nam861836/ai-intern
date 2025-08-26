import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from graph.graph import create_supervisor_graph
from langchain_core.messages import HumanMessage
from services.redis_caching import redis_caching
from services.mongodb import get_mongo_client

redis_client = redis_caching()
client = get_mongo_client()

checkpoint_db = client["checkpointing_db"]
checkpoints_col = checkpoint_db["checkpoints"]
checkpoint_write_col = checkpoint_db["checkpoint_write"]

app = FastAPI()
graph = create_supervisor_graph()

class QueryRequest(BaseModel):
    message: str
    thread_id: str = Field(default="1")


@app.post("/v1/chat")
async def query_graph(request: QueryRequest):
    thread_id = request.thread_id or str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}
    state = {"messages": [HumanMessage(content=request.message)]}
    result = graph.invoke(state, config=config)

    messages = result.get("messages", [])
    response = messages[-1] if messages else None
    ai_message = response.content if response else None

    # Store in Redis
    redis_client.rpush(thread_id, f"Human: {request.message}")
    if ai_message:
        redis_client.rpush(thread_id, f"AI: {ai_message}")

    return {
        "thread_id": thread_id,
        "response": ai_message
    }

@app.post("/v1/sessions/new")
async def new_session():
    thread_id = str(uuid.uuid4())
    redis_client.sadd("chat:sessions", thread_id)
    return {"thread_id": thread_id}

# ===== List sessions =====
@app.get("/v1/sessions")
async def list_sessions():
    sessions = redis_client.smembers("chat:sessions")
    sessions = [s for s in sessions]
    return {"sessions": sessions}

# ===== Get history =====
@app.get("/v1/history/{thread_id}")
async def get_history(thread_id: str):
    messages = redis_client.lrange(thread_id, 0, -1)
    messages = [msg for msg in messages]
    return {"thread_id": thread_id, "history": messages}

@app.delete("/v1/sessions/{thread_id}")
async def delete_session(thread_id: str):
    # --- MongoDB ---
    res1 = checkpoints_col.delete_many({"thread_id": thread_id})
    res2 = checkpoint_write_col.delete_many({"thread_id": thread_id})

    # --- Redis ---
    redis_deleted_from_set = redis_client.srem("chat:sessions", thread_id)
    redis_deleted_msgs = redis_client.delete(thread_id)

    deleted_anything = (
        res1.deleted_count > 0
        or res2.deleted_count > 0
        or redis_deleted_from_set > 0
        or redis_deleted_msgs > 0
    )

    if not deleted_anything:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "status": "success",
        "deleted_thread_id": thread_id,
        "mongo_deleted": {
            "checkpoints": res1.deleted_count,
            "checkpoint_write": res2.deleted_count,
        },
        "redis_deleted": {
            "from_sessions_set": bool(redis_deleted_from_set),
            "messages_deleted": bool(redis_deleted_msgs),
        },
    }

# ===== Health check =====
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Server is running"}

# ===== Redirect root =====
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
