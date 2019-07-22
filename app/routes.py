from app import app
from flask import render_template
import folium
import os
import sys

@app.route('/')
@app.route('/index')
def index():
    m = folium.Map(min_zoom=2, max_zoom=14, zoom_start=2)
    make_marker()
    #folium.Marker([42.4709, -70.9176], popup='<i>Ralphy Baby Lives Here!!</i>', tooltip="Click Me!").add_to(m)
    m.save('./app/templates/map.html')
    return render_template('index.html', title='Map Home')

place_code_to_lat_long = {'2.1.1.2': [53.726669, -127.647621], '2.1.1.8': [51.253777, -85.323212]}


def get_filenames() -> list:
    # List all files in a directory using os.listdir
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
        if name[:7:2].isnumeric():
            latlong = place_code_to_lat_long[name[:7]]
            latlong_list[name] = latlong
    return filename_to_latlong
            
def make_marker():
    latlong_dict = extract_location()
    for entry in latlong_dict:
        location = latlong_dict[entry]
        name = entry
        folium.Marker(location, popup=name, tooltip='site name, derived from separate location').add_to(m)


# file=sys.stderr
