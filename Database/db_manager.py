# sync_example.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

Base = declarative_base()

class Estate(Base):
    __tablename__ = "real_estate"
    id = Column(Integer, primary_key=True)
    judet = Column(String, nullable=False)
    suprafata = Column(Integer, nullable=False)
    etaj = Column(String, nullable=False)
    an_constructie = Column(String, nullable=False)
    pret = Column(Integer, nullable=False)

# creezi URL-ul
url = URL.create(
    drivername="postgresql+psycopg",  # sau "postgresql+psycopg2" dacă ai instalat psycopg2-binary
    username="postgres",
    password="1234",
    host="localhost",
    port=5432,
    database="Scooby"
)

engine = create_engine(url, echo=True, future=True)

# creezi tabelele dacă nu există
Base.metadata.create_all(engine)

# creezi session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def insert(id: str, judet: str, suprafata: int, etaj: str, an_constructie: str, pret: int):
    with SessionLocal() as session:
        estate = Estate(id=id, judet=judet, suprafata=suprafata, etaj=etaj, an_constructie=an_constructie, pret=pret)
        session.add(estate)
        session.commit()        # salvează în DB
        session.refresh(estate)   # aduce valorile generate (ex: id)
        return estate
