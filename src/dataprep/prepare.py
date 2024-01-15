import logging
from openai import OpenAI
import requests
import json

'''
Retrieve information from OpenAI about public holiday
'''
def check_openai(holiday, country, api_key):
    logging.info(f"Getting information about the {holiday} from {country}")
    client = OpenAI(api_key=api_key)
    chat_completion = client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[
            {"role": "system", "content": "You are an information guide on various countries public holidays. DO NOT OUTPUT THE DATE. I am interested in purely information about the holiday and it's significance. Your output should not be longer than 2 sentences. DO NOT OUTPUT THE DATE."},
            {"role": "user", "content": f"I want information about the {holiday} holiday from {country}, please do not output the date of the holiday."}
       ])
    result = chat_completion.choices[0].message.content
    return result


'''
Retrieve list of public holidays from Nager API
'''
def get_public_holidays():
    logging.info(f"Retrieving list of public holidays from Nager.Date")
    return requests.get("https://date.nager.at/api/v3/NextPublicHolidaysWorldwide").json()


with open('countries.json') as json_file:
   json_data = json.load(json_file)

'''
Create a list of coordinates for the countries with a public holiday
'''
def get_lat_long(country):
    logging.info(f"Getting LAT & LONG for {country}")
    element = next((item for item in json_data if item["CountryCode"] == country), None)
    return element["CountryName"], element["CapitalLatitude"], element["CapitalLongitude"]


