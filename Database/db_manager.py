# db_manager_fixed.py
import os
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
import pandas as pd

Base = declarative_base()

class Estate(Base):
    __tablename__ = "real_estate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    judet = Column(String, nullable=True)
    oras = Column(String, nullable=True)
    suprafata = Column(Integer, nullable=True)
    etaj = Column(String, nullable=True)
    an_constructie = Column(String, nullable=True)
    pret = Column(Integer, nullable=False)

# --- Config (schimbă după nevoie) ---
url = URL.create(
    drivername=f"postgresql+psycopg2",
    username="postgres",
    password="1234",
    host="localhost",
    port=5432,
    database="Scooby"
)

engine = create_engine(url, echo=True, future=True)

# --- 1) Test conexiune simplu ---
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Conexiune OK, SELECT 1 ->", result.scalar_one())
except Exception as e:
    print("Eroare la conectare:", e)
    raise

# --- 2) Creează tabelele (dacă nu există) ---
Base.metadata.create_all(engine)
print("Tabela(s) create/verificate (dacă nu existau).")
# --- 3) Exemple de inserare / încărcare CSV ---

CSV_PATH = "olx_imobiliare.csv"
if os.path.exists(CSV_PATH):
    print("Găsit CSV:", CSV_PATH)
    # Varianta B: COPY (performant) folosind raw_connection și copy_expert
    # Dezactivează Varianta A de mai sus dacă vrei doar COPY, ca să nu dublezi datele.
    try:
        raw_conn = engine.raw_connection()
        try:
            cur = raw_conn.cursor()
            with open(CSV_PATH, "r", encoding="utf-8") as f:
                sql = """
                COPY real_estate(judet, oras, suprafata, etaj, an_constructie, pret)
                FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',');
                """
                cur.copy_expert(sql, f)
            raw_conn.commit()
            print("CSV încărcat cu COPY (cursor).")
        finally:
            cur.close()
            raw_conn.close()
    except Exception as e:
        print("Eroare la COPY via raw_connection:", e)
else:
    print(f"Nu am găsit fișierul CSV: {CSV_PATH}. Pune-l în același folder sau schimbă CSV_PATH.")