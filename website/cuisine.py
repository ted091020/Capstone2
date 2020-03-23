from flask import Flask, render_template, url_for, send_file, request, redirect
import folium
import os
import json
from branca.colormap import linear
import pandas as pd
import numpy as np 
import time


app = Flask(__name__)

############ Load Data #########

filepath = os.path.join(r'C:\Users\Evan\Desktop\Capstone 2\Data\Final Data\zip_codes_final.geojson')

with open(filepath) as zip_codes:
    zip_data = json.load(zip_codes)

rest_file = r'C:\Users\Evan\Desktop\Capstone 2\Data\Final Data\restaurants_final.csv'
restaurant_data = pd.read_csv(rest_file, index_col='Unnamed: 0')

# Convert postalcode to string so it matches the json
restaurant_data['postalcode'] = restaurant_data['postalcode'].astype('int')
restaurant_data['postalcode'] = restaurant_data['postalcode'].astype('str')
restaurant_data['population'] = restaurant_data['population'].astype('int')
restaurant_data['med_income'] = restaurant_data['med_income'].astype('int')

############ Functions Here ##########

def recommend_zips(json, data, cuisine, age_group):
    '''Displays a chorpleth map colored based on the best opportunity to open a new restaurant'''
    
    # Calculate the cuisine metric
    data[cuisine+'_metric'] = np.round((data['population_scaled'] + data['med_income_scaled'] + data['RPC_scaled'] + (1-data[cuisine]) + data[age_group+'_scaled']) * 20, decimals=1)
    
    # Add the metric to the json
    # Create mapper dictionary
    mapper = pd.Series(data[cuisine+'_metric'].values, index=data['postalcode']).to_dict()
    # Add the metric to the json properties using the mapper (for the tooltip)
    for f in json['features']:
        f['properties'][cuisine+'_metric'] = mapper[f['properties']['postalcode']]
    
    # Create dictionary that determines the fill color
    cuisine_dict = data.set_index('postalcode')[cuisine+'_metric']

    # Generate map centered on New York
    t = folium.Map(
            location=[40.73942, -73.98160],
            zoom_start=10
    )

    # Set the colormap
    colormap = linear.YlGn_09.scale(
        data[cuisine+'_metric'].min(),
        data[cuisine+'_metric'].max())

    # Add the GeoJson layer
    folium.GeoJson(
                    json,
                    name=cuisine+' Metric',
                    style_function=lambda feature: {
                                                    'fillColor': colormap(cuisine_dict[feature['properties']['postalcode']]),
                                                    'color': 'black',
                                                    'weight': 1,
                                                    'dashArray': '1, 1',
                                                    'fillOpacity': 0.9
                                                    },
                    highlight_function=lambda x: {'weight':3, 'color':'black'},
                    tooltip=folium.features.GeoJsonTooltip(fields=['postalcode', cuisine+'_metric'],
                                                           aliases=['ZIP', 'Opportunity Metric'],
                                                           sticky=True,
                                                       
                                                        
                                                           )
    ).add_to(t)

    colormap.caption = cuisine+' Metric'
    colormap.add_to(t)

    # Save html file
    t.save(r'C:\Users\Evan\anaconda3\envs\cuisine\cuisine\static\metric_map.html')






######### FLASK HERE ###########

@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
def home():
	if request.method == "POST":
		cuisine = request.form.get('cuisine')
		age_group = request.form.get('age_group')
		recommend_zips(zip_data, restaurant_data, cuisine, age_group)
		top_10 = top_10 = restaurant_data.sort_values(by=cuisine+'_metric', ascending=False)[0:10].reset_index(drop=True).drop('index', axis=1)
		return render_template('home.html', current_time=int(time.time()), cuisine=cuisine, age_group=age_group, top_10=top_10)
	else:
		top_10 = pd.DataFrame()
		return render_template('home.html', top_10=top_10)

@app.route('/about')
def about():
	return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)