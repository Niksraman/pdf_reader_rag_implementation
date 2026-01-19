
import streamlit as st
import requests

st.title("Chat With Your Docs")

question = st.text_input("Ask a question:")

if st.button("Ask"):
    resp = requests.post("http://127.0.0.1:8000/ask", json={"question": question})
    data = resp.json()
    st.subheader("Answer")
    st.write(data["answer"])

    st.subheader("Sources")
    for s in data["sources"]:
        st.write("- ", s[:200], "...")
