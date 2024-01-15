import os
import logging
import pandas as pd
import plotly.graph_objects as go
import textwrap
import sys
sys.path.append("../")
import dataprep.prepare as dp


def fig():
    cs, latx, longx, name, desc = [], [], [], [], []
    holidays = dp.get_public_holidays()
    api_key = os.getenv("OPENAI_API_KEY")
    logging.info(f"Retrieved {len(holidays)} results")
    for i in holidays:
        country = i['countryCode']
        holiday_name = i['name']
        date = i['date']
        country_long, lat, long = dp.get_lat_long(country)
        if api_key is None:
            logging.warning("Ensure to set your OpenAI API Key in order to retrieve extra information about each holiday.")
            description = ""
        else:
            description = dp.check_openai(holiday_name, country_long, api_key)
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
