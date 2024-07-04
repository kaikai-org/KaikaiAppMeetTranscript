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

### audio_capture.py

This module provides functions for recording audio using PyAudio and saving it as a WAV file. It also includes a function for loading existing audio files from the file system.


### transcription.py

This module integrates the Pyannote.audio diarization pipeline and the OpenAI Whisper speech recognition model from the Hugging Face Transformers library. It handles the transcription of audio data and saves the transcription results to a text file with a timestamped filename.


### ui.kv

The Kivy language file defining the layout of the application, including input fields, buttons, and labels for displaying transcription results.


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