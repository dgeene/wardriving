from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass

class Session(Base):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_date: Mapped[str] = mapped_column(Date)

    def __repr__(self) -> str:
        return f'Scan Session: {self.scan_date}'

class Macaddress(Base):
    __tablename__ = 'macaddress'

    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f'Mac Address: {self.id}'

class SessionRecord(Base):
    __tablename__ = 'session_record'

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[str] = mapped_column(String(20))
    longitude: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return f'Record: {self.id}'
