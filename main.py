from dash import Dash, dcc, html
from geopy.geocoders import Nominatim
import json
import openai
import os
import pandas as pd
import plotly.graph_objects as go
import requests
import textwrap
import logging

logging.basicConfig(level=logging.INFO)

with open('countries.json') as json_file:
   json_data = json.load(json_file)

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

def check_openai(holiday, country):
    logging.info(f"Getting information about the {holiday} from {country}")
    completion = openai.ChatCompletion.create(
       model="gpt-3.5-turbo",
       messages=[
            {"role": "system", "content": "You are an information guide on various countries public holidays. DO NOT OUTPUT THE DATE. I am interested in purely information about the holiday and it's significance. Your output should not be longer than 2 sentences. DO NOT OUTPUT THE DATE."},
            {"role": "user", "content": f"I want information about the {holiday} holiday from {country}, please do not output the date of the holiday."}
       ])
    result = completion.choices[0].message.content
    return result

def get_public_holidays():
    logging.info(f"Retrieving list of public holidays from Nager.Date")
    return requests.get("https://date.nager.at/api/v3/NextPublicHolidaysWorldwide").json()

def get_lat_long(country):
    element = next((item for item in json_data if item["CountryCode"] == country), None)
    return element["CountryName"], element["CapitalLatitude"], element["CapitalLongitude"]

def fig():
    cs, latx, longx, name, desc = [], [], [], [], []
    holidays = get_public_holidays()
    logging.info(f"Retrieved {len(holidays)} results")
    for i in holidays:
        country = i['countryCode']
        holiday_name = i['name']
        date = i['date']
        country_long, lat, long = get_lat_long(country)
        if openai.organization == openai.api_key:
            logging.warning("Ensure to set your OpenAI API Key in order to retrieve extra information about each holiday.")
            description = ""
        else:
            description = check_openai(holiday_name, country_long)
        logging.info(f"Successfully retrieved information about {holiday_name} from {country_long}")
        description = textwrap.fill(description, 40).replace("\n", "<br>")
        cs.append(country_long)
        name.append(holiday_name)
        latx.append(lat)
        longx.append(long)
        desc.append(description)

    df = pd.DataFrame(
       {
           "cnt": cs,
           "date": date,
           "lat": latx,
           "long": longx,
           "holiday": name,
           "desc": desc
       }
    )

    df['text'] = "Date: "+df['date']+"<br>" + "Country: "+df['cnt']+"<br>" + "Holiday: "+df['holiday']+"<br><br>"+df['desc']
    
    fig = go.Figure(data=go.Scattergeo(
        lon = df['long'],
        lat = df['lat'],
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = "x-open-dot",
            line = dict(
                width=2,
                color='rgba(102, 102, 102)'
            ),
            color = "rgba(40, 44, 52)",
        )))
      
    fig.update_geos(
       resolution=110,
       showcoastlines=True,
       showcountries=True,
       showland=True,
       showocean=False,
       showlakes=False,
       showrivers=False
    )
    fig.update_layout(
        height=800, 
        margin={"r":0,"t":0,"l":0,"b":0},
        title='<br><br>Public Holidays around the World<br>(Hover for additional information)'
        )
    return fig


app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig())
])

if __name__ == '__main__':
 app.run_server(debug=True, host="0.0.0.0", port=8050, use_reloader=False)
