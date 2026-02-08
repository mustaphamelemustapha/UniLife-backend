from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from models.user import User  # import User model


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # NEW: link to user
    user_id = Column(Integer, ForeignKey("users.id")
                     )  # foreign key to users table
    # relationship back to user
    user = relationship("User", back_populates="expenses")
