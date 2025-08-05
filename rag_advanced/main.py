from graph import create_langgraph
from schema import getStateRoute

def getRoute(): 
    return lambda state: state["route"]

def main():
    graph = create_langgraph()
    while True:
        query = input("Enter your query ('q' to quit): ")
        if query.lower() == 'q':
            break
        result = graph.invoke({"input": query})
        get_route = lambda state: state["route"]
        route = get_route(result)
        if route == "tavily": 
            #print(result)
            print("Route: ", result["route"])
            print("Answer: ", result["output"]["answer"])
            #print("Source: ", type(result["output"]["results"][0]))
        else: 
            print(result)


if __name__ == "__main__":
    main()
