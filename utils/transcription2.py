import torch
import wave
import numpy as np
from pyannote.audio import Pipeline
from transformers import pipeline
from speechbox import ASRDiarizationPipeline
from datetime import datetime

# Charger le pipeline de diarisation
diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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"
)

# Charger le pipeline de reconnaissance vocale
asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
)

# Créer le pipeline combiné
combined_pipeline = ASRDiarizationPipeline(
    asr_pipeline=asr_pipeline, diarization_pipeline=diarization_pipeline
)

def tuple_to_string(start_end_tuple, ndigits=1):
    return str((round(start_end_tuple[0], ndigits), round(start_end_tuple[1], ndigits)))

def format_as_transcription(raw_segments):
    return "\n\n".join(
        [
            chunk["speaker"] + " " + tuple_to_string(chunk["timestamp"]) + chunk["text"]
            for chunk in raw_segments
        ]
    )

def transcribe_audio(filename):
    # Lire le fichier WAV
    with wave.open(filename, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)

    # Convertir en numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    audio_np = audio_np.astype(np.float32) / 32768.0  # Normaliser les données audio
    input_tensor = torch.from_numpy(audio_np[None, :])

    # Utiliser le pipeline de diarisation
    diarization_outputs = diarization_pipeline(
        {"waveform": input_tensor, "sample_rate": framerate}
    )

    # Vérifier s'il y a des segments de diarisation
    if not diarization_outputs:
        print("No diarization segments detected.")
        return "No diarization segments detected."

    # Utiliser le pipeline de reconnaissance vocale
    asr_outputs = asr_pipeline(
        {"array": audio_np, "sampling_rate": framerate},
        generate_kwargs={"max_new_tokens": 256},
        return_timestamps=True,
    )

    # Vérifier s'il y a des résultats de reconnaissance vocale
    if not asr_outputs:
        print("No ASR outputs detected.")
        return "No ASR outputs detected."

    # Afficher les résultats intermédiaires pour le débogage
    print("Diarization Outputs:", diarization_outputs)
    print("ASR Outputs:", asr_outputs)

    # Combiner les résultats des deux pipelines
    final_outputs = combined_pipeline({"array": audio_np, "sampling_rate": framerate})

    transcription = format_as_transcription(final_outputs)

    # Générer le nom du fichier basé sur la date et l'heure actuelles
    now = datetime.now()
    filename = now.strftime("meet_transcript_%Y%m%d_%H%M%S.txt")

    # Sauvegarder la transcription dans un fichier texte
    with open(filename, "w", encoding='utf-8') as f:
        f.write(transcription)

    return format_as_transcription(final_outputs)
