from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from utils.database import Base


class JobInformation(Base):
    __tablename__ = "job_information"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    title = Column(String)
    url = Column(String, unique=True, index=True)
    restriction = Column(Boolean)
    state = Column(String)
    match_percentage = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    ai_analysis = Column(String)
    description = Column(String)
