import streamlit as st
import requests

API_URL = "http://localhost:8000/v1"

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title("Tech Support Chatbot")

# ===== Helper functions =====
def get_sessions():
    r = requests.get(f"{API_URL}/sessions")
    if r.status_code == 200:
        return r.json().get("sessions", [])
    return []

def get_history(thread_id):
    r = requests.get(f"{API_URL}/history/{thread_id}")
    if r.status_code == 200:
        return r.json().get("history", [])
    return []

def new_session():
    r = requests.post(f"{API_URL}/sessions/new")
    if r.status_code == 200:
        return r.json().get("thread_id")
    return None

def send_message(message, thread_id):
    payload = {"message": message, "thread_id": thread_id}
    r = requests.post(f"{API_URL}/chat", json=payload)
    if r.status_code == 200:
        return r.json().get("response")
    return "⚠️ API error"

def delete_session(thread_id):
    r = requests.delete(f"{API_URL}/sessions/{thread_id}")
    return r.status_code == 200


# ===== Sidebar: Sessions =====
st.sidebar.title("💬 Chat Sessions")

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "delete_target" not in st.session_state:
    st.session_state.delete_target = None

# nút tạo session mới
if st.sidebar.button("➕ New session"):
    new_id = new_session()
    st.session_state.current_session = new_id
    st.rerun()

# danh sách sessions
sessions = get_sessions()
for s in sessions:
    col1, col2 = st.sidebar.columns([4, 1])
    with col1:
        if st.button(s, key=f"session-{s}"):
            st.session_state.current_session = s
            st.rerun()
    with col2:
        if st.button("❌", key=f"delete-{s}"):
            st.session_state.delete_target = s

# xác nhận xóa
if st.session_state.delete_target:
    target = st.session_state.delete_target
    st.sidebar.warning(f"❗ Delete session {target}?")
    col_ok, col_cancel = st.sidebar.columns(2)
    with col_ok:
        if st.button("✅ Yes", key="confirm-delete"):
            ok = delete_session(target)
            if ok:
                if st.session_state.current_session == target:
                    st.session_state.current_session = None
                st.session_state.delete_target = None
                st.rerun()
            else:
                st.sidebar.error("❌ Failed to delete")
    with col_cancel:
        if st.button("❌ No", key="cancel-delete"):
            st.session_state.delete_target = None
            st.rerun()


# ===== Main Chat Window =====
thread_id = st.session_state.current_session
if thread_id:
    st.subheader(f"🧵 Session ID: {thread_id}")

    # Load history
    history = get_history(thread_id)
    for msg in history:
        role, content = msg.split(":", 1)
        if role.strip() == "Human":
            st.chat_message("user").write(content.strip())
        else:
            st.chat_message("assistant").write(content.strip())

    # Chat input
    if prompt := st.chat_input("Enter..."):
        st.chat_message("user").write(prompt)
        reply = send_message(prompt, thread_id)
        st.chat_message("assistant").write(reply)

