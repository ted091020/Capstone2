from tkinter import *
import pandas as pd
import numpy as numpy
import folium
import json
from branca.colormap import linear
import os
import webbrowser

############ Load Data #########

filepath = os.path.join(r'C:\Users\Evan\Desktop\Capstone 2\Data\Final Data\zip_codes_final.geojson')
filepath2 = os.path.join(r'C:\Users\mdegr\Downloads\Capstone2-master\Capstone2-master\Data\Final Data\zip_codes_final.geojson')
with open(filepath2) as zip_codes:
    zip_data = json.load(zip_codes)

rest_file = r'C:\Users\Evan\Desktop\Capstone 2\Data\Final Data\restaurants_final.csv'
rest_file2 = r'C:\Users\mdegr\Downloads\Capstone2-master\Capstone2-master\Data\Final Data\restaurants_final.csv'

restaurant_data = pd.read_csv(rest_file2, index_col='Unnamed: 0')

# Remove the decimal and convert postal code to string
restaurant_data['postalcode'] = restaurant_data['postalcode'].astype('int')
restaurant_data['postalcode'] = restaurant_data['postalcode'].astype('str')

############ Functions Here ##########

def recommend_zips(json, data, cuisine, age_group):
    '''Displays a chorpleth map colored based on the best opportunity to open a new restaurant'''
    
    # Calculate the cuisine metric
    data[cuisine+'_metric'] = (data['population_scaled'] + data['med_income_scaled'] + data['RPC_scaled'] + (1-data[cuisine]) + data[age_group+'_scaled']) * 20
    
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
    t.save(r'C:\Users\mdegr\Downloads\Capstone2-master\Capstone2-master\map.html')
    # Open the map in browser
    webbrowser.open_new_tab(r'C:\Users\mdegr\Downloads\Capstone2-master\Capstone2-master\map.html')
    


def myClick():
	cuisine = selected_cuisine.get()
	age_group = selected_age.get()
	recommend_zips(json=zip_data, data=restaurant_data, cuisine=cuisine, age_group=age_group)


########## GUI Stuff ###########

#Create main window
root = Tk()
root.geometry('500x200')

# Create labels
cuisine_label = Label(root, text='Choose your cuisine').grid(row=0, column=0)
age_label = Label(root, text='Choose your target age group').grid(row=0, column=2)

# Create dropdown menus
selected_cuisine = StringVar()
selected_age = StringVar()

cuisine_drop = OptionMenu(root, selected_cuisine, "Italian", 'Chinese', 'American').grid(row=1, column=0)
age_drop = OptionMenu(root, selected_age, '0-14', '15-29', '30-54', '55+').grid(row=1, column=2)




# Create button to generate map
generate_button = Button(root, text='Generate Map!', padx=50, command=myClick).grid(row=2, column=1)

#MainLoop

root.mainloop()