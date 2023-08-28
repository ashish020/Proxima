import speech_recognition as sr
import os
import openai
import pyttsx3
import random


# OPEN AI key

openai.api_key = "##########################################"
model_id = 'gpt-3.5-turbo'

# Initiating the test-to-speech engine
engine = pyttsx3.init()

# Changing speech rate
engine.setProperty('rate', 180)

# Get the available voice
voices = engine.getProperty('voices')

# Choose the voice based on the voice id
engine.setProperty('voice', voices[1].id)

# counter just for interacting purposes
interaction_counter = 0


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("")
            #Print('Skipping unknown error')


def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )

    api_usage = response['usage']
    print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


# Starting conversation
conversation = []
conversation.append({'role': 'user', 'content': 'Please, act like Friday AI from Iron Man, make a 1 sentence phrase introducing yourself without saying something that sounds like this chat is already defined'})
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())


def activate_assistant():
    starting_chat_phrases = ["Yes sir, how can i help you?",
                             "Yes, what can i do for you?",
                             "How can i help you, sir?",
                             "Proxima here, how can i help you today?",
                             "Yes boss, whats the plan?",
                             "Yes, What's in your mind sir?",
                             "Yes boss, I am here to help",
                             "How can I assist you today, sir?",
                             "Yes sir, How can I make your day easier?"]

    continued_chat_phrases = ["yes", "Yes, sir", "Yes, boss", "I'm all ears"]
    random_chat = ""
    if(interaction_counter == 1):
        random_chat = random.choices(starting_chat_phrases)
    else:
        random_chat = random.choices(continued_chat_phrases)

    return  random_chat


def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")


while True:
    # wait for user to say "Proxima
    print("Say 'Proxima' to start.....")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if "proxima" in transcription.lower():
                interaction_counter += 1

                # record audio

            filename = 'input.wav'

            readyToWork = activate_assistant()
            speak_text(readyToWork)
            print(readyToWork)
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                source.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

                    # transcribe audio to text
            text = transcribe_audio_to_text(filename)

            if text:
                print(f"You Said: {text}")
                append_to_log(f"You: {text}\n")

                # generate response using chatGPT

                print(f"Proxima says: {conversation}")

                prompt = text

                conversation.append({'role': 'user', 'content': prompt})
                conversation = ChatGPT_conversation(conversation)

                print('{0} {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content']))

                append_to_log(f"Proxima: {conversation[-1]['content'].strip()}\n")



                # Read response using text to speech
                speak_text(conversation[-1]['content'].strip())

        except Exception as e:
            continue
            #Print("An error occurred: {}".format(e)












