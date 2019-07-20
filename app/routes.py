from app import app
from flask import render_template
import folium

@app.route('/')
@app.route('/index')
def index():
    m = folium.Map(location=[42.4709, -70.9176], max_zoom=16, min_zoom=4, zoom_start=7)
    folium.Marker([42.4709, -70.9176], popup='<i>Ralphy Baby Lives Here!!</i>', tooltip="Click Me!").add_to(m)
    m.save('./app/templates/map.html')
    return render_template('index.html', title='Map Home')

