import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLSession

from main import Session as ScanSession
from models import Base, Session, Macaddress, SessionRecord


@pytest.fixture(scope='function')
def database():
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
    # prints the DDL for table creation
    #print(Base.metadata.create_all(engine))

    session = SQLSession(engine)
    yield session

class TestDatabase:

    def test_session(self, database):
        s = ScanSession()
        s.scan_date = '2012-06-29'

        session1 = Session(scan_date=s.scan_date)
        assert type(session1.scan_date) == datetime
        assert str(session1) == 'Scan Session: 2012-06-29 00:00:00'

    def test_macaddress(self, database):
        s = Macaddress(mac='c0:c1:c0:01:30:c9')
        print(s.mac)