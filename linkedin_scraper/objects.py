from dataclasses import dataclass
from time import sleep

from selenium.webdriver import Chrome

from . import constants as c

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json 

@dataclass
class Contact:
    name: str = None
    occupation: str = None
    url: str = None
    
    def to_json(self):
        """Converts the experience to JSON."""
        data = {}
        data["name"] = self.name
        data["occupation"] = self.occupation
        data["url"] = self.url
        
        return data


@dataclass
class Institution:
    institution_name: str = None
    linkedin_url: str = None
    website: str = None
    industry: str = None
    type: str = None
    headquarters: str = None
    company_size: int = None
    founded: int = None
    
    def to_json(self):
        """Converts the experience to JSON."""
        data = {}
        data["institution_name"] = self.institution_name
        data["linkedin_url"] = self.linkedin_url
        data["website"] = self.website
        data["industry"] = self.industry
        data["type"] = self.type
        data["headquarters"] = self.headquarters
        data["company_size"] = self.company_size
        data["founded"] = self.founded

        return data

@dataclass
class Experience(Institution):
    from_date: str = None
    to_date: str = None
    description: str = None
    position_title: str = None
    duration: str = None
    location: str = None
    
    def to_json(self):
        """Converts the experience to JSON."""
        data = {}
        data["from_date"] = self.from_date
        data["to_date"] = self.to_date
        data["description"] = self.description
        data["position_title"] = self.position_title
        data["duration"] = self.duration
        data["location"] = self.location
        
        return data


@dataclass
class Education(Institution):
    from_date: str = None
    to_date: str = None
    description: str = None
    degree: str = None
    
    def to_json(self):
        """Converts the experience to JSON."""
        data = {}
        data["from_date"] = self.from_date
        data["to_date"] = self.to_date
        data["description"] = self.description
        data["degree"] = self.degree

        return data

@dataclass
class Interest(Institution):
    title = None
    
    def to_json(self):
        """Converts the experience to JSON."""
        data = {}
        data["title"] = self.title
        
        return data

@dataclass
class Accomplishment(Institution):
    category = None
    title = None

    def to_json(self):
        """Converts the experience to JSON."""
        data = {}
        data["title"] = self.title
        data["category"] = self.category
        
        return data

@dataclass
class Scraper:
    driver: Chrome = None
    WAIT_FOR_ELEMENT_TIMEOUT = 5
    TOP_CARD = "pv-top-card"

    def to_json(self):
        """Converts the scraper to JSON."""
        data = {}
        data["driver"] = self.driver
        data["wait_for_element_timeout"] = self.wait_for_element_timeout
        data["top_card"] = self.top_card

        return data

    @staticmethod
    def wait(duration):
        sleep(int(duration))

    def focus(self):
        self.driver.execute_script('alert("Focus window")')
        self.driver.switch_to.alert.accept()

    def mouse_click(self, elem):
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(elem).perform()

    def wait_for_element_to_load(self, by=By.CLASS_NAME, name="pv-top-card", base=None):
        base = base or self.driver
        return WebDriverWait(base, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    by,
                    name
                )
            )
        )

    def wait_for_all_elements_to_load(self, by=By.CLASS_NAME, name="pv-top-card", base=None):
        base = base or self.driver
        return WebDriverWait(base, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_all_elements_located(
                (
                    by,
                    name
                )
            )
        )


    def is_signed_in(self):
        try:
            WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        c.VERIFY_LOGIN_ID,
                    )
                )
            )

            self.driver.find_element(By.CLASS_NAME, c.VERIFY_LOGIN_ID)
            return True
        except Exception as e:
            pass
        return False

    def scroll_to_half(self):
        self.driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def scroll_class_name_element_to_page_percent(self, class_name:str, page_percent:float):
        self.driver.execute_script(
            f'elem = document.getElementsByClassName("{class_name}")[0]; elem.scrollTo(0, elem.scrollHeight*{str(page_percent)});'
        )

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element(By.CLASS_NAME, class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element(By.XPATH,tag_name)
            return True
        except:
            pass
        return False

    def __find_enabled_element_by_xpath__(self, tag_name):
        try:
            elem = self.driver.find_element(By.XPATH,tag_name)
            return elem.is_enabled()
        except:
            pass
        return False

    @classmethod
    def __find_first_available_element__(cls, *args):
        for elem in args:
            if elem:
                return elem[0]
