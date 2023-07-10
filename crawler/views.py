from django.shortcuts import render
from django.http import JsonResponse
from linkedin_scraper import Person, actions
from selenium import webdriver

import json

from linkedin_scraper.profileCollector import ProfileCollector

def crawlers(request):
    driver = webdriver.Chrome()

    email = "shubhamjobanputra@gmail.com"
    password = "!0x7PW5!#L5%"
    actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
    # person = Person("https://www.linkedin.com/in/veena-siddaraju-68813b225", driver=driver,close_on_complete=True)
    
    search_criteria = {
        'keywords': 'BMC Remedy',
        'geoUrn': ['100811329']
    }
    
    urls = ProfileCollector(search_criteria=search_criteria,driver=driver,max_page=100)
    
    # data = person_to_json(person)
    # data = person_to_json(urls)
    # return JsonResponse(data, safe=False)
    return JsonResponse(urls.to_json(), safe=False)

def person_to_json(person):
    """Converts a Person object to JSON.

    Args:
    person: The Person object to convert.

    Returns:
    A JSON representation of the Person object.
    """

    data = {}
    data["linkedin_url"] = person.linkedin_url
    data["name"] = person.name
    data["about"] = person.about
    data["experiences"] = [experience.to_json() for experience in person.experiences]
    data["educations"] = [education.to_json() for education in person.educations]
    data["interests"] = [interest.to_json() for interest in person.interests]
    data["accomplishments"] = [accomplishment.to_json() for accomplishment in person.accomplishments]
    data["also_viewed_urls"] = person.also_viewed_urls
    data["contacts"] = [contact.to_json() for contact in person.contacts]

    return data