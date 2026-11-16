import streamlit as st
from query import ask

st.set_page_config(
    page_title="Company Knowledge Assistant",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Company Knowledge Assistant")
st.caption("Ask questions — answers come from your internal documents with citations.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Chunks to retrieve", min_value=1, max_value=10, value=5)
    st.divider()
    st.markdown("**To add documents:**")
    st.markdown("1. Drop `.txt` files into `documents/`")
    st.markdown("2. Run `python ingest.py`")
    st.markdown("3. Restart this app")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander(f"📄 {len(msg['citations'])} source(s) used"):
                for i, (chunk, meta, dist) in enumerate(msg["citations"], 1):
                    st.markdown(f"**[{i}] {meta['source']}**")
                    st.markdown(f"> {chunk[:300]}{'...' if len(chunk) > 300 else ''}")
                    st.divider()

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            answer, citations = ask(prompt, top_k=top_k)
        st.markdown(answer)
        if citations:
            with st.expander(f"📄 {len(citations)} source(s) used"):
                for i, (chunk, meta, dist) in enumerate(citations, 1):
                    st.markdown(f"**[{i}] {meta['source']}**")
                    st.markdown(f"> {chunk[:300]}{'...' if len(chunk) > 300 else ''}")
                    st.divider()

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "citations": citations
    })