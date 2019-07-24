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
            filename_to_latlong = extract_location()
            location = filename_to_latlong[filename]
            location[0] += 5
            location[1] += 5
            name = filename[:-5]            
            marker = folium.Marker(location, popup=name, tooltip='site name, derived from separate location')
        marker_list.append(marker.location)
        marker.add_to(m)
    m.save('./app/templates/map.html')
    print(marker_list)

    return render_template('index.html', title='Map Home')

place_code_to_lat_long = {'2.1.1.2': [53.726669, -127.647621], '2.1.1.8': [51.253777, -85.323212], '2.2.5.0': [18.928371, -70.384653]}


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
    for file in filenames:
        file_code = file[:file.find(' ')]
        latlong = place_code_to_lat_long[file_code]  # this indexing won't work for files that have two-digit numbers in the code
        filename_to_latlong[file] = latlong
    return filename_to_latlong

# def extract_filedata():
    #filenames = get_filenames()
    # for file in filenames:
        #file_obj = open(file)
        #html_file = mammoth.convert_to_html(file_obj)
        # print(html_file)

def make_marker(filename: str):
    # return a Marker object with the properties of a file
    filename_to_latlong = extract_location()
    location = filename_to_latlong[filename]
    name = filename[:-5]
    marker = folium.Marker(location, popup=name, tooltip='site name, derived from separate location')

    return marker

# extract_filedata()

# print("", file=sys.stderr)
