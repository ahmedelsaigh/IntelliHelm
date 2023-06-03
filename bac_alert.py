import sys
from play_audio import PlayAudio
import serial
import pynmea2

def coordinates(ser, is_env_local): # $GNRMC,-80.529282,43.496972

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


ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, timeout=1)
coordinates_string = ' '.join(str(n) for n in coordinates(ser, False))

value = "Hi, I am not sober enough to drive. Please come get me at %s. to %s" % (coordinates_string, sys.argv[1])

PlayAudio().play_audio_output("B A C level low")
OutgoingText(value).start()
