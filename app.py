import speech_recognition as sr
from openai import OpenAI
import pyttsx3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

client = OpenAI(api_key="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")
engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('index.html')
#-------------------------------------------------------------- main function to be exected when the button is pressed
@app.route('/execute_function', methods=['POST'])
def execute_function():# if you change this name, you have to change the function name in the js code as well 
    recognizer = sr.Recognizer()
    is_listening = True

    # Read data from data.txt
    data_path = 'static/information/data.txt'  # Relative path to data.txt
    with open(data_path, 'r') as file:
        data = file.read()

    while True:
        if is_listening:
            print("What do you desire..?")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                filename = "static/audio/input.wav"
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

            # Transcribe audio to text
            text = transcribe_audio_to_text(filename)

            if text:
                print(f"You said: {text}")
                if text =="who is the head of visual computing lab":
                    speak_text("The head of visaul computing lab is Samuel")
                    return jsonify({'message': "The head of visaul computing lab is Samuel"})
                if text == "explain Tushar project":
                    speak_text(data)
                    return jsonify({'message': data})
                elif text:
                        
                    # Generate response using AutoGPT and data from data.txt as context
                    response = generate_response(text, data)
                    print(f"The answer you desired is: {response}")
                    # Speak the response
                    speak_text(response)
                    return jsonify({'message': response})
            else:
                print("Error: Could not transcribe audio to text")
                return jsonify({'message': 'Error: Could not transcribe audio to text'})


#--------------------------------------------------------------
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print('Error:', e)
        return None

def generate_response(prompt, context):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=context + "\nQuestion: " + prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    app.run(debug=True)
