from app import app
from flask import render_template, url_for
import folium
import mammoth
import os
import sys

# constants
place_code_to_lat_long = {'2.1.1.1': [55.017001, -114.930192], '2.1.1.2': [55.268163, -124.945342], '2.1.1.4': [55.079546, -97.449267], '2.1.1.7': [45.067580, -63.157430], '2.1.1.10': [51.253777, -85.323212], '2.1.1.13': [54.588975, -105.862449], '2.2.5.0': [18.928371, -70.384653]}

PATH = '/home/ubuntu/mapWebsite/app/static/'


@app.route('/')
@app.route('/index')
def index():
    # create map, populate with markers, and offset overlapping markers
    m = folium.Map(min_zoom=2, max_zoom=14, zoom_start=2)
    location_list = []
    filenames = get_filenames()
    for file in filenames:
        marker = make_marker(file)
        while marker.location in location_list:
            marker.location[0] += 0.001
            marker.location[1] += 0.001
        location_list.append(marker.location)
        marker.add_to(m)
    m.save('./app/templates/map.html')

    return render_template('index.html', title='Map Home')


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
    # extract coordinate strings from each file and store them in a dictionary with their file
    filename_to_coordinates = {}
    path = PATH + file
    with open(path) as f:
        file_data = f.read()
    start_index = file_data.find('oordinates')
    if start_index != -1:
        data_slice = file_data[start_index: start_index + 50]
        coordinates = re.findall(r'[-]?\d+\.?\d*, [-]?\d+\.?\d*', data_slice)
        coords = format_coords(coordinates[0])
        filename_to_coordinates[file] = coords
    else:
        filename_to_latlong=extract_filename_location()
        location=filename_to_latlong[file]
        filename_to_coordinates[file]=location

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


def get_url(file: str) -> list:
    url = (url_for('static', filename=file))
    
    return url  # incomplete url


def make_marker(filename: str):
    # return a Marker object with the properties of a file
    url = get_url(filename)
    file_to_coords = make_file_to_coord_dict(filename)
    location = file_to_coords[filename]
    index = filename.rfind("-")
    name = filename[index + 1:-5]    
    marker = folium.Marker(location, popup='<a href="' + url + '" target="_blank">' + name + '</a>', tooltip=name)

    return marker


# print("", file=sys.stderr)
