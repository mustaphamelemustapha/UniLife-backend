from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
