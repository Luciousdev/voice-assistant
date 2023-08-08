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
    response = response.choices[0].text.strip()
    return response  # Return the generated response



#########################
# LISTER FOR USER INPUT #
#########################

def chat_with_user():
    # Initialize the recognizer
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("[STATUS] - Adjusting for ambient noise level.")
            r.adjust_for_ambient_noise(source)

            print("[STATUS] - Listening...")
            audio = r.listen(source)

            if "assistant" in r.recognize_google(audio).lower():
                print("Assistant activated.")

                try:
                    print("Listening to user...")
                    user_audio = r.listen(source, timeout=5)
                    user_text = r.recognize_google(user_audio)
                    print("User said:", user_text)

                    # Generate assistant's response
                    assistant_response = chatgpt(user_text)

                    # Convert assistant's response to speech
                    text_to_speech(assistant_response)

                except sr.WaitTimeoutError:
                    print("No speech detected.")

                except sr.UnknownValueError:
                    print("[ERROR] - Unable to recognize speech.")

# Start the conversation loop
chat_with_user()
