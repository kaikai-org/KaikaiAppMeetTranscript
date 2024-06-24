import speech_recognition as sr
import pyaudio
import wave
import threading
import io

def record_audio(filename, duration):
    # Paramètres d'enregistrement
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = duration

    # Initialisation de l'enregistreur
    audio = pyaudio.PyAudio()

    # Ouverture du flux d'enregistrement
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished")

    # Arrêt du flux et fermeture
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Sauvegarde des données audio dans un fichier WAV
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return filename

def load_audio_file(file_path):
    with open(file_path, "rb") as f:
        audio_data = f.read()
    return io.BytesIO(audio_data)