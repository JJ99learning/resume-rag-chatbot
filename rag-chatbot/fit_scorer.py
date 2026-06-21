import re
from retriever import retrieve
from rag import ask_claude

SCORE_PROMPT = """You are a career coach evaluating resume-to-JD fit. Be honest and specific.

Job Requirements:
- Role: {role_summary}
- Required Skills: {required_skills}
- Nice to Have: {nice_to_have}
- Keywords: {keywords}

Resume Content:
{resume_content}

Provide your assessment in EXACTLY this format:

FIT SCORE: [0-100]

MATCHED SKILLS:
- [skills from JD clearly present in resume]

MISSING SKILLS:
- [required skills NOT found in resume]

TOP 3 SUGGESTIONS:
1. [highest-impact improvement]
2. [second improvement]
3. [third improvement]

SUMMARY: [2-3 sentences on overall fit and biggest opportunity]"""


def score_fit(jd_analysis: dict) -> dict:
    skills = jd_analysis.get("required_skills", []) + jd_analysis.get("keywords", [])
    query = " ".join(skills[:6])
    chunks = retrieve(query)
    resume_content = "\n\n".join(chunks)

    prompt = SCORE_PROMPT.format(
        role_summary=jd_analysis.get("role_summary", ""),
        required_skills=", ".join(jd_analysis.get("required_skills", [])),
        nice_to_have=", ".join(jd_analysis.get("nice_to_have", [])),
        keywords=", ".join(jd_analysis.get("keywords", [])),
        resume_content=resume_content,
    )

    report = ask_claude(prompt, label="Step 2: Fit Scoring")

    score = 0
    match = re.search(r'FIT SCORE:\s*(\d+)', report)
    if match:
        score = int(match.group(1))

    return {"score": score, "report": report}


if __name__ == "__main__":
    sample_analysis = {
        "role_summary": "AI Engineer building LLM applications",
        "required_skills": ["Python", "LLMs", "RAG", "Vector databases"],
        "nice_to_have": ["FastAPI", "MLOps"],
        "keywords": ["AI", "machine learning", "NLP"],
    }
    result = score_fit(sample_analysis)
    print(f"Score: {result['score']}/100\n")
    print(result["report"])
