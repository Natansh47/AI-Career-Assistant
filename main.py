from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.ai_service import (
    extract_skills,
    generate_questions,
    generate_study_plan,
    analyze_resume
)

from database.db import engine, get_db
from models.job_model import Job

app = FastAPI()

Job.metadata.create_all(bind=engine)


class JobRequest(BaseModel):
    jd: str


class QuestionRequest(BaseModel):
    role: str
    skills: list


class StudyPlanRequest(BaseModel):
    skills: list


class SaveJobRequest(BaseModel):
    company: str
    role: str
    jd: str
    skills: str
    questions: str
    study_plan: str
    status: str


class ResumeRequest(BaseModel):
    resume: str
    jd: str


@app.get("/")
def home():
    return {
        "message": "AI Career Assistant Backend Running"
    }


@app.post("/extract-skills")
def extract(request: JobRequest):

    result = extract_skills(request.jd)

    return {
        "skills": result
    }


@app.post("/generate-questions")
def questions(request: QuestionRequest):

    result = generate_questions(
        request.role,
        request.skills
    )

    return {
        "questions": result
    }


@app.post("/study-plan")
def study_plan(request: StudyPlanRequest):

    result = generate_study_plan(
        request.skills
    )

    return {
        "study_plan": result
    }


@app.post("/save-job")
def save_job(
    request: SaveJobRequest,
    db: Session = Depends(get_db)
):

    new_job = Job(
        company=request.company,
        role=request.role,
        jd=request.jd,
        skills=request.skills,
        questions=request.questions,
        study_plan=request.study_plan,
        status=request.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job saved successfully",
        "job_id": new_job.id
    }


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(Job).all()

    return jobs


@app.put("/job-status/{job_id}")
def update_job_status(
    job_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {
            "error": "Job not found"
        }

    job.status = status

    db.commit()

    return {
        "message": "Status updated successfully"
    }


@app.post("/analyze-resume")
def resume_analysis(request: ResumeRequest):

    result = analyze_resume(
        request.resume,
        request.jd
    )

    return {
        "analysis": result
    }

@app.delete("/delete-job/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        return {
            "message": "Job not found"
        }

    db.delete(job)

    db.commit()

    return {
        "message": "Job deleted successfully"
    }