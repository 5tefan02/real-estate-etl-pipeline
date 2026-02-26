from Database.nomalize_db import normalize_db
from Scraping.scraper_OLX import scrape_olx
from Scraping.scraper_imobiliarero import scrape_imobiliarero
from Database.insert_estates import insert_estates
from Database.db_manager import engine, Base
import Database.db_tabels as db_tabels

def main():
    Base.metadata.create_all(bind=engine)
    
    rezultate_olx = scrape_olx()

    if rezultate_olx:
        insert_estates(rezultate_olx)
        print(f"{len(rezultate_olx)} rezultate inserate in baza de date.")
    else:
        print("Niciun rezultat de inserat")

    scrape_imobiliarero()


if __name__ == "__main__":
    main()
