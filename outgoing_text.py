import bluetooth
from threading import Thread
import time
import random
import sys
import os
from gtts import gTTS
from play_audio import PlayAudio

class OutgoingText(Thread):

    def __init__(self, value, display):
        Thread.__init__(self)
        self.value = value
        self.display = display

    def run(self):

        msg = construct_bluetooth_msg(self.value)
        if not msg:
            return

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

                    sock.send(msg)
                    #PlayAudio().play_audio_output("Message Sent")
                    play_audio_output("Message Sent")

                    print(("Sent: " + msg))
                    sock.close()
                    
                    self.display.clear_name()
                    self.display.write_incoming("Message Sent")

                    time.sleep(2)

                    self.display.clear_incoming()
                    return

            except KeyboardInterrupt:
                print("Phew! Done Searching")
                sys.exit()

def construct_bluetooth_msg(value):

    if "to" in value:
        # error handling
        if len(value.split()) < 3:
            return ""

        msg_then_recipient = value.rsplit("to", 1)
        msg = msg_then_recipient[0].strip()
        recipient = msg_then_recipient[1].strip()
    else:
        # error handling
        if len(value.split()) < 2:
            return ""

        recipient_then_msg = value.split(' ', 1)
        recipient = recipient_then_msg[0].strip()
        msg = recipient_then_msg[1].strip()
    
    if recipient == "john":
        recipient = "+16474447887"
    elif recipient == "mo" or recipient == "mohamed" or recipient == "mohammad":
        recipient = "+1905924505"
    elif recipient == "arnab" or recipient == "anab" or recipient == "mohammad":
        recipient = "+16474447887"
    elif recipient == "chigo" or recipient == "cheego" or recipient == "sheego":
        recipient = "+1905924505"
    else:
        recipient = "+16474447887"

    print(("\nRecipient: " + recipient))
    print(("Message: " + msg))
    return recipient + " " + msg


def play_audio_output(text):

    #if os.path.exists('navigation.mp3'): # lower volume

    myobj = gTTS(text=text, lang='en', slow=False) 

    # Saving the converted audio in a mp3 file
    myobj.save("text_sent.mp3") 

    # Playing the converted file 
    os.system("mpg321 text_sent.mp3") 

    # remove when done
    os.remove('text_sent.mp3')
