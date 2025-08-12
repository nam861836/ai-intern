import uuid

import streamlit as st
from langchain_core.messages import HumanMessage


def get_graph():
    if "graph" not in st.session_state:
        # Lazy import to avoid failing at import time if env vars are missing
        from graph import create_supervisor_graph

        st.session_state.graph = create_supervisor_graph()
    return st.session_state.graph


def init_session_state():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"web-{uuid.uuid4()}"
    if "chat" not in st.session_state:
        st.session_state.chat = []  # list of {role: "user"|"assistant", content: str}


def reset_conversation():
    st.session_state.thread_id = f"web-{uuid.uuid4()}"
    st.session_state.chat = []


def main():
    st.set_page_config(page_title="RAG Advanced Demo", page_icon="🤖")
    st.title("🤖 RAG Advanced Demo")
    st.caption("Chat with a supervisor agent that can search web, query DB, or do RAG on a policy PDF.")

    init_session_state()

    with st.sidebar:
        st.subheader("Session")
        st.text(f"Thread: {st.session_state.thread_id}")
        if st.button("Reset conversation", use_container_width=True):
            reset_conversation()
            st.rerun()

    # Render prior messages
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input
    prompt = st.chat_input("Ask something…")
    if prompt:
        # Echo user message
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Invoke graph with checkpointing using the per-session thread_id
        graph = get_graph()
        checkpoint_config = {"configurable": {"thread_id": st.session_state.thread_id}}

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    result = graph.invoke({"messages": [HumanMessage(content=prompt)]}, config=checkpoint_config)
                    ai_msg = result["messages"][-1]
                    content = getattr(ai_msg, "content", str(ai_msg))
                except Exception as e:
                    content = f"Error: {e}"
                st.write(content)
                st.session_state.chat.append({"role": "assistant", "content": content})


if __name__ == "__main__":
    main()


