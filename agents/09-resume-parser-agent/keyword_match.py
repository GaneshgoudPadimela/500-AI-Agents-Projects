"""Keyword match helper for the resume parser agent.
The main agent uses an LLM to parse a resume and score fit. This helper adds a
cheap, deterministic first pass that needs no API key: it extracts known tech
keywords from a resume and a job description, then reports which job keywords
the resume already covers and which ones are missing.
Usage:
    python keyword_match.py resume.txt job_description.txt
"""
import re
import sys
KNOWN_KEYWORDS = [
    "java", "spring boot", "spring", "microservices", "rest", "api", "kafka",
    "cassandra", "docker", "kubernetes", "python", "airflow", "spark",
    "sql", "nosql", "aws", "gcp", "azure", "ci/cd", "jenkins", "git",
    "hibernate", "jpa", "mongodb", "postgresql", "redis", "graphql",
    "react", "angular", "node.js", "typescript", "javascript",
    "langchain", "crewai", "autogen", "langgraph", "openai", "llm", "rag",
]

def find_keywords(text):
    """Return the set of known keywords present in the text."""
    lowered = text.lower()
    found = set()
    for keyword in KNOWN_KEYWORDS:
        if re.search(r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])", lowered):
            found.add(keyword)
    return found

def keyword_match(resume_text, job_text):
    """Compare resume keywords against job-description keywords."""
    resume_keywords = find_keywords(resume_text)
    job_keywords = find_keywords(job_text)
    matched = job_keywords & resume_keywords
    missing = job_keywords - resume_keywords
    score = round(100 * len(matched) / len(job_keywords), 1) if job_keywords else 0.0
    return {
        "job_keywords": sorted(job_keywords),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "score_percent": score,
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        resume = f.read()
    with open(sys.argv[2], encoding="utf-8") as f:
        job = f.read()
    result = keyword_match(resume, job)
    print(f"Keyword match: {result['score_percent']}%")
    print(f"Matched: {', '.join(result['matched']) or 'none'}")
    print(f"Missing: {', '.join(result['missing']) or 'none'}")
