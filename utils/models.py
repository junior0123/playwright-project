from sqlalchemy import Column, Integer, String, Boolean

from utils.database import Base


class JobInformation(Base):
    __tablename__ = "job_information"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    title = Column(String)
    url = Column(String, unique=True, index=True)
    restriction = Column(Boolean)
    compatible = Column(String)
    description = Column(String)
