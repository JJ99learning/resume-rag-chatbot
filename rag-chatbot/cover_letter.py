from retriever import retrieve
from rag import ask_claude

COVER_LETTER_PROMPT = """You are a professional career writer. Write a compelling, tailored cover letter based on the job description and resume below.

Job Requirements:
- Role: {role_summary}
- Required Skills: {required_skills}
- Nice to Have: {nice_to_have}
- Keywords: {keywords}

Resume Content:
{resume_content}

Write a cover letter that:
1. Opens with a strong hook (not "I am applying for...")
2. Connects resume experience directly to JD requirements using specific examples
3. Incorporates keywords from the JD naturally
4. Is 3-4 paragraphs, professional but not stiff
5. Ends with a clear call to action

Output ONLY the cover letter text. No commentary, no labels, no meta-text."""


def generate_cover_letter(jd_analysis: dict) -> str:
    skills = jd_analysis.get("required_skills", []) + jd_analysis.get("keywords", [])
    query = " ".join(skills[:6])
    chunks = retrieve(query)
    resume_content = "\n\n".join(chunks)

    prompt = COVER_LETTER_PROMPT.format(
        role_summary=jd_analysis.get("role_summary", ""),
        required_skills=", ".join(jd_analysis.get("required_skills", [])),
        nice_to_have=", ".join(jd_analysis.get("nice_to_have", [])),
        keywords=", ".join(jd_analysis.get("keywords", [])),
        resume_content=resume_content,
    )
    return ask_claude(prompt, label="Step 4: Cover Letter")


if __name__ == "__main__":
    sample_analysis = {
        "role_summary": "AI Engineer building LLM applications",
        "required_skills": ["Python", "LLMs", "RAG", "Vector databases"],
        "nice_to_have": ["FastAPI", "MLOps"],
        "keywords": ["AI", "machine learning", "NLP"],
    }
    result = generate_cover_letter(sample_analysis)
    print(result)
