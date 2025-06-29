import scrapy
from scrapy import Spider, Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin
import time
import re

class WeddingSpotSeleniumSpider(Spider):
    name = "wedding_venues"
    allowed_domains = ["wedding-spot.com"]

    base_url = (
        "https://www.wedding-spot.com/wedding-venues/"
        "?pr=new%20jersey"
        "&r=new%20jersey%3anorth%20jersey"
        "&r=new%20jersey%3aatlantic%20city"
        "&r=new%20jersey%3ajersey%20shore"
        "&r=new%20jersey%3asouth%20jersey"
        "&r=new%20jersey%3acentral%20jersey"
        "&r=new%20york%3along%20island"
        "&r=new%20york%3amanhattan"
        "&r=new%20york%3abrooklyn"
        "&r=pennsylvania%3aphiladelphia"
    )
    max_pages = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def start_requests(self):
        self.driver.get(self.base_url)
        current_page = 1

        while current_page <= self.max_pages: #this is just condition for scraping 5 pages as mentioned in the requirement
            time.sleep(3)  # to wait for the content loading

            sel = Selector(text=self.driver.page_source)
            venue_links = sel.css('a::attr(href)').getall()
            venue_links = {url for url in venue_links if url.startswith('/venue/')}

            if not venue_links:
                self.logger.info(f"No venues found on page {current_page}. Stopping.")
                break

            for link in venue_links:
                full_url = urljoin(self.base_url, link)
                yield scrapy.Request(full_url, callback=self.parse_venue)

            try:
                # Using Selenium to handle the 'Next Page' 
                next_button = self.driver.find_element("xpath", '//button[@aria-label="Next Page"]')
                next_button.click()
                current_page += 1 #tracking pages scraped to limit the pages to 5
                time.sleep(3)
            except NoSuchElementException:
                self.logger.info("No more pages or Next button not found.")
                break


        self.driver.quit()

    def parse_venue(self, response):

        #for extracting highlights
        highlights = response.css('div.VenueHighlights--label::text').getall()
        unique_highlights = list(dict.fromkeys(highlights))

        #for extracting guest capacity
        descriptions = response.css('p.VenuePage--detail-description::text').getall()
        guest_capacity_text = next((d for d in descriptions if 'Accommodates' in d), None)

        guest_capacity = None
        if guest_capacity_text:
            match = re.search(r'(\d+)', guest_capacity_text)
            if match:
                guest_capacity = int(match.group(1))


        #for extracting the venue address
        location_div = response.css('div.VenuePage--detail:nth-of-type(4) p.VenuePage--detail-description')
        street = location_div.xpath('text()').get()
        city_state_zip = location_div.css('span::text').get()

        if street and city_state_zip:
            address = f"{street.strip()}, {city_state_zip.strip()}"
        else:
            address = None


        #for extracting phone number (in some there were none), I have left the extention no. in some as it is since it might be of help
        phone_raw = response.css('span.SecondaryCTA--hidden::text').get()
        phone = phone_raw.strip() if phone_raw else None

        #for venue name
        venue_name = response.css('h1.SecondaryCTA--venueName::text').get()

        yield {
            'URL': response.url,
            'Venue Name': venue_name,
            'Phone': phone,
            'Venue Highlights': unique_highlights,
            'Guest Capacity': guest_capacity,
            'Address': address,
        }
