import os
from django.shortcuts import render
from django.http import JsonResponse
from linkedin_scraper import Person, actions
from selenium import webdriver

import json

from linkedin_scraper.profileCollector import ProfileCollector

# Dumbo Details
# email = "veenasiddaraju98@gmail.com"
# password = "Zade@1997"

# My Details
# email = "shubhamjobanputra@gmail.com"
# password = "!0x7PW5!#L5%"

# My Details
email = "softheroes.sh@gmail.com"
password = "Test123!"

profile_file = "jsons/profiles.json"

search_criteria = {
    'keywords': 'BMC Remedy',
    'geoUrn': '["100811329"]'
}

def crawl_profiles(request):
    driver = webdriver.Chrome()
    
    actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
    # person = Person("https://www.linkedin.com/in/veena-siddaraju-68813b225", driver=driver,close_on_complete=True)
    
    # search_criteria = {
    #     'keywords': 'bmc remedy',
    #     'geoUrn': '["115918471","106187582","102106636","104869687","106442238"]'
    # }
    
    urls = ProfileCollector(search_criteria=search_criteria,driver=driver,max_page=1)
    
    save_dict_to_json(urls.to_json(),profile_file)
    
    # data = person_to_json(person)
    # data = person_to_json(urls)
    # return JsonResponse(data, safe=False)
    return JsonResponse({'message':'profile stored successfully!'}, safe=False)

def crawl_peoples(request):
    driver = webdriver.Chrome()

    actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
    
    existing_data = load_dict_from_json(profile_file)  # Load existing data from JSON file    
    
    # persons = []
    # for each_profile in existing_data['profile_urls']:
    #     if not each_profile['crawled']:
    #         person = Person(each_profile['profile_url'], driver=driver,close_on_complete=True)
    #         persons.append(person_to_json(person))
    urls = [profile["profile_url"] for profile in existing_data["profile_urls"]];
    person_object = Person('',linkedin_urls=urls, driver=driver,close_on_complete=True)
    
    return JsonResponse(person_object.profile_details, safe=False)
    # return JsonResponse({'message':'people stored successfully!'}, safe=False)

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