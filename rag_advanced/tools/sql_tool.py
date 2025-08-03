def query_sql_tool(state):
    query = state["input"]
    # giả lập SQL response
    return {"output": f"[SQL] Info for query: {query}"}
