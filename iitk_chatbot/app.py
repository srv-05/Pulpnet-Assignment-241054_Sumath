import streamlit as st
from qa_pipeline import get_answer

st.title("IIT Kanpur Chatbot")
st.markdown("Ask a question based on IITK sources")

query = st.text_input("Your question:")
if query:
    with st.spinner("Thinking..."):
        answer = get_answer(query)
        s=''
        for i in range(0,len(answer)):
            s=s+answer[i]
    st.success("Answer: " + s)