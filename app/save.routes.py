from app import app
from flask import render_template
import folium
import os

@app.route('/')
@app.route('/index')
def index():
    m = folium.Map(min_zoom=2, max_zoom=14, zoom_start=2)
    #folium.Marker([42.4709, -70.9176], popup='<i>Ralphy Baby Lives Here!!</i>', tooltip="Click Me!").add_to(m)
    m.save('./app/templates/map.html')
    return render_template('index.html', title='Map Home')

# def make_marker():
    #folium.Marker([location], popup='link to file', tooltip='site name, derived from separate location').add_to(m)

def get_filenames():
    # List all files in a directory using os.listdir
    basepath = '/home/ubuntu/rock_art_files/'
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            print(entry)
