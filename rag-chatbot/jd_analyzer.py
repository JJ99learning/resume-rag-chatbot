import json
import re
from rag import ask_claude

EXTRACT_PROMPT = """You are a job requirements analyst. Extract key information from this job description.

Job Description:
{jd_text}

Output ONLY valid JSON with no markdown, no code blocks, no extra text:
{{
  "role_summary": "one sentence describing the role",
  "required_skills": ["skill1", "skill2"],
  "nice_to_have": ["skill1", "skill2"],
  "keywords": ["keyword1", "keyword2"]
}}"""


def analyze_jd(jd_text: str) -> dict:
    prompt = EXTRACT_PROMPT.format(jd_text=jd_text.strip())
    response = ask_claude(prompt, label="Step 1: JD Analysis")
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    raise ValueError(f"Failed to parse JD analysis JSON: {response[:300]}")


if __name__ == "__main__":
    sample = """
    We are hiring an AI Engineer to build LLM-powered applications.
    Requirements: 2+ years Python, experience with LLMs (GPT/Claude), RAG pipelines, vector databases.
    Nice to have: FastAPI, MLOps, fine-tuning experience.
    """
    result = analyze_jd(sample)
    print(json.dumps(result, indent=2, ensure_ascii=False))
