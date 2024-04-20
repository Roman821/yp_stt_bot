from sqlalchemy import Column, Integer

from database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True, unique=True, nullable=False)
    seconds_blocks_spent = Column(Integer, nullable=False, default=0)
