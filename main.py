from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from pytube import YouTube
from pytube.exceptions import *
import ssl

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

class YouTubeDownloaderApp(App):
    def build(self):
        self.title = "YouTube Downloader"
        self.root = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # URL input
        self.url_label = Label(text="YouTube Video URL:")
        self.url_input = TextInput(multiline=False)
        self.root.add_widget(self.url_label)
        self.root.add_widget(self.url_input)

        # Download path input
        self.path_label = Label(text="Download Path:")
        self.path_input = TextInput(multiline=False)
        self.root.add_widget(self.path_label)
        self.root.add_widget(self.path_input)

        # Browse button for selecting download path
        self.browse_button = Button(text="Browse", on_press=self.browse_callback)
        self.root.add_widget(self.browse_button)

        # Download button
        self.download_button = Button(text="Download", on_press=self.download_video)
        self.root.add_widget(self.download_button)

        return self.root

    def browse_callback(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.file_chosen)
        self.root.add_widget(file_chooser)

    def file_chosen(self, chooser, selected_path, touch):
        self.root.remove_widget(chooser)  # Remove file chooser after selection
        self.path_input.text = selected_path

    def download_video(self, instance):
        video_url = self.url_input.text
        download_path = self.path_input.text if self.path_input.text else "."

        try:
            # Validate the URL
            if not video_url.startswith("https://www.youtube.com/watch?v="):
                raise ValueError("Invalid URL. Make sure it is a valid YouTube video URL.")

            # Create a YouTube object using the video URL
            yt = YouTube(video_url)

            # Select the highest available resolution
            video = yt.streams.get_highest_resolution()

            # Display information about the video
            info_text = f"Downloading video: {yt.title}\nResolution: {video.resolution}\nFormat: {video.mime_type}"
            self.show_info(info_text)

            # Download the video to the specified folder
            video.download(download_path)
            success_text = f"Download completed. Video saved at {download_path}"
            self.show_info(success_text)

        except RegexMatchError:
            self.show_error("Error: Unable to extract video information.")
        except VideoUnavailable:
            self.show_error("Error: The video is unavailable.")
        except ValueError as ve:
            self.show_error(f"Error: {ve}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {e}")

    def show_info(self, text):
        info_label = Label(text=text, color=(0, 1, 0, 1))  # Green text for info
        self.root.add_widget(info_label)

    def show_error(self, text):
        error_label = Label(text=text, color=(1, 0, 0, 1))  # Red text for errors
        self.root.add_widget(error_label)

if __name__ == "__main__":
    YouTubeDownloaderApp().run()
