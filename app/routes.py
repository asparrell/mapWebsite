from app import app
from flask import render_template
import folium
import os
import sys

@app.route('/')
@app.route('/index')
def index():
    m = folium.Map(min_zoom=2, max_zoom=14, zoom_start=2)
    filenames = get_filenames()
    for file in filenames:
        marker = make_marker(file)
        marker.add_to(m)
    #folium.Marker([42.4709, -70.9176], popup='<i>Ralphy Baby Lives Here!!</i>', tooltip="Click Me!").add_to(m)
    m.save('./app/templates/map.html')
    return render_template('index.html', title='Map Home')

place_code_to_lat_long = {'2.1.1.2': [53.726669, -127.647621], '2.1.1.8': [51.253777, -85.323212]}


def get_filenames() -> list:
    # List all files in the rock_art_files directory
    filenames = []
    basepath = '/home/ubuntu/rock_art_files/'
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            filenames.append(entry)
    return filenames

def extract_location() -> dict:
    # Get latlong coordinates from filename for each file
    filenames = get_filenames()
    filename_to_latlong = {}
    for name in filenames:
        # this indexing won't work for files that have two-digit numbers in the code
        latlong = place_code_to_lat_long[name[:7]]
        filename_to_latlong[name] = latlong
    return filename_to_latlong
            
def make_marker(filename: str):
    # return a Marker object with the properties of a file
    latlong_dict = extract_location()
    location = latlong_dict[filename[:7]]
    name = filename[:-5]
    marker = folium.Marker(location, popup=name, tooltip='site name, derived from separate location')

    return marker

# print("", file=sys.stderr)
