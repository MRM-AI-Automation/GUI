import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        pass

    def transform(self, frame):
        return frame

def main():
    st.title("Rover Camera Feed")

    webrtc_streamer(
        key="example",
        video_transformer_factory=VideoTransformer,
        async_transform=True,
    )

if __name__ == "__main__":
    main()
