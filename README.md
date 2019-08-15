# mapWebsite

New saved file:

Save to local folder containing mammoth_convert.sh
Run `$ ./mammoth_convert.sh` in the directory with the .docx files that need to be converted
Move all the .html files onto the Amazon server, directory 'static' under mapWebsite/app:
`$ scp -i ~/.ssh/cjsaws-inst1.pem *.html ubuntu@18.220.141.162:~/mapWebsite/app/static`

If the marker for the file appears at the top of the map, the script could not read the GPS coordinates. Make sure they are in the format "GPS Coordinates: [123.45, 67.890]"



From the top directory, launch by typing:

`$ export FLASK_APP=map.py`

`$ export FLASK_RUN_PORT=8820`

`$ flask run --host=0.0.0.0` or `$ nohup flask run --host=0.0.0.0 &`

(or change port number in the above to the appropriate port for your instance). Nohup needs to be quit with `killall flask`

