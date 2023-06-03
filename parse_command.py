import speech_recognition as sr
from os import path

class ParseCommand:

    def run(self, speech_text):
        
        # speech_text = audio_to_text(audio)
        job, value = text_to_job(speech_text)
        print(("\nJob: " + job))
        print(("Value: " + value))
        return job, value

# def audio_to_text(audio):

    # # audio_file format example: "speech.wav"
    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), audio_file_name)
    # # use the audio file as the audio source
    # r = sr.Recognizer()
    # with sr.AudioFile(AUDIO_FILE) as source:
    #     r.adjust_for_ambient_noise(source)
    #     audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    # try:
    #     # for testing purposes, we're just using the default API key
    #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    #     # instead of `r.recognize_google(audio)`
    #     speech_text = r.recognize_google(audio)
    #     print("\nGoogle Speech Recognition heard you say: " + speech_text)
    # except sr.UnknownValueError:
    #     print("\nGoogle Speech Recognition could not understand audio")
    # except sr.RequestError as e:
    #     print("\nCould not request results from Google Speech Recognition service; {0}".format(e))

    # return speech_text

def text_to_job(speech_text):

    phrase_map = dict()
    phrase_map["directions to"] = "navigation"
    phrase_map["go to"] = "navigation"
    phrase_map["get to"] = "navigation"
    phrase_map["navigate to"] = "navigation"
    phrase_map["take me to"] = "navigation"

    phrase_map["call"] = "call"
    phrase_map["dial"] = "call"

    phrase_map["text"] = "text"
    #phrase_map["text this to"] = "text"
    #phrase_map["send a text to"] = "text"
    #phrase_map["send a message to"] = "text"
    phrase_map["send"] = "text"
    phrase_map["message"] = "text"

    job = ""
    value = ""
    for k,v in phrase_map.items():
        if k in speech_text:
            job = v
            value = speech_text.split(k,1)[1].strip()
            break

    return job, value
