import bluetooth
from threading import Thread
import time
import random
import sys
import os
from gtts import gTTS
from play_audio import PlayAudio

class IncomingText(Thread):

    def __init__(self):#, display):
        #self.display = display
        Thread.__init__(self)

    def run(self):

        address="60:14:66:E8:EE:5E" #RPi MAC Address
        host="60:14:66:E8:EE:5E"
        uuid="8ce255c0-200a-11e0-ac64-0800200c9a66"

        service_matches = bluetooth.find_service( uuid = uuid, address = address )

        count = 0
        while True:
            try:
                print("Searching ...")
                try: service_matches
                except NameError:
                    service_matches = bluetooth.find_service( uuid = uuid)
                else:
                    if not service_matches:
                        if count > 10:
                            # output to speaker "Bluetooth is not connected"
                            return
                        count+=1
                        print ("without address")
                        service_matches = bluetooth.find_service( uuid = uuid)
                    else:
                        print ("with address")
                        service_matches_with_addr = bluetooth.find_service( uuid = uuid, address = host )
                        if service_matches_with_addr:
                            service_matches = service_matches_with_addr
                        else:
                            continue

                if service_matches:
                    first_match = service_matches[0]
                    port = first_match["port"]
                    name = first_match["name"]
                    host = first_match["host"]

                    print("connecting to \"%s\" on %s %s" % (name, host,port))
                    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                    sock.connect((host, port))

                    while True:
                        try:
                            try:
                                # msg recieved from android
                                data = sock.recv(1024)
                                if len(data) == 0: break

                                # strip hash number and hashtag from msg
                                msg = extractMsg(data)
                                print("received [%s]" % msg)
                                play_audio_output("Ahmed said " + msg)
                                #self.display.write_incoming("Incoming Message")

                                time.sleep(0.5)

                                #self.display.clear_incoming()
                            except:
                                print("Android no longer interested in my spam, socket not valid, going back to searching")
                                break
                        except KeyboardInterrupt:
                            print("Done with Spamming, Press Ctrl-C again if you wish to quit, otherwise I'll keep searching")
                            break

            except KeyboardInterrupt:
                print("Phew! Done Searching")
                sys.exit()

def extractMsg(data):
    # removes trailing hash number
    data = data.rsplit(' ', 1)[0]
    # removes opening hashtag
    data = data.split(' ', 1)[1]
    return data

def play_audio_output(text):

    myobj = gTTS(text=text, lang='en', slow=False) 

    if os.path.exists('navigation.mp3'):

        # Saving the converted audio in a mp3 file
        myobj.save("text_on_hold.mp3") 

    else:
        # Saving the converted audio in a mp3 file
        myobj.save("incoming_text.mp3") 

        # Playing the converted file 
        os.system("mpg321 incoming_text.mp3") 

        # remove when done
        os.remove('incoming_text.mp3')
