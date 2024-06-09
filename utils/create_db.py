from .database import engine, Base
from .models import JobInformation

Base.metadata.create_all(bind=engine)
