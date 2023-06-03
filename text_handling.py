#!/usr/bin/python

import bluetooth
import threading
import time
import random
import sys

address="60:14:66:E8:EE:5E" #RPi MAC Address
host="60:14:66:E8:EE:5E"
uuid="8ce255c0-200a-11e0-ac64-0800200c9a66"

service_matches = bluetooth.find_service( uuid = uuid, address = address )

while True:
  try:
    print("Searching ...")
    try: service_matches
    except NameError:
      service_matches = bluetooth.find_service( uuid = uuid)
    else:
      if not service_matches:
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

      print("Happy Spamming")

      while True:
        try:
          #string = 'test' + random.choice('abcdefghij') + '\n'
          string = "+16474447887 hello" 
          try:
            # sending to andorid
            #sock.send(string)
            #break

            # recieving from android
            data = sock.recv(1024)
            if len(data) == 0: break
            print("received [%s]" % data)

            time.sleep(0.5)
          except:
            print("Android no longer interested in my spam, socket not valid, going back to searching")
            break
        except KeyboardInterrupt:
          print("Done with Spamming, Press Ctrl-C again if you wish to quit, otherwise I'll keep searching")
          break


  except KeyboardInterrupt:
    print("Phew! Done Searching")
    sys.exit()

if service_matches:
  first_match = service_matches[0]
  port = first_match["port"]
  name = first_match["name"]
  host = first_match["host"]

  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((host, port))

  print("Happy Spamming")

  while True:
    try:
      string = 'test' + random.choice('abcdefghij') + '\n'
      sock.send(string)
      time.sleep(0.5)
    except KeyboardInterrupt:
      print("Done with Spamming")
      sys.exit()


sock.close()


# Part 1: Pairing
#     - RPi bluetooth must be on at all times.
#     - Phone detects RPi.
#     - Phone initiates connection and pair.

# Part 2: Call
#     - Forward call from phone to RPi.
#     - Ask user to answer call (Yes/No).
#     - Establish call.








# Part 3: Text
#     - 
