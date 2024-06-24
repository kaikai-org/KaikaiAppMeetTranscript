from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from utils.audio_capture import record_audio, load_audio_file
from utils.transcription import transcribe_audio
import io
import threading
from datetime import datetime

class MyApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.label = Label(
            text='Enter duration (in seconds) and press "Record" to start recording, or load an audio file',
            font_size='20sp',
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.label)

        self.duration_input = TextInput(
            hint_text='Enter duration in seconds',
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        self.layout.add_widget(self.duration_input)

        self.record_button = Button(
            text='Record',
            on_press=self.record_audio,
            font_size='20sp',
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.record_button)

        self.load_button = Button(
            text='Load Audio File',
            on_press=self.show_load,
            font_size='20sp',
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.load_button)

        self.transcription_label = Label(
            text='Transcription will appear here',
            font_size='20sp',
            halign='left',
            valign='top',
            size_hint_y=None,
            height=400,
            text_size=(400, None)
        )
        self.transcription_label.bind(size=self.update_text_size)
        self.layout.add_widget(self.transcription_label)

        return self.layout

    def update_text_size(self, *args):
        self.transcription_label.text_size = (self.transcription_label.width, None)

    def record_audio(self, instance):
        duration = int(self.duration_input.text) if self.duration_input.text.isdigit() else 10
        threading.Thread(target=self._record_and_transcribe, args=(duration,)).start()

    def _record_and_transcribe(self, duration):
        # Générer le nom du fichier basé sur la date et l'heure actuelles
        now = datetime.now()
        audio_filename = now.strftime("./audios_meet/audio_meet_%Y%m%d_%H%M%S.wav")

        # Capturer l'audio et sauvegarder dans un fichier
        record_audio(audio_filename, duration)

        # Charger l'audio depuis le fichier et le transcrire
        audio_data = load_audio_file(audio_filename)
        transcription = transcribe_audio(audio_data)

        # Mettre à jour l'interface utilisateur avec la transcription
        self.transcription_label.text = transcription
        self.label.text = f'Recording finished and saved as {audio_filename}'

    def show_load(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView()
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