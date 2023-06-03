import mapbox
import geocoder
import serial
import time
import string
import pynmea2
import os
from gtts import gTTS
from threading import Thread
from play_audio import PlayAudio
from timeit import Timer

class Navigation(Thread):

    def __init__(self, destination_name, display):
        Thread.__init__(self)
        self.destination_name = destination_name
        self.display = display

    def run(self):

        is_env_local = False

        if is_env_local:
            ser = open('gps_coordinates.txt', 'r')
        else:
            ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, timeout=1)

        proximity_location = first_run_to_get_proximity(ser, is_env_local)

        # use the first gps coordinates for geocoding proximity
        destination_coord = geocode_destination(self.destination_name, proximity_location)
        destination_coord_to_lnglat = [destination_coord[1], destination_coord[0]]
        print(("Destination Geocode: " + str(destination_coord_to_lnglat)))

        read_counter = 0

        while True:
            data_line = ser.readline()
            gps_tag = data_line[0:6]
            
            time.sleep(2)
            # a way of slowing down the updating of directions
            if gps_tag == "$GNRMC":
                read_counter += 15
            if read_counter < 15:
                continue
            read_counter = 0 #reset
            
            print(data_line)
            #continue

            # extract location coordinates
            if is_env_local:
                #for line in ser:
                data_line_map = data_line.split(',')
                lat = data_line_map[1]
                lng = data_line_map[2]
            else:
                #for line in ser:
                data_line_map = pynmea2.parse(data_line)
                lat = data_line_map.latitude
                lng = data_line_map.longitude
            location = [lat, lng]

            gps = "Location = " + str(location[0]) + ", " + str(location[1])
            print(gps)

            if location[0] == 0.0 or location[1] == 0.0:
                continue

            # make the api call using the current driver location
            response = api_call(location, destination_coord_to_lnglat)

            # extract the navigation directions from the api response
            navigation = get_navigation(response)
            if not navigation:
                play_audio_output("Invalid destination")
                return

            if navigation["distance"] < 20 and navigation["turn"] == "arrive":
                print("You have arrived.")
                self.display.write_street_name("You have arrived.")
                self.display.clear_distance()
                self.display.clear_direction()
                play_audio_output("You have arrived at your destination")
                time.sleep(2)
                self.display.clear_street_name()
                #ser.flushInput()
                #ser.flushOutput()
                ser.close()
                return
            else:
                print(navigation["instruction"])
                #PlayAudio().play_audio_output(navigation["instruction"])
                if not navigation["street_name"]:
                    play_audio_output("turn " + navigation["turn"])
                    self.display.clear_street_name()
                    self.display.write_direction("Turn " + navigation["turn"])
                    self.display.write_distance(str(navigation["distance"]) + "m")
                else:
                    play_audio_output("turn " + navigation["turn"] + " on " + navigation["street_name"])
                    self.display.write_street_name(navigation["street_name"])
                    self.display.write_direction("Turn " + navigation["turn"])
                    self.display.write_distance(str(navigation["distance"]) + "m")

API_KEY = 'pk.eyJ1IjoiaW50ZWxsaWhlbG0iLCJhIjoiY2trNmFmcHBkMDByYTJ2bW84cnA2OWhpNiJ9.Q8ywzffxS2XSF7MVo_P2HQ'

def geocode_destination(dest, proximity):

    print(("Destination Name: " + str(dest)))
    print(("Proximity for: " + str(proximity) + "\n\n"))
    g = geocoder.mapbox(dest, key=API_KEY, proximity=proximity)
    return g.latlng

def api_call(location, destination_coord):
	access_token = API_KEY
	service = mapbox.Directions(access_token=access_token)

	origin = {
	    'type': 'Feature',
	    'geometry': {
	        'type': 'Point',
	        'coordinates': [float(location[0]), float(location[1])]}}
	destination = {
	    'type': 'Feature',
	    'geometry': {
	        'type': 'Point',
	        'coordinates': [float(destination_coord[0]), float(destination_coord[1])]}}

	response = service.directions([origin, destination], profile='mapbox/driving', steps=True)
	return response

def get_navigation(response):

    directions = dict()

    #print((response.json()))
    if not response.json()['routes']:
        return
    steps = response.json()['routes'][0]['legs'][0]['steps']

    if steps[1]['maneuver']['type'] == "arrive":
        directions["turn"] = "arrive"
    else:
        directions["turn"] = steps[1]['maneuver']['modifier']

    directions["instruction"] = steps[0]['maneuver']['instruction']
    directions["street_name"] = steps[0]['name']
    directions["duration"] = steps[0]['duration']
    directions["distance"] = steps[0]['distance']

    return directions

def first_run_to_get_proximity(ser, is_env_local): # $GNRMC,-80.529282,43.496972

    data_line = ser.readline()
    gps_tag = data_line[0:6]

    while gps_tag != "$GNRMC":   
        data_line = ser.readline()
        gps_tag = data_line[0:6]
    
    # extract location coordinates
    if is_env_local:
        #for line in ser:
        data_line_map = [x.strip() for x in data_line.split(',')]
        lat = data_line_map[1]
        lng = data_line_map[2]
    else:
        #for line in ser:
        data_line_map = pynmea2.parse(data_line)
        lat = data_line_map.latitude
        lng = data_line_map.longitude
    proximity_location = [float(lng), float(lat)]

    return proximity_location

def play_audio_output(instruction):

    if not os.path.exists('navigation.mp3'):

        myobj = gTTS(text=instruction, lang='en', slow=False) 

        # Saving the converted audio in a mp3 file
        myobj.save("navigation.mp3") 

        # Playing the converted file 
        os.system("mpg321 navigation.mp3") 

        # remove when done
        os.remove('navigation.mp3')

        if os.path.exists('text_on_hold.mp3'):

            # Playing the converted file 
            os.system("mpg321 text_on_hold.mp3") 

            # remove when done
            os.remove('text_on_hold.mp3')
