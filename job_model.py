from sqlalchemy import Column, Integer, String, Text
from database.db import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String)

    role = Column(String)

    jd = Column(Text)

    skills = Column(Text)

    questions = Column(Text)

    study_plan = Column(Text)

    status = Column(String)