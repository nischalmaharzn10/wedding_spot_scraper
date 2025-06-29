# Wedding Venue Scraper

## Task

Scrape venue details from [Wedding Spot](https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1), visiting each venue’s detail page and extracting specific fields across 4–5 listing pages.

## Extracted Fields

- URL  
- Venue Name  
- Phone  
- Venue Highlights  
- Guest Capacity  
- Address  

## Tech Stack

- [Scrapy](https://scrapy.org/)
- [Selenium](https://www.selenium.dev/)
- Python

## How to Set Up

1. **Clone the repository**
   
2. **Create a virtual env**
    - python -m venv venv
    - source venv/bin/activate   # on Linux/macOS
    - venv\Scripts\activate      # on Windows
   
3. **Install dependencies**
    - pip install -r requirements.txt

4. **Run the spider**
    - scrapy crawl wedding_venues -o venues.csv

5. **Notes**
   - The scraper uses Selenium to handle JavaScript-rendered pagination.
   - It follows the "Next Page" button instead of hardcoding pagination.
   - The project captures 5 pages of venue listings as mentioned in requirements.
