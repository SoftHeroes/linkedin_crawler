import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
from .objects import Scraper

class ProfileCollector(Scraper):
    def __init__(
        self,
        search_criteria=None,
        max_page=100,
        driver=None,
        get=True,
        scrape=True,
    ):
        self.search_criteria = search_criteria
        self.profile_urls = []
        self.max_page = max_page

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(self.generate_search_url(search_criteria))

        self.driver = driver

        if scrape:
            self.scrape()

    def generate_search_url(self, search_criteria, page=1):
        base_url = "https://www.linkedin.com/search/results/people/"
        search_criteria['page'] = page
        query_params = urlencode(search_criteria, safe='')
        search_url = f"{base_url}?{query_params}"
        return search_url

    def generate_next_page_url(self, current_page):
        next_page = current_page + 1
        if next_page <= self.max_page:
            return self.generate_search_url(self.search_criteria, next_page)
        else:
            return None
        
    def scrape(self):
        current_page = 1
        while current_page <= self.max_page:
            search_url = self.generate_search_url(self.search_criteria, current_page).replace('%27', '"')
            self.driver.get(search_url)
            sleep(3)  # Wait for the page to load

            entity_results = self.driver.find_elements(By.CSS_SELECTOR, '.entity-result[data-chameleon-result-urn]')
            for entity_result in entity_results:
                universal_image_div = entity_result.find_element(By.CSS_SELECTOR, '.entity-result__universal-image')
                profile_element = universal_image_div.find_element(By.TAG_NAME, 'a')
                profile_url = profile_element.get_attribute('href')
                self.profile_urls.append(profile_url)

            next_page_url = self.generate_next_page_url(current_page)
            if next_page_url is None:
                break

            self.driver.get(next_page_url)
            sleep(3)  # Wait for the next page to load
            current_page += 1

        return self.profile_urls
    
    def to_json(self):
        """Converts the experience to JSON."""
        data = {}
        data["profile_urls"] = self.profile_urls
                
        return data
