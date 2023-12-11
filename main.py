import json
from vosk import Model, KaldiRecognizer
import pyaudio
import openai
from threading import Thread
from gtts import gTTS
import os

def get_ChatGPT_API():
    sf = open('settings.txt', 'r')
    key = sf.readlines()
    sf.close()
    print("Ключ считан!")
    return key[0].split()[1].replace(" ", "")

def get_gptmodel():
    sf = open('settings.txt', 'r')
    mdl = sf.readlines()
    sf.close()
    print("Модель Chat GPT установлена!")
    return mdl[1].split()[1].replace(" ", "")

openai.api_key = get_ChatGPT_API()

def chat_ai(mes):
    a = openai.ChatCompletion.create(
        model=get_gptmodel(),
        messages=[{"role": "user", "content": mes}])
    answer = a['choices'][0]['message']['content']
    ans = f'{answer}'.strip()
    print(ans)
    TTS(ans)

def TTS(txt):
    stream.stop_stream()
    audio = gTTS(text=txt, lang="ru", slow=False)
    audio.save("tts.mp3")
    os.system('/Applications/VLC.app/Contents/MacOS/VLC -I rc --play-and-exit --rate 1.5 tts.mp3')
    stream.start_stream()

def get_model():
    sf = open('settings.txt', 'r')
    path = sf.readlines()
    sf.close()
    print("Путь к модели Vosk считан!")
    return path[2].split()[1].replace(" ", "")

def get_rate():
    sf = open('settings.txt', 'r')
    ratest = sf.readlines()
    sf.close()
    print("Частота считана!")
    ratest = int(ratest[3].split()[1].replace(" ", ""))
    return ratest

drate = get_rate()
path = get_model()
model = Model(path)
rec = KaldiRecognizer(model, drate)
p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16, 
    channels=1, 
    rate=drate, 
    input=True, 
    frames_per_buffer=drate
)
stream.start_stream()

while True:
    data = stream.read(4000)
    if rec.AcceptWaveform(data):
        data = json.loads(rec.Result())["text"]
        text = str(data)
        if "чат" in text:
            text = text.replace("чат ", "")
            print(text)
            Thread(target=chat_ai, args=(text + " кратко", )).start()
