from query_classifier import classify_query

def route_query(state):
    query = state["input"]
    route = classify_query(query)
    return {"route": route, "input": query}
