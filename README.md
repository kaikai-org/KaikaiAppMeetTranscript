# KaikaiApp - Audio Transcription Application

KaikaiApp is a desktop application built with Kivy for recording audio, loading audio files, and transcribing audio using advanced diarization and speech recognition models. The application allows users to set the recording duration, save the audio file, and load existing audio files from the file system, including the desktop.

## Features

- Record audio for a specified duration.
- Save recorded audio as a WAV file.
- Load and transcribe existing audio files.
- Display transcription results in the application.
- Save transcription results to a text file with a timestamped filename.

## Requirements

- Python 3.6+
- Kivy
- PyAudio
- Wave
- Torch
- Transformers
- Pyannote.audio
- Datasets
- Speechbox

## Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/myapp.git
cd myapp
```

2. Create a virtual environment and activate it:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required libraries:

```sh
pip install -r requirements.txt
```

## Usage

1. Run the application:

```sh
python main.py
```

2. **Record Audio**:
   - Enter the desired recording duration in seconds in the provided input field.
   - Press the "Record" button to start recording.
   - The recorded audio will be saved with a timestamped filename in the current directory.
   - The transcription of the recorded audio will be displayed in the application.

3. **Load Audio File**:
   - Press the "Load Audio File" button.
   - Navigate to the desired audio file location using the file chooser (default path is set to the desktop).
   - Select the audio file to load and transcribe.
   - The transcription of the loaded audio will be displayed in the application.

## Project Structure

- `main.py`: The main application file that initializes and runs the Kivy application.
- `audio_capture.py`: Handles audio recording and loading audio files from the file system.
- `transcription.py`: Contains functions for transcribing audio using diarization and speech recognition models.
- `ui.kv`: Kivy language file defining the user interface layout.

## Code Overview

### main.py

This file contains the main Kivy application class `MyApp` which builds the user interface, handles events, and manages audio recording and transcription.

Here is a snippet from `main.py`:

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from audio_capture import record_audio, load_audio_file
from transcription import transcribe_audio
import threading
from datetime import datetime

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text='Enter duration (in seconds) and press "Record" to start recording, or load an audio file',
                           font_size='20sp', halign='center', valign='middle', size_hint_y=None, height=50)
        self.layout.add_widget(self.label)

        self.duration_input = TextInput(hint_text='Enter duration in seconds', input_filter='int', multiline=False,
                                        size_hint_y=None, height=50, font_size='20sp')
        self.layout.add_widget(self.duration_input)

        self.record_button = Button(text='Record', on_press=self.record_audio, font_size='20sp', size_hint_y=None, height=50)
        self.layout.add_widget(self.record_button)

        self.load_button = Button(text='Load Audio File', on_press=self.show_load, font_size='20sp', size_hint_y=None, height=50)
        self.layout.add_widget(self.load_button)

        self.transcription_label = Label(text='Transcription will appear here', font_size='20sp', halign='left', valign='top',
                                         size_hint_y=None, height=400, text_size=(400, None))
        self.transcription_label.bind(size=self.update_text_size)
        self.layout.add_widget(self.transcription_label)

        return self.layout

    def update_text_size(self, *args):
        self.transcription_label.text_size = (self.transcription_label.width, None)

    def record_audio(self, instance):
        duration = int(self.duration_input.text) if self.duration_input.text.isdigit() else 10
        threading.Thread(target=self._record_and_transcribe, args=(duration,)).start()

    def _record_and_transcribe(self, duration):
        now = datetime.now()
        audio_filename = now.strftime("audio_%Y%m%d_%H%M%S.wav")
        record_audio(audio_filename, duration)
        audio_data = load_audio_file(audio_filename)
        transcription = transcribe_audio(audio_data)
        self.transcription_label.text = transcription
        self.label.text = f'Recording finished and saved as {audio_filename}'

    def show_load(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView(path='C:/Users/ACER/Desktop')
        load_button = Button(text="Load", size_hint_y=None, height=50)
        content.add_widget(filechooser)
        content.add_widget(load_button)
        self.popup = Popup(title='Load Audio File', content=content, size_hint=(0.9, 0.9))

        def load_selected_file(instance):
            selection = filechooser.selection
            if selection:
                audio_data = load_audio_file(selection[0])
                transcription = transcribe_audio(audio_data)
                self.transcription_label.text = transcription
                self.label.text = 'File loaded and transcribed'
                self.popup.dismiss()

        load_button.bind(on_press=load_selected_file)
        self.popup.open()

if __name__ == "__main__":
    MyApp().run()
```

