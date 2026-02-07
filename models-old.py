from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

# ================= USERS =================


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


# ================= EXPENSES =================
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))


# ================= STUDY =================
class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    subject = Column(String)
    duration = Column(Integer)


# ================= USERS =================


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


# ================= EXPENSES =================
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))


# ================= STUDY =================
class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    subject = Column(String)
    duration = Column(Integer)
