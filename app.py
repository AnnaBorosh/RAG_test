import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pinecone import Pinecone


st.title("📑 The Batch Article Search")


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
pc_api = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pc_api)
index = pc.Index("ragtest")

def get_context_from_pinecone(question):
    results = index.search(
        namespace="__default__",
        query={"inputs": {"text": question},
               "top_k": 3}
    )
    matches = results.get("result", {}).get("hits", [])

    context_chunks = []
    top_image_url = None
    top_title = None
    top_link = None

    for i, match in enumerate(matches):
        fields = match.get("fields", {})
        if i == 0:
            top_image_url = fields.get("image_url")
            top_title = fields.get("title")
            top_link = fields.get("link")

        chunk = fields.get("text") or fields.get("title") or ""
        context_chunks.append(chunk)

    context = "\n\n".join(context_chunks)
    return context, top_image_url, top_title, top_link


def ask_gemini(question, context):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    prompt = f"""You are a helpful assistant. Use the following context to answer the question:

Context:
{context}

Question:
{question}

Answer:"""
    response = model.generate_content(prompt)
    return response.text



question = st.text_input("Ask your question:")

if question:
    with st.spinner("Thinking..."):
        context, image_url, article_title, article_link = get_context_from_pinecone(question)
        answer = ask_gemini(question, context)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.markdown("**Answer:**")
        st.write(answer)
        

    with right_col:
        if image_url:
            st.image(image_url, caption="Top related image", use_container_width=True)
        st.markdown("---")
        st.markdown("**Source article:**")
        st.markdown(f"[{article_title}]({article_link})", unsafe_allow_html=True)