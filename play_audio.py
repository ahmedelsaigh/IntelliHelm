# Import the required module for text 
# to speech conversion 
from gtts import gTTS 
#from playsound import playsound
import os
#import pygame
#from io import BytesIO
import io
import time
#from tempfile import TemporaryFile
#from IPython.display import Audio

class PlayAudio:
    
    def play_audio_output(self, text):

        if not os.path.exists('output.mp3'):

            myobj = gTTS(text=text, lang='en', slow=False) 

            # Saving the converted audio in a mp3 file named 
            # welcome 
            myobj.save("output.mp3") 

            # Playing the converted file 
            os.system("mpg321 output.mp3") 

            # remove when done
            os.remove('output.mp3')

       	#tts = gTTS(text=text, lang='en')
        #fp = BytesIO()
        #tts.write_to_fp(fp)
        #fp.seek(0)
        #pygame.mixer.init()
        #pygame.mixer.music.load(fp)
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
        #    pygame.time.Clock().tick(10)

        # with io.BytesIO() as f:
        #     gTTS(text=text, lang='en').write_to_fp(f)
        #     f.seek(0)
        #     pygame.mixer.init()
        #     pygame.mixer.music.load(f)
        #     pygame.mixer.music.play()
        #     while pygame.mixer.music.get_busy():
        #         continue
