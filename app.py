# Kolom Kanan untuk Generasi Audio (SUDAH DIPERBAIKI)
with col2:
    st.header("Buat Audio")
    with st.form("audio_form"):
        audio_prompt = st.text_area("Deskripsi audio yang diinginkan:", "Lagu rock epik dengan solo gitar listrik yang membara, tempo cepat.", height=150)
        duration_seconds = st.number_input("Durasi (detik):", min_value=1, max_value=45, value=10) # Max durasi bisa dinaikkan sedikit
        submitted_audio = st.form_submit_button("🎵 Buat Audio Sekarang!", use_container_width=True)

    if submitted_audio:
        if not STABILITY_API_KEY:
            st.error("Kunci API Stability tidak ditemukan! Harap konfigurasikan di Streamlit Secrets.")
        elif not audio_prompt:
            st.warning("Mohon masukkan deskripsi audio.")
        else:
            with st.spinner("AI sedang membuat audio... Mohon tunggu..."):
                try:
                    # Ini adalah data yang kita kirim
                    form_data = {
                        "prompt": audio_prompt,
                        "duration": str(duration_seconds),
                        "output_format": "wav"
                    }
                    
                    # Mengirim request ke URL API yang BARU
                    response = requests.post(
                        "https://api.stability.ai/v2beta/stable-audio/generate", # <<< INI BARIS YANG DIPERBAIKI
                        headers={
                            "authorization": f"Bearer {STABILITY_API_KEY}",
                            "Accept": "audio/*"
                        },
                        files={"none": ''}, # Diperlukan untuk multipart/form-data
                        data=form_data
                    )

                    if response.status_code == 200:
                        st.audio(response.content, format='audio/wav')
                        st.success("Audio berhasil dibuat!")
                    else:
                        # Pesan error akan lebih informatif sekarang
                        st.error(f"Gagal membuat audio: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
