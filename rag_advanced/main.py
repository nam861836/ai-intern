from graph import create_supervisor_graph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

#from schema import getStateRoute

def main():
    checkpoint_config = {"configurable": {"thread_id": "1"}}
    graph = create_supervisor_graph()
    while True:
        query = input("Enter: ")
        if query.lower() == 'q':
            break
        result = graph.invoke({"messages": [HumanMessage(content=query)]}, config = checkpoint_config)
        print("Response: ", result["messages"][-1].content)

if __name__ == "__main__":
    main()
