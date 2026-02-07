from sqlalchemy import Column, Integer, String
from database import Base


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    subject = Column(String)
    duration = Column(Integer)
