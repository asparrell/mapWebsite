from app import app
from flask import render_template
import folium
import mammoth
import os
import sys

@app.route('/')
@app.route('/index')
def index():
    m = folium.Map(min_zoom=2, max_zoom=14, zoom_start=2)
    marker_list = []
    filenames = get_filenames()
    for file in filenames:
        marker = make_marker(file)
        if marker.location in marker_list:
            # will need to change the next two lines to reflect new data
            filename_to_latlong = extract_location()
            location = filename_to_latlong[file]
            location[0] += 0.1  # will lessen this increment
            location[1] += 0.1
            name = file[:-5]
            marker = folium.Marker(location, popup=name, tooltip=name)
        marker_list.append(marker.location)
        marker.add_to(m)
    m.save('./app/templates/map.html')

    return render_template('index.html', title='Map Home')

place_code_to_lat_long = {'2.1.1.1': [55.017001, -114.930192], '2.1.1.2': [55.268163, -124.945342], '2.1.1.4': [55.079546, -97.449267], '2.1.1.7': [45.067580, -63.157430], '2.1.1.10': [51.253777, -85.323212], '2.1.1.13': [54.588975, -105.862449], '2.2.5.0': [18.928371, -70.384653]}


def get_filenames() -> list:
    # List all files in the rock_art_files directory; will have to sort by .html
    filenames = []
    basepath = '/home/ubuntu/rock_art_files/'
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            filenames.append(entry)
    return filenames

def extract_location() -> dict:
    # Get latlong coordinates from filename for each file
    # will replace this with new extract_location()
    filenames = get_filenames()
    filename_to_latlong = {}
    for file in filenames:
        file_code = file[:file.find(' ')]
        latlong = place_code_to_lat_long[file_code]
        filename_to_latlong[file] = latlong
    return filename_to_latlong

def make_marker(filename: str):
    # return a Marker object with the properties of a file
    # file_to_coords = make_file_to_coord_dict()
    # location = file_to_coords[filename]
    # will comment out the next two lines
    filename_to_latlong = extract_location()
    location = filename_to_latlong[filename]
    name = filename[:-5]
    marker = folium.Marker(location, popup=name, tooltip=name)

    return marker


# print("", file=sys.stderr)
