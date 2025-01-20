# import the necessary packages
import pyaudio
import wave
import keyboard
import time
from openai import OpenAI

# define the codec and create an AudioFile object
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "test.wav"

# initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# alternative way to record audio with keyboard input
frames = []
print("Press Space to start recording.") 
keyboard.wait("space")
print("Recording... Press Space to stop recording.")
time.sleep(0.2)

# record audio until the space key is pressed
while True:
    try:
        data = stream.read(CHUNK)
        frames.append(data)
    except KeyboardInterrupt:
        break
    if keyboard.is_pressed("space"):
        print("Recording stopped.")
        time.sleep(0.2)
        break
    
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

# transcribe the audio file
client = OpenAI()

audio_file = open("test.wav", "rb")

transcription = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file,
)

print(transcription.text)