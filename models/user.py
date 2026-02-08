from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    dark_mode = Column(Integer, default=0, nullable=False)

    # NEW: list of expenses this user owns
    expenses = relationship("Expense", back_populates="user")
    study_plans = relationship("StudyPlan", back_populates="user")
