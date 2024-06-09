import pytest
from utils.database import SessionLocal

@pytest.fixture(scope='function')
def db_session():
    session = SessionLocal()
    yield session
    print("Cerrando sesion")
    session.close()
