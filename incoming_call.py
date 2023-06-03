import time
from transparent_display import Transparent_Display

display = Transparent_Display()
#time.sleep(8)

display.write_incoming("Incoming Call")

time.sleep(3)

display.clear_incoming()
