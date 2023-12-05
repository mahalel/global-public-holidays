import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pysnooper
import json
from geopy.geocoders import Nominatim

countries = {
"AD":"Andorra",
"AL":"Albania",
"AR":"Argentina",
"AT":"Austria",
"AU":"Australia",
"AX":"Åland Islands",
"BA":"Bosnia and Herzegovina",
"BB":"Barbados",
"BE":"Belgium",
"BG":"Bulgaria",
"BJ":"Benin",
"BO":"Bolivia",
"BR":"Brazil",
"BS":"Bahamas",
"BW":"Botswana",
"BY":"Belarus",
"BZ":"Belize",
"CA":"Canada",
"CH":"Switzerland",
"CL":"Chile",
"CN":"China",
"CO":"Colombia",
"CR":"Costa Rica",
"CU":"Cuba",
"CY":"Cyprus",
"CZ":"Czechia",
"DE":"Germany",
"DK":"Denmark",
"DO":"Dominican Republic",
"EC":"Ecuador",
"EE":"Estonia",
"EG":"Egypt",
"ES":"Spain",
"FI":"Finland",
"FO":"Faroe Islands",
"FR":"France",
"GA":"Gabon",
"GB":"United Kingdom",
"GD":"Grenada",
"GG":"Guernsey",
"GI":"Gibraltar",
"GL":"Greenland",
"GM":"Gambia",
"GR":"Greece",
"GT":"Guatemala",
"GY":"Guyana",
"HN":"Honduras",
"HR":"Croatia",
"HT":"Haiti",
"HU":"Hungary",
"ID":"Indonesia",
"IE":"Ireland",
"IM":"Isle of Man",
"IS":"Iceland",
"IT":"Italy",
"JE":"Jersey",
"JM":"Jamaica",
"JP":"Japan",
"KR":"South Korea",
"LI":"Liechtenstein",
"LS":"Lesotho",
"LT":"Lithuania",
"LU":"Luxembourg",
"LV":"Latvia",
"MA":"Morocco",
"MC":"Monaco",
"MD":"Moldova",
"ME":"Montenegro",
"MG":"Madagascar",
"MK":"North Macedonia",
"MN":"Mongolia",
"MS":"Montserrat",
"MT":"Malta",
"MX":"Mexico",
"MZ":"Mozambique",
"NA":"Namibia",
"NE":"Niger",
"NG":"Nigeria",
"NI":"Nicaragua",
"NL":"Netherlands",
"NO":"Norway",
"NZ":"New Zealand",
"PA":"Panama",
"PE":"Peru",
"PG":"Papua New Guinea",
"PL":"Poland",
"PR":"Puerto Rico",
"PT":"Portugal",
"PY":"Paraguay",
"RO":"Romania",
"RS":"Serbia",
"RU":"Russia",
"SE":"Sweden",
"SG":"Singapore",
"SI":"Slovenia",
"SJ":"Svalbard and Jan Mayen",
"SK":"Slovakia",
"SM":"San Marino",
"SR":"Suriname",
"SV":"El Salvador",
"TN":"Tunisia",
"TR":"Turkey",
"UA":"Ukraine",
"US":"United States",
"UY":"Uruguay",
"VA":"Vatican City",
"VE":"Venezuela",
"VN":"Vietnam",
"ZA":"South Africa",
"ZW":"Zimbabwe",
}

def get_public_holidays():
    return requests.get("https://date.nager.at/api/v3/NextPublicHolidaysWorldwide").json()

# @pysnooper.snoop()
def get_lat_long(country):
    geolocator = Nominatim(user_agent="testing-andrei")
    location = geolocator.geocode(country)
    return location.latitude, location.longitude




@pysnooper.snoop()
def main():
    cs = []
    latx = []
    longx = []
    name = []
    holidays = get_public_holidays()
    for i in holidays[0:2]:
        country = countries[i['countryCode']]
        holiday_name = i['name']
        lat, long = get_lat_long(country)
        cs.append(country)
        name.append(holiday_name)
        latx.append(lat)
        longx.append(long)

    df = pd.DataFrame(
       {
           "cnt": cs,
           "lat": latx,
           "long": longx,
           "holiday": name
           # "Custom": ["test1", "test2"]
       }
    )

    df['text'] = df['cnt'] + " " + df['holiday']
    # fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', hover_name='Country', color="Country", text="Country", symbol="Holiday", custom_data="Custom", projection="natural earth2")
    
    fig = go.Figure(data=go.Scattergeo(
        # locationmode = 'USA-states',
        lon = df['long'],
        lat = df['lat'],
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=2,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'Blues',
            cmin = 0,
            color = "rgba(40, 44, 52)",
            # cmax = df['cnt'].max(),
            # colorbar_title="Incoming flights<br>February 2011"
        )))
    
    
    fig.show()

main()