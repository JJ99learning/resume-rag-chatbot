from retriever import retrieve
from rag import ask_claude

INTERVIEW_PROMPT = """You are a technical interview coach. Based on the job requirements and resume below, generate the 10 most likely interview questions and provide reference answers grounded in the resume content.

Job Requirements:
- Role: {role_summary}
- Required Skills: {required_skills}
- Keywords: {keywords}

Resume Content:
{resume_content}

Output EXACTLY in this format (no extra text before or after):

**Q1: [question]**
A: [answer based on resume content, 2-4 sentences, specific and concrete]

**Q2: [question]**
A: [answer]

Continue through Q10."""


def generate_interview_prep(jd_analysis: dict) -> str:
    skills = jd_analysis.get("required_skills", []) + jd_analysis.get("keywords", [])
    query = " ".join(skills[:6])
    chunks = retrieve(query)
    resume_content = "\n\n".join(chunks)

    prompt = INTERVIEW_PROMPT.format(
        role_summary=jd_analysis.get("role_summary", ""),
        required_skills=", ".join(jd_analysis.get("required_skills", [])),
        keywords=", ".join(jd_analysis.get("keywords", [])),
        resume_content=resume_content,
    )
    return ask_claude(prompt, label="Step 3: Interview Prep")


if __name__ == "__main__":
    sample_analysis = {
        "role_summary": "AI Engineer building LLM applications",
        "required_skills": ["Python", "LLMs", "RAG", "Vector databases"],
        "nice_to_have": ["FastAPI", "MLOps"],
        "keywords": ["AI", "machine learning", "NLP"],
    }
    result = generate_interview_prep(sample_analysis)
    print(result)