### audio_capture.py

This module provides functions for recording audio using PyAudio and saving it as a WAV file. It also includes a function for loading existing audio files from the file system.

Here is a snippet from `audio_capture.py`:

```python
import pyaudio
import wave
import io

def record_audio(filename, duration):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = duration

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished")
    stream.stop_stream()
    stream.close()
    audio.terminate()

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
```

### transcription.py

This module integrates the Pyannote.audio diarization pipeline and the OpenAI Whisper speech recognition model from the Hugging Face Transformers library. It handles the transcription of audio data and saves the transcription results to a text file with a timestamped filename.

Here is a snippet from `transcription.py`:

```python
import torch
import numpy as np
import wave
from pyannote.audio import Pipeline
from transformers import pipeline
from speechbox import ASRDiarizationPipeline
from datetime import datetime

diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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"
)

asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    language='en'
)

combined_pipeline = ASRDiarizationPipeline(
    asr_pipeline=asr_pipeline, diarization_pipeline=diarization_pipeline
)

def tuple_to_string(start_end_tuple, ndigits=1):
    return str((round(start_end_tuple[0], ndigits), round(start_end_tuple[1], ndigits)))

def format_as_transcription(raw_segments):
    return "\n\n".join(
        [
            chunk["speaker"] + " " + tuple_to_string(chunk["timestamp"]) + ": " + chunk["text"]
            for chunk in raw_segments
        ]
    )

def transcribe_audio(audio_data):
    with wave.open(audio_data, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)

    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    audio_np = audio_np.astype(np.float32) / 32768.0
    input_tensor = torch.from_numpy(audio_np[None, :])

    diarization_outputs = diarization_pipeline(
        {"waveform": input

_tensor, "sample_rate": framerate}
    )

    if not diarization_outputs:
        print("No diarization segments detected.")
        return "No diarization segments detected."

    asr_outputs = asr_pipeline(
        {"array": audio_np, "sampling_rate": framerate},
        generate_kwargs={"max_new_tokens": 256},
        return_timestamps=True,
        language='en'
    )

    if not asr_outputs:
        print("No ASR outputs detected.")
        return "No ASR outputs detected."

    print("Diarization Outputs:", diarization_outputs)
    print("ASR Outputs:", asr_outputs)

    final_outputs = combined_pipeline({"array": audio_np, "sampling_rate": framerate})
    transcription = format_as_transcription(final_outputs)

    now = datetime.now()
    filename = now.strftime("meet_transcript_%Y%m%d_%H%M%S.txt")

    with open(filename, "w", encoding='utf-8') as f:
        f.write(transcription)

    print(f"Transcription saved as {filename}")

    return transcription
```

### ui.kv

The Kivy language file defining the layout of the application, including input fields, buttons, and labels for displaying transcription results.

```kv
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    Label:
        id: label
        text: 'Enter duration (in seconds) and press "Record" to start recording, or load an audio file'
        font_size: '20sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: None
        height: 50

    TextInput:
        id: duration_input
        hint_text: 'Enter duration in seconds'
        input_filter: 'int'
        multiline: False
        size_hint_y: None
        height: 50
        font_size: '20sp'

    Button:
        text: 'Record'
        on_press: app.record_audio
        font_size: '20sp'
        size_hint_y: None
        height: 50

    Button:
        text: 'Load Audio File'
        on_press: app.show_load
        font_size: '20sp'
        size_hint_y: None
        height: 50

    Label:
        id: transcription_label
        text: 'Transcription will appear here'
        font_size: '20sp'
        halign: 'left'
        valign: 'top'
        size_hint_y: None
        height: 400
        text_size: self.width, None
```

## Troubleshooting

- Ensure all required libraries are installed correctly.
- Make sure your microphone is working and accessible by the application.
- Check file paths if you encounter issues loading audio files.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the Kaikai License.

## Acknowledgements

- [Kivy](https://kivy.org/)
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- [Pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [Speechbox](https://github.com/mravanelli/speechbox)

Feel free to contact us for any further questions or support.