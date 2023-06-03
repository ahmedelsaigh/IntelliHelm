from parse_command import ParseCommand
from navigation import Navigation
from outgoing_call import OutgoingCall
from outgoing_text import OutgoingText
from incoming_text import IncomingText
from play_audio import PlayAudio
import speech_recognition as sr
from transparent_display import Transparent_Display
from timeit import Timer
import os
import time
import sys


def channel_request(speech_text):

    if "do not answer" in speech_text or "hang up" in speech_text or "cancel" in speech_text:
        os.system("python ~/ofono-1.18/test/reject-calls")
        return
    elif "answer" in speech_text or "pick" in speech_text:
        os.system("python ~/ofono-1.18/test/answer-calls")
        return
    # process user input
    # audio_file = "audio_files/text1.wav"
    job, value = ParseCommand().run(speech_text)

    if job == "navigation":
        Navigation(value, display).start()

    elif job == "text":
        OutgoingText(value, display).start()

    elif job == "call":
        OutgoingCall(value).start()

PlayAudio().play_audio_output("Voice Assisstant started. Please pair your phone and put it on vibrate.")
# start incoming calls and text threads here
#IncomingText().start()

display = Transparent_Display()
while True:
    
    try:
        time.sleep(0.1)
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        # convert audio to speech
        try:
            speech_text = r.recognize_google(audio).lower()
            print(("\nGoogle Speech Recognition heard you say: " + speech_text))
            #if speech_text.startswith("helmet"):
            channel_request(speech_text)

        except sr.UnknownValueError:
            print("\nGoogle Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(("\nCould not request results from Google Speech Recognition service; {0}".format(e)))
    except KeyboardInterrupt:
        print("Phew! Done Searching")
        sys.exit()
