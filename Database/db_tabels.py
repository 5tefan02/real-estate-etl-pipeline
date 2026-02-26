from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey 
from sqlalchemy.orm import relationship
from Database.db_manager import Base

class Estate(Base):
    __tablename__ = "raw_data"
    
    id_raw = Column(String(100), primary_key=True) 
    URL_anunt = Column(String(500), nullable=True)
    judet = Column(String(100), nullable=False)
    oras = Column(String(100), nullable=False)
    suprafata = Column(Integer, nullable=True)
    etaj = Column(String(100), nullable=True) 
    perioada_constructie = Column(String(100), nullable=True) # Schimbat în nullable=True pentru siguranță
    an_constructie = Column(String(100), nullable=True)
    compartimentare = Column(String(100), nullable=True)
    camere = Column(String(100), nullable=True) 
    pret = Column(Integer, nullable=False)
    tip_tranzactie = Column(String(50), nullable=True)
    tip_imobiliar = Column(String(50), nullable=True)
    platforma = Column(String(50), nullable=True)
    data = Column(Date, nullable=False)
    processed = Column(Boolean, nullable=False, default=False)
    
class Judet(Base):
    __tablename__ = 'judete'

    id_judet = Column(Integer, primary_key=True, autoincrement=True)
    nume_judet = Column(String(100), unique=True, nullable=False)
    localitati = relationship("Localitate", back_populates="judet", cascade="all, delete-orphan")
    
class Localitate(Base):
    __tablename__ = 'localitati'

    id_localitate = Column(Integer, primary_key=True, autoincrement=True)
    id_judet = Column(Integer, ForeignKey('judete.id_judet'), nullable=False)
    nume_localitate = Column(String(100), nullable=False)

    judet = relationship("Judet", back_populates="localitati")
    anunturi = relationship("Anunt", back_populates="localitate")

class TipImobil(Base):
    __tablename__ = 'tipuri_imobil'

    id_tip_imobiliar = Column(Integer, primary_key=True, autoincrement=True)
    nume_tip = Column(String(50), unique=True, nullable=False)
    anunturi = relationship("Anunt", back_populates="tip_imobiliar")

class TipTranzactie(Base):
    __tablename__ = 'tipuri_tranzactie'

    id_tip_tranzactie = Column(Integer, primary_key=True, autoincrement=True)
    nume_tranzactie = Column(String(50), unique=True, nullable=False)
    anunturi = relationship("Anunt", back_populates="tip_tranzactie")
    
class PerioadaAnConstructie(Base):
    __tablename__ = 'perioada_an_constructie'

    id_an_constructie = Column(Integer, primary_key=True, autoincrement=True)
    perioada_constructie = Column(String(100), unique=True, nullable=False)
    anunturi = relationship("Anunt", back_populates="perioada_ref")
    
class Anunt(Base):
    __tablename__ = 'anunturi'

    id_anunt = Column(Integer, primary_key=True, autoincrement=True)
    
    # Chei Externe
    id_localitate = Column(Integer, ForeignKey('localitati.id_localitate'), nullable=False)
    id_tip_imobiliar = Column(Integer, ForeignKey('tipuri_imobil.id_tip_imobiliar'))
    id_tip_tranzactie = Column(Integer, ForeignKey('tipuri_tranzactie.id_tip_tranzactie'))
    id_perioada_constructie = Column(Integer, ForeignKey('perioada_an_constructie.id_an_constructie'))
    
    # Atribute
    suprafata = Column(Integer)
    etaj = Column(String(100))
    an_constructie = Column(String(100)) # Valoarea brută (ex: "2020")
    compartimentare = Column(String(100))
    pret = Column(Integer)
    data_publicare = Column(Date)
    id_sursa_raw = Column(String(100), ForeignKey('raw_data.id_raw'))

    # Relații (Dependențele)
    localitate = relationship("Localitate", back_populates="anunturi")
    tip_imobiliar = relationship("TipImobil", back_populates="anunturi")
    tip_tranzactie = relationship("TipTranzactie", back_populates="anunturi")
    perioada_ref = relationship("PerioadaAnConstructie", back_populates="anunturi")
    sursa_raw = relationship("Estate")