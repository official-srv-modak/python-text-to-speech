import speech_recognition as sr

from gtts import gTTS
import os

def text_to_speech(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')

    # Save the generated speech to a file
    tts.save("output.mp3")

    # Play the generated speech (macOS)
    os.system("afplay output.mp3")

def recognise_speech(placeholder, count):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use microphone as source
    with sr.Microphone() as source:
        print("Listening...")
        if count == 1:
            text_to_speech(placeholder)
        audio = recognizer.listen(source)

    # Convert speech to text
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        #print(text_to_speech("You said: " + text))
        return text
    except sr.UnknownValueError:
        text = "Sorry, could not understand what you just said."
        print(text)
        text_to_speech(text)
    except sr.RequestError as e:
        text = "Error fetching results; {0}".format(e)
        print(text)
        text_to_speech(text)



#print(recognise_speech())




