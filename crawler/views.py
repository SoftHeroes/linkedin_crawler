from django.shortcuts import render
from django.http import JsonResponse
from linkedin_scraper import Person, actions
from selenium import webdriver

import json

def crawlers(request):
    driver = webdriver.Chrome()

    email = "shubhamjobanputra@gmail.com"
    password = "!0x7PW5!#L5%"
    actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
    person = Person("https://www.linkedin.com/in/veena-siddaraju-68813b225", driver=driver,close_on_complete=True)
    
    data = person_to_json(person)
    
    return JsonResponse(data, safe=False)

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