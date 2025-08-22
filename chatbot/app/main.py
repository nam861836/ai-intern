from graph.graph import create_supervisor_graph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from services.redis_caching import redis_caching

redis_client = redis_caching()

def main():
    # Config to keep state between turns
    checkpoint_config = {"configurable": {"thread_id": "2"}}
    thread_id = checkpoint_config["configurable"]["thread_id"]

    # Create the graph
    graph = create_supervisor_graph()

    print("=== Chatbot ===")
    print("Type 'q' or 'quit' to exit.\n")

    while True:
        query = input("You: ")
        if query.strip().lower() in ["q", "quit"]:
            print("Bye!")
            break

        # Run graph
        result = graph.invoke(
            {"messages": [HumanMessage(content=query)]},
            config=checkpoint_config
        )

        # Get last message from AI
        last_message = result["messages"][-1]
        print("AI:", last_message)
        
        redis_client.rpush(thread_id, f"Human: {query}")
        redis_client.rpush(thread_id, f"AI: {last_message.content}")

        # Show tool calls if exist (optional for debugging)
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            print("\n[Tool Calls]")
            for call in last_message.tool_calls:
                print(f"- Tool: {call['name']}, Args: {call['args']}")
            print()


if __name__ == "__main__":
    main()
