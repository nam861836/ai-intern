import uuid
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from graph.graph import create_supervisor_graph
from langchain_core.messages import HumanMessage

app = FastAPI()
graph = create_supervisor_graph()

class QueryRequest(BaseModel):
    message: str
    thread_id: str = Field(default="1")


@app.post("/query")
async def query_graph(request: QueryRequest):
    # Generate a unique thread_id for checkpointing
    thread_id = request.thread_id or str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}
    state = {"messages": [HumanMessage(content=request.message)]}
    result = graph.invoke(state, config=config)
    messages = result.get("messages", [])
    output = "\n".join([str(m.content) for m in messages if hasattr(m, "content")])
    return {"output": output, "messages": [m.content for m in messages if hasattr(m, "content")]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
