from graph import create_langgraph

def main():
    graph = create_langgraph()
    result = graph.invoke({"input": "What is the recipe for the best chocolate chip cookies?"})
    print("Result:", result)

if __name__ == "__main__":
    main()
