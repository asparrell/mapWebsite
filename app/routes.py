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
    location_list = []
    filenames = get_filenames()
    for file in filenames:
        marker = make_marker(file)
        if marker.location in location_list:
            marker.location[0] += 0.01  # will lessen this increment
            marker.location[1] += 0.01
            #name = file[:-5]
            #marker = folium.Marker(location, popup=name, tooltip=name)
        location_list.append(marker.location)
        print(location_list)
        marker.add_to(m)
    m.save('./app/templates/map.html')

    return render_template('index.html', title='Map Home')

place_code_to_lat_long = {'2.1.1.1': [55.017001, -114.930192], '2.1.1.2': [55.268163, -124.945342], '2.1.1.4': [55.079546, -97.449267], '2.1.1.7': [45.067580, -63.157430], '2.1.1.10': [51.253777, -85.323212], '2.1.1.13': [54.588975, -105.862449], '2.2.5.0': [18.928371, -70.384653]}

PATH = '/home/ubuntu/rock_art_files/'

def get_filenames() -> list:
    # List all files in the rock_art_files directory; will have to sort by .html
    filenames = []
    basepath = PATH
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            if entry[-5:] == '.html':
                filenames.append(entry)
    return filenames

def extract_filename_location() -> dict:
    # Get latlong coordinates from filename for each file
    filenames = get_filenames()
    filename_to_latlong = {}
    for file in filenames:
        file_code = file[:file.find(' ')]
        latlong = place_code_to_lat_long[file_code]
        filename_to_latlong[file] = latlong
    return filename_to_latlong

def make_file_to_coord_dict(file: str) -> dict:
    filename_to_coordinates = {}
    path = PATH + file
    with open(path) as f:
        file_data = f.read()
    start_index = file_data.find('oordinates')
    if start_index != -1:
        data_slice = file_data[start_index: start_index + 50]
        index1 = data_slice.find('>')
        index2 = data_slice.find('<', index1)
        coordinates = data_slice[index1 + 1:index2].strip()
        coords = format_coords(coordinates)
        filename_to_coordinates[file] = coords
    else:
        filename_to_latlong = extract_filename_location()
        location = filename_to_latlong[file]
        filename_to_coordinates[file] = location

    return filename_to_coordinates

def format_coords(coordinates: str) -> list:
    # changes coordinate string to float list
    coords = []
    lat = coordinates[:coordinates.find(',')]
    lat = float(lat)
    coords.append(lat)
    long = coordinates[coordinates.find(' ') + 1:]
    long = float(long)
    coords.append(long)
    
    return coords

def make_marker(filename: str):
    # return a Marker object with the properties of a file
    file_to_coords = make_file_to_coord_dict(filename)
    location = file_to_coords[filename]
    name = filename[:-5]
    marker = folium.Marker(location, popup=name, tooltip=name)

    return marker


# print("", file=sys.stderr)
