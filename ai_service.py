import requests
import re


def extract_skills(jd):

    prompt = f"""
    Extract:
    1. Skills
    2. Tools
    3. Concepts

    From this Job Description:

    {jd}

    Format clearly with headings.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma4",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    response_text = data.get("response", "")

    skills = []
    tools = []
    concepts = []

    current_section = None

    for line in response_text.splitlines():

        line = line.strip()

        if "Skills" in line:
            current_section = "skills"
            continue

        elif "Tools" in line:
            current_section = "tools"
            continue

        elif "Concepts" in line:
            current_section = "concepts"
            continue

        clean_line = re.sub(r"[*•-]", "", line).strip()

        if clean_line:

            if current_section == "skills":
                skills.append(clean_line)

            elif current_section == "tools":
                tools.append(clean_line)

            elif current_section == "concepts":
                concepts.append(clean_line)

    return {
        "skills": skills,
        "tools": tools,
        "concepts": concepts
    }


def generate_questions(role, skills):

    prompt = f"""
    Generate interview questions for:

    Role:
    {role}

    Skills:
    {skills}

    Generate:
    1. Beginner questions
    2. Intermediate questions
    3. Advanced questions
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma4",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data.get("response", "")


def generate_study_plan(skills):

    prompt = f"""
    Create a study plan for the following skills:

    {skills}

    Include:
    1. Topics to learn
    2. Practice recommendations
    3. Beginner to advanced roadmap
    4. Suggested free resources
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma4",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data.get("response", "")


def analyze_resume(resume, jd):

    prompt = f"""
    Compare this resume with the job description.

    Resume:
    {resume}

    Job Description:
    {jd}

    Return:
    1. Match score
    2. Missing skills
    3. Resume improvements
    4. ATS optimization suggestions
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma4",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data.get("response", "")