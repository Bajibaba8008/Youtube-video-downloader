import streamlit as st
from pytube import YouTube
import os

# Download function
def download_video(url, choice):
    try:
        yt = YouTube(url)

        # Display video details
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Author:** {yt.author}")
        st.write(f"**Views:** {yt.views}")
        st.write(f"**Length:** {yt.length // 60} minutes {yt.length % 60} seconds")
        st.write(f"**Rating:** {yt.rating}")

        # Choose download option
        if choice == 'Highest Resolution':
            stream = yt.streams.get_highest_resolution()
        elif choice == 'Choose Resolution':
            video_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            resolutions = [stream.resolution for stream in video_streams]
            selected_resolution = st.selectbox("Select Resolution", resolutions)
            stream = yt.streams.filter(res=selected_resolution, file_extension='mp4').first()
        elif choice == 'Audio Only':
            stream = yt.streams.filter(only_audio=True).first()

        # Download
        with st.spinner("Downloading..."):
            file_path = stream.download()

        # Rename if audio
        if choice == 'Audio Only':
            base, ext = os.path.splitext(file_path)
            new_file = base + '.mp3'
            os.rename(file_path, new_file)
            st.success("Audio downloaded successfully!")
        else:
            st.success("Video downloaded successfully!")

    except Exception as e:
        st.error(f"An error occurred: {e}")


# Streamlit Interface
st.title("🎥 YouTube Video Downloader")
video_url = st.text_input("Enter the YouTube Video URL")

option = st.radio(
    "Choose download option:",
    ('Highest Resolution', 'Choose Resolution', 'Audio Only')
)

if st.button("Download"):
    if video_url:
        download_video(video_url, option)
    else:
        st.warning("Please enter a valid YouTube URL.")
