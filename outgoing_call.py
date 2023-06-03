import bluetooth
from threading import Thread
import time
import random
import sys
import os

class OutgoingCall(Thread):

    def __init__(self, contact):
        Thread.__init__(self)
        self.contact = contact

    def run(self):

        recipient = self.contact
        if recipient == "john":
            recipient = "+16474447887"
        elif recipient == "mo" or recipient == "mohamed" or recipient == "mohammad":
            recipient = "+1905924505"
        elif recipient == "jane" or recipient == "arnab" or recipient == "amed":
            recipient = "+16474447887"
        elif recipient == "chigo" or recipient == "cheego" or recipient == "sheego":
            recipient = "+1905924505"
        else:
            recipient = "+16474447887"

        os.system("python ~/ofono-1.18/test/dial-number %s" % recipient)
