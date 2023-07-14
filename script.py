from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import openai
import os



###################################
# CONVERT CHATGPT RESPONSE TO TTS #
###################################


def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language,  slow=False, lang_check=False)
    tts.save('output.mp3')
    audio = AudioSegment.from_file('output.mp3', format='mp3')
    play(audio)
    # Remove the temporary audio file
    os.remove('output.mp3')
    listening()


#############################
# GET RESPONSE FROM CHATGPT #
#############################

openai.api_key = 'sk-'

def chatgpt(prompt):
    start_sequence = "\nA:"
    restart_sequence = "\n\nQ: "


    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Q: {prompt}",
        temperature=0.7,
        max_tokens=50,
        n=1,
        stop=None
    )

    # response = response.choices[0].text
    response=response.choices[0].text.strip()

    text_to_speech(response) 



#########################
# LISTER FOR USER INPUT #
#########################

def listening():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Continuously listen for audio input
    while True:
        with sr.Microphone() as source:

            print("[STATUS] - Adjusting for ambient noise level.")
            r.adjust_for_ambient_noise(source)

            # Listen for user input
            print("[STATUS] - Listening...")
            audio = r.listen(source)

            # Use the keyword to activate assistant
            if "assistant" in r.recognize_google(audio).lower():
                print("Assistant activated.")

                # Capture speech until the person stops talking
                try:
                    print("Listening to user...")
                    user_audio = r.listen(source, timeout=5)

                    # Convert captured speech to text
                    user_text = r.recognize_google(user_audio)
                    print("User said:", user_text)
                    chatgpt(user_text)

                except sr.WaitTimeoutError:
                    print("No speech detected.")

                except sr.UnknownValueError:
                    print("[ERROR] - Unable to recognize speech.")

                break

            else:
                print("[NOTE] - Keyword not detected.")


listening()
# chatgpt("Hello")
