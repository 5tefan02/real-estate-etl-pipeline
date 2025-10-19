# db_manager_fixed.py
import os
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
import pandas as pd

# SQLAlchemy base class for ORM models
Base = declarative_base()

# ORM model for the "real_estate" table
class Estate(Base):
    __tablename__ = "real_estate"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)   # Auto-increment primary key
    judet = Column(String, nullable=True)                        # County
    oras = Column(String, nullable=True)                         # City
    suprafata = Column(Integer, nullable=True)                   # Surface (sqm)
    etaj = Column(String, nullable=True)                         # Floor
    an_constructie = Column(String, nullable=True)               # Construction year
    pret = Column(Integer, nullable=False)                       # Price (required field)

# Database configuration
url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="1234",
    host="localhost",
    port=5432,
    database="Scooby"
)

# Create database engine (echo=True shows executed SQL in console)
engine = create_engine(url, echo=True, future=True)

# 1) Test database connection 
try:
    # Open connection and run a simple SELECT to verify the database is reachable
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connection successful. SELECT 1 returned ->", result.scalar_one())
except Exception as e:
    print("Connection error:", e)
    raise  # Stop execution if the database can't be reached

# 2) Create the table (if it does not exist already) 
Base.metadata.create_all(engine)
print("Tables created or verified.")

#  3) Import data from CSV using PostgreSQL COPY (fast import) 
CSV_PATH = "olx_imobiliare.csv"

# Check if CSV file exists in the same directory
if os.path.exists(CSV_PATH):
    print("CSV file found:", CSV_PATH)

    try:
        # Copy CSV data directly into PostgreSQL (very fast method)
        raw_conn = engine.raw_connection()
        try:
            cur = raw_conn.cursor()

            # Open CSV and run the COPY command
            with open(CSV_PATH, "r", encoding="utf-8") as f:
                sql = """
                COPY real_estate(judet, oras, suprafata, etaj, an_constructie, pret)
                FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',');
                """
                cur.copy_expert(sql, f)

            raw_conn.commit()  # Save changes
            print("CSV imported using COPY.")
        finally:
            # Always close cursor and connection
            cur.close()
            raw_conn.close()

    except Exception as e:
        print("Error during COPY import:", e)

else:
    # CSV not found, show a warning
    print(f"CSV file not found: {CSV_PATH}. Place it in the same folder or update CSV_PATH.")
