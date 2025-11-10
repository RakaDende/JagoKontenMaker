# File: app.py

import streamlit as st
import os
import requests

# Mengambil API key dari secrets Streamlit
# Pastikan Anda sudah mengaturnya di pengaturan deploy Streamlit Anda
STABILITY_API_KEY = st.secrets.get("STABILITY_API_KEY")

# Konfigurasi halaman
st.set_page_config(page_title="Image & Audio Generator", layout="wide")
st.title("🎨🔊 AI Image and Audio Generator")
st.write("Powered by Stability AI (SD3 & Stable Audio)")

# Membuat tab untuk Image dan Audio
tab1, tab2 = st.tabs(["🖼️ Image Generation", "🎵 Audio Generation"])

# Tab Generasi Gambar
with tab1:
    st.header("Stable Diffusion 3 Image Generation")
    
    with st.form("image_form"):
        image_prompt = st.text_area("Enter your image prompt:", "A cat wearing a top hat, photorealistic, 4k")
        negative_prompt = st.text_area("Negative prompt (optional):", "blurry, low quality")
        aspect_ratio = st.selectbox("Aspect Ratio:", ["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16"], index=1)
        
        submitted_image = st.form_submit_button("Generate Image")

    if submitted_image:
        if not STABILITY_API_KEY:
            st.error("Stability API key not found! Please add it to your Streamlit secrets.")
        elif not image_prompt:
            st.warning("Please enter a prompt to generate an image.")
        else:
            with st.spinner("Generating your image... This may take a moment."):
                try:
                    response = requests.post(
                        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
                        headers={"authorization": f"Bearer {STABILITY_API_KEY}", "accept": "image/*"},
                        files={"none": ''},
                        data={
                            "prompt": image_prompt,
                            "negative_prompt": negative_prompt,
                            "aspect_ratio": aspect_ratio,
                            "output_format": "png",
                        },
                    )
                    
                    if response.status_code == 200:
                        st.image(response.content, caption="Generated Image", use_column_width=True)
                        st.success("Image generated successfully!")
                    else:
                        st.error(f"Error generating image: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

# Tab Generasi Audio
with tab2:
    st.header("Stable Audio Generation")

    with st.form("audio_form"):
        audio_prompt = st.text_area("Enter your audio prompt:", "A gentle acoustic guitar melody with birds chirping in the background")
        duration_seconds = st.number_input("Duration (seconds):", min_value=1, max_value=30, value=10)

        submitted_audio = st.form_submit_button("Generate Audio")

    if submitted_audio:
        if not STABILITY_API_KEY:
            st.error("Stability API key not found! Please add it to your Streamlit secrets.")
        elif not audio_prompt:
            st.warning("Please enter a prompt to generate audio.")
        else:
            with st.spinner("Generating your audio... Please wait."):
                try:
                    response = requests.post(
                        "https://api.stability.ai/v1/generation/stable-audio-generate",
                        headers={"authorization": f"Bearer {STABILITY_API_KEY}"},
                        json={
                            "text": audio_prompt,
                            "model_id": "stable-audio-1.0",
                            "duration_seconds": duration_seconds,
                        }
                    )

                    if response.status_code == 200:
                        # Simpan audio ke file sementara untuk diputar
                        audio_filename = "output_audio.wav"
                        with open(audio_filename, "wb") as f:
                            f.write(response.content)
                        
                        st.audio(audio_filename)
                        st.success("Audio generated successfully!")
                    else:
                        st.error(f"Error generating audio: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")