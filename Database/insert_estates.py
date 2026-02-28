from Database.db_tabels import Estate
from Database.db_manager import SessionLocal


def insert_estates(rezultate: list[dict]):
    session = SessionLocal()

    try:
        objects = [
            Estate(
                id_raw=r["id_raw"],
                URL_anunt=r["URL_anunt"],
                judet=r["judet"],
                oras=r["oras"],
                suprafata=r["suprafata"],
                etaj=r["etaj"],
                perioada_constructie=r.get("perioada_constructie"),
                an_constructie=r["an_constructie"],
                compartimentare=r.get("compartimentare"),
                camere=r.get("camere"),
                tip_tranzactie=r["tip_tranzactie"],
                tip_imobiliar=r["tip_imobiliar"],
                platforma=r["platforma"],
                pret=r["pret"],
                data=r["data"],
                processed=r["processed"])
            for r in rezultate
        ]

        session.add_all(objects)
        session.commit()
        print(f"[DB] Inserate {len(objects)} inregistrari")

    except Exception as e:
        session.rollback()
        print("[DB] Eroare la insert:", e)
        raise

    finally:
        session.close()
        