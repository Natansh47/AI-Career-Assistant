import streamlit as st
import requests
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="AI Career Assistant",
    layout="wide"
)


API_URL = "http://127.0.0.1:8000"


if "questions_text" not in st.session_state:
    st.session_state.questions_text = ""

if "study_plan_text" not in st.session_state:
    st.session_state.study_plan_text = ""

if "skills_list" not in st.session_state:
    st.session_state.skills_list = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

if "study_chat_history" not in st.session_state:
    st.session_state.study_chat_history = []

if "study_questions" not in st.session_state:
    st.session_state.study_questions = []

if "study_question_index" not in st.session_state:
    st.session_state.study_question_index = 0

if "roadmap_text" not in st.session_state:
    st.session_state.roadmap_text = ""

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = ""


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Applications",
        "Interview Questions",
        "Study Mentor",
        "Roadmap",
        "Resume Suggestions"
    ]
)


st.title("AI Career Assistant")

st.caption("AI-powered job tracking and interview preparation")


response = requests.get(f"{API_URL}/jobs")
jobs = response.json()


if page == "Applications":

    st.header("Saved Job Applications")

    if jobs:

        df = pd.DataFrame(jobs)

        display_df = df[[
            "id",
            "company",
            "role",
            "skills",
            "status"
        ]]

        st.subheader("Saved Applications")

        selected_row = st.selectbox(
            "Select Application to View JD",
            options=display_df.index,
            format_func=lambda x: f"{display_df.loc[x, 'company']} - {display_df.loc[x, 'role']}"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Job Description")

        st.text_area(
            "Selected JD",
            value=df.loc[selected_row, "jd"],
            height=250,
            disabled=True
        )


    else:
        st.warning("No jobs found")


    st.divider()

    st.header("Add Job Application")

    with st.form("job_form"):

        company = st.text_input("Company Name")

        role = st.text_input("Role")

        jd = st.text_area(
            "Paste Job Description",
            height=250
        )

        submitted = st.form_submit_button("Extract Skills & Save Job")

        if submitted:

            extract_response = requests.post(
                f"{API_URL}/extract-skills",
                json={
                    "jd": jd
                }
            )

            extracted_data = extract_response.json()

            if "skills" in extracted_data and isinstance(extracted_data["skills"], dict):
                extracted_data = extracted_data["skills"]

            skills_list = extracted_data.get("skills", [])

            st.session_state.skills_list = skills_list

            save_response = requests.post(
                f"{API_URL}/save-job",
                json={
                    "company": company,
                    "role": role,
                    "jd": jd,
                    "skills": ", ".join(skills_list),
                    "questions": "",
                    "study_plan": "",
                    "status": "Applied"
                }
            )

            save_result = save_response.json()

            st.success("Job Application Saved Successfully")

            st.write(save_result)

    st.divider()

    st.subheader("Delete Job Applications")

    if jobs:

        job_options = {
            f"{row['id']} - {row['company']} - {row['role']}": row["id"]
            for _, row in df.iterrows()
        }

        selected_jobs = st.multiselect(
            "Select Jobs to Delete",
            options=list(job_options.keys())
        )

        if st.button("Delete Selected Jobs"):

            for job_label in selected_jobs:

                job_id = job_options[job_label]

                requests.delete(
                    f"{API_URL}/delete-job/{job_id}"
                )

            st.success("Selected jobs deleted successfully")

            st.rerun()


if page == "Interview Questions":

    st.header("Interview Question Chatbot")

    if jobs:

        jobs_df = pd.DataFrame(jobs)

        selected_job_label = st.selectbox(
            "Select Saved Job",
            options=[
                f"{row['id']} - {row['company']} - {row['role']}"
                for _, row in jobs_df.iterrows()
            ]
        )

        selected_job_id = int(selected_job_label.split(" - ")[0])

        selected_job = jobs_df[
            jobs_df["id"] == selected_job_id
        ].iloc[0]

        st.subheader("Selected Job")

        st.write(f"Company: {selected_job['company']}")
        st.write(f"Role: {selected_job['role']}")

        if st.button("Generate Initial Questions"):

            skills_list = []

            if selected_job.get("skills"):
                skills_list = [
                    skill.strip()
                    for skill in str(selected_job['skills']).split(",")
                ]

            questions_response = requests.post(
                f"{API_URL}/generate-questions",
                json={
                    "role": selected_job["role"],
                    "skills": skills_list
                }
            )

            questions = questions_response.json()

            questions_text = questions.get(
                "questions",
                questions
            )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": questions_text
                }
            )

        st.divider()

        st.subheader("Interview Chat")

        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_input = st.chat_input(
            "Ask more interview questions or concepts..."
        )

        if user_input:

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            skills_list = []

            if selected_job.get("skills"):
                skills_list = [
                    skill.strip()
                    for skill in str(selected_job['skills']).split(",")
                ]

            followup_response = requests.post(
                f"{API_URL}/generate-questions",
                json={
                    "role": f"{selected_job['role']} - {user_input}",
                    "skills": skills_list
                }
            )

            followup_questions = followup_response.json()

            assistant_reply = followup_questions.get(
                "questions",
                followup_questions
            )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

            st.rerun()

    else:

        st.warning("No saved jobs found")


if page == "Study Mentor":

    st.header("Study Plan Chatbot")

    if jobs:

        jobs_df = pd.DataFrame(jobs)

        selected_job_label = st.selectbox(
            "Select Saved Job",
            options=[
                f"{row['id']} - {row['company']} - {row['role']}"
                for _, row in jobs_df.iterrows()
            ],
            key="study_job_selector"
        )

        selected_job_id = int(
            selected_job_label.split(" - ")[0]
        )

        selected_job = jobs_df[
            jobs_df["id"] == selected_job_id
        ].iloc[0]

        st.subheader("Selected Job")

        st.write(f"Company: {selected_job['company']}")
        st.write(f"Role: {selected_job['role']}")

        st.info(
            "Ask roadmap, learning, revision, or concept questions related to the selected role."
        )

        st.divider()

        st.subheader("Study Mentor Chat")

        for message in st.session_state.study_chat_history:

            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_input = st.chat_input(
            "Ask concepts, roadmap questions, or answer the mentor..."
        )

        if user_input:

            st.session_state.study_chat_history.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            skills_list = []

            if selected_job.get("skills"):

                skills_list = [
                    skill.strip()
                    for skill in str(
                        selected_job["skills"]
                    ).split(",")
                ]

            followup_response = requests.post(
                f"{API_URL}/study-plan",
                json={
                    "skills": skills_list + [user_input]
                }
            )

            followup_result = followup_response.json()

            assistant_reply = followup_result.get(
                "study_plan",
                followup_result
            )

            st.session_state.study_chat_history.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

            st.rerun()

    else:

        st.warning("No saved jobs found")


if page == "Roadmap":

    st.header("1 Week Study Roadmap")

    if jobs:

        jobs_df = pd.DataFrame(jobs)

        selected_job_label = st.selectbox(
            "Select Saved Job",
            options=[
                f"{row['id']} - {row['company']} - {row['role']}"
                for _, row in jobs_df.iterrows()
            ],
            key="roadmap_job_selector"
        )

        selected_job_id = int(
            selected_job_label.split(" - ")[0]
        )

        selected_job = jobs_df[
            jobs_df["id"] == selected_job_id
        ].iloc[0]

        st.subheader("Selected Job")

        st.write(f"Company: {selected_job['company']}")
        st.write(f"Role: {selected_job['role']}")

        if st.button("Generate 1 Week Roadmap"):

            skills_list = []

            if selected_job.get("skills"):

                skills_list = [
                    skill.strip()
                    for skill in str(
                        selected_job["skills"]
                    ).split(",")
                ]

            roadmap_prompt = [
                "Create a detailed 7 day study roadmap with daily tasks, concepts, interview prep, projects and revision topics"
            ]

            roadmap_response = requests.post(
                f"{API_URL}/study-plan",
                json={
                    "skills": skills_list + roadmap_prompt
                }
            )

            roadmap_result = roadmap_response.json()

            st.session_state.roadmap_text = roadmap_result.get(
                "study_plan",
                roadmap_result
            )

        if st.session_state.roadmap_text:

            st.subheader("Your 1 Week Roadmap")

            st.write(st.session_state.roadmap_text)

    else:

        st.warning("No saved jobs found")


if page == "Resume Suggestions":

    st.header("Resume Improvement Suggestions")

    if jobs:

        jobs_df = pd.DataFrame(jobs)

        selected_job_label = st.selectbox(
            "Select Saved Job",
            options=[
                f"{row['id']} - {row['company']} - {row['role']}"
                for _, row in jobs_df.iterrows()
            ],
            key="resume_job_selector"
        )

        selected_job_id = int(
            selected_job_label.split(" - ")[0]
        )

        selected_job = jobs_df[
            jobs_df["id"] == selected_job_id
        ].iloc[0]

        st.subheader("Selected Job")

        st.write(f"Company: {selected_job['company']}")
        st.write(f"Role: {selected_job['role']}")

        uploaded_resume = st.file_uploader(
            "Upload Resume",
            type=["txt", "md", "pdf"]
        )

        resume_text = ""

        if uploaded_resume is not None:

            if uploaded_resume.type == "application/pdf":

                pdf_reader = PdfReader(uploaded_resume)

                extracted_text = ""

                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() + "\n"

                resume_text = extracted_text

            else:

                stringio = StringIO(
                    uploaded_resume.getvalue().decode("utf-8")
                )

                resume_text = stringio.read()

            st.subheader("Uploaded Resume Preview")

            st.text_area(
                "Resume Content",
                value=resume_text,
                height=300,
                disabled=True
            )

        if st.button("Analyze Resume") and resume_text:

            skills_list = []

            if selected_job.get("skills"):

                skills_list = [
                    skill.strip()
                    for skill in str(
                        selected_job["skills"]
                    ).split(",")
                ]

            analysis_prompt = f'''
Analyze this resume for the role: {selected_job['role']}.

Resume:
{resume_text}

Target Skills:
{', '.join(skills_list)}

Give:
1. Skills to Add
2. Missing ATS Keywords
3. Project Suggestions
4. Bullet Point Improvements
5. Resume Score out of 100
6. Experience Gap Suggestions
7. Strongest Resume Sections
8. Weakest Resume Sections
9. Suggested Projects to Add
10. Final Hiring Readiness Verdict
'''

            analysis_response = requests.post(
                f"{API_URL}/study-plan",
                json={
                    "skills": [analysis_prompt]
                }
            )

            analysis_result = analysis_response.json()

            st.session_state.resume_analysis = analysis_result.get(
                "study_plan",
                analysis_result
            )

        if st.session_state.resume_analysis:

            st.subheader("AI Resume Analysis")

            st.write(st.session_state.resume_analysis)

    else:

        st.warning("No saved jobs found")