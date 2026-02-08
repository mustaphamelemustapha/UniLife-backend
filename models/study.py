from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    day = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    date = Column(String, nullable=True)   # YYYY-MM-DD
    time = Column(String, nullable=True)   # HH:MM
    remind_at = Column(DateTime, nullable=True)
    reminder_sent = Column(Boolean, default=False, nullable=False)
    reminder_sent_at = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="study_plans")
