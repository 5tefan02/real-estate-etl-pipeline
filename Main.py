from Scraping.scraper_OLX import scrape_olx
from Database.db_manager import insert_estates

def main():
    rezultate = scrape_olx()

    if rezultate:
        insert_estates(rezultate)
        print(f"{len(rezultate)} rezultate inserate in baza de date.")
    else:
        print("Niciun rezultat de inserat")


if __name__ == "__main__":
    main()
