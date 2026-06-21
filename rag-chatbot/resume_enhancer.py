from retriever import retrieve_all
from rag import ask_claude

ENHANCE_PROMPT = """You are a resume writing expert. Rewrite the bullet point below to be stronger and more impactful for the target role.

Target Role Context:
- Role: {role_summary}
- Key Skills: {required_skills}

Original Bullet:
{bullet}

Rewrite using:
1. Strong action verb at the start (Led, Built, Reduced, Shipped, etc.)
2. STAR structure where applicable (Action → Result)
3. Quantified impact — add plausible metrics if none exist, mark with [estimate]
4. Keywords aligned to the target role

Output EXACTLY in this format:
**Improved:** [rewritten bullet]
**Why it's stronger:** [1-2 sentences on key improvements]"""


def enhance_bullet(bullet: str, jd_analysis: dict) -> str:
    prompt = ENHANCE_PROMPT.format(
        role_summary=jd_analysis.get("role_summary", ""),
        required_skills=", ".join(jd_analysis.get("required_skills", [])),
        bullet=bullet.strip(),
    )
    return ask_claude(prompt, label="Resume Enhancer")


def keyword_coverage(jd_analysis: dict) -> dict:
    all_keywords = list(dict.fromkeys(
        jd_analysis.get("required_skills", []) +
        jd_analysis.get("nice_to_have", []) +
        jd_analysis.get("keywords", [])
    ))
    resume_text = " ".join(retrieve_all()).lower()
    covered = [k for k in all_keywords if k.lower() in resume_text]
    missing = [k for k in all_keywords if k.lower() not in resume_text]
    return {"covered": covered, "missing": missing}


if __name__ == "__main__":
    sample_jd = {
        "role_summary": "AI Engineer building LLM applications",
        "required_skills": ["Python", "LLMs", "RAG"],
        "nice_to_have": ["FastAPI"],
        "keywords": ["machine learning", "NLP"],
    }
    sample_bullet = "worked on backend services using java"
    result = enhance_bullet(sample_bullet, sample_jd)
    print(result)
