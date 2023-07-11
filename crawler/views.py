import os
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
    
    urls = ProfileCollector(search_criteria=search_criteria,driver=driver,max_page=2)
    
    save_dict_to_json(urls.to_json(),'jsons/profiles.json')
    
    # data = person_to_json(person)
    # data = person_to_json(urls)
    # return JsonResponse(data, safe=False)
    return JsonResponse({'message':'profile stored successfully!'}, safe=False)

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

def save_dict_to_json(data, file_path):
    """
    Saves a dictionary to a JSON file, checking for existing profile URLs.
    """
    existing_data = load_dict_from_json(file_path)  # Load existing data from JSON file

    # Check if the file exists
    if not os.path.isfile(file_path):
        # Create the directory if it doesn't exist
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)

        existing_data = data  # Use the provided data as the initial content

    # Extract the list of profile URLs from existing data
    existing_urls = [item['profile_url'] for item in existing_data.get('profile_urls', [])]

    for item in data.get('profile_urls', []):
        profile_url = item['profile_url']

        if profile_url not in existing_urls:
            existing_data.setdefault('profile_urls', []).append(item)

    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file)


def load_dict_from_json(file_path):
    """
    Loads a dictionary from a JSON file, handling file not found gracefully.
    """
    if not os.path.isfile(file_path):
        # Return an empty dictionary if the file is not found
        return {'profile_urls':[]}
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data