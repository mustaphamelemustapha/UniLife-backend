from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.user import User  # import User model


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    # NEW: link to user
    user_id = Column(Integer, ForeignKey("users.id")
                     )  # foreign key to users table
    # relationship back to user
    user = relationship("User", back_populates="expenses")
