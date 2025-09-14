from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os

load_dotenv()
print("🔐 My API Key:", os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    print("📥 Received data from frontend:", data)

    resume = data.get("resumeText")
    job_desc = data.get("jobDescription")
    language = data.get("language")

    prompt = f"""
    You are an AI HR assistant. Based on the following resume and job description,
    generate the following in {language}:
    1. A personalized cover letter
    2. Important resume keywords
    3. 5 predicted interview questions

    Resume:
    {resume}

    Job Description:
    {job_desc}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        result = response['choices'][0]['message']['content']
        sections = result.split('\n\n')
        return jsonify({
            "cover_letter": sections[0],
            "keywords": sections[1] if len(sections) > 1 else "N/A",
            "interview_questions": sections[2] if len(sections) > 2 else "N/A"
        })
    except Exception as e:
        print("💥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
