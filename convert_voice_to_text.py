import speech_recognition as sr
from os import path

import soundfile


def convert_voice_to_text(file_path):
    wav_file_path = 'test-source/voice.wav' 
    data, samplerate = soundfile.read(file_path)
    soundfile.write(wav_file_path, data, samplerate, subtype='PCM_16')

    audio_file = path.join(path.dirname(path.realpath(__file__)), wav_file_path)

    r = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))