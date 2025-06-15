# run.py
import scraper
import generator

def main():
    scraper.main()        # or whatever function runs the scraping
    generator.main()      # generates HTML pages from scraped data

if __name__ == "__main__":
    main()
