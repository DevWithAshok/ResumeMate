import streamlit as st
import requests

st.set_page_config(page_title="ResumeMate - CareerMitra")

st.title("📄 ResumeMate by CareerMitra")
st.write("Generate cover letters, resume keywords, and interview questions using AI.")

resume_text = st.text_area("📎 Paste your Resume Text here", height=200)
job_desc = st.text_area("🧾 Paste the Job Description", height=200)
language = st.selectbox("🌐 Select Output Language", ["English", "Hindi", "Telugu"])

if st.button("Generate with AI"):
    if not resume_text or not job_desc:
        st.warning("Please fill in both resume and job description.")
    else:
        with st.spinner("Thinking with OpenAI..."):
            payload = {
                "resume": resume_text,
                "job_description": job_desc,
                "language": language
            }
            response = requests.post("http://localhost:5000/generate", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.subheader("📝 Cover Letter")
                st.text_area("Generated Cover Letter", value=data["cover_letter"], height=200)
                st.subheader("📌 Resume Keywords")
                st.write(data["keywords"])
                st.subheader("🎤 Interview Questions")
                st.text_area("AI-Predicted Interview Questions", value=data["interview_questions"], height=150)
            else:
                st.error("Something went wrong. Check if backend is running.")
