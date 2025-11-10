# File: app.py (Versi dengan Kustomisasi Tampilan)

import streamlit as st
import requests

# ------------------- KODE CSS UNTUK TAMPILAN BARU -------------------
# Kode ini akan mengubah tampilan default Streamlit
# menjadi lebih modern dan mirip desain Google.
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Definisikan CSS dalam sebuah string
# Anda bisa bereksperimen dengan mengubah nilai-nilai di sini (misal: warna, ukuran)
css = """
<style>
    /* Mengubah font utama aplikasi */
    html, body, [class*="st-"] {
        font-family: 'Roboto', sans-serif;
    }

    /* Kustomisasi container utama */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        border-radius: 20px;
    }

    /* Kustomisasi Header/Judul */
    h1 {
        font-size: 2.5rem;
        color: #202124; /* Warna abu-abu gelap Google */
    }
    
    h2, h3 {
        color: #3c4043;
    }

    /* Kustomisasi Form Container */
    [data-testid="stForm"] {
        background-color: #F8F9FA; /* Warna latar belakang form sedikit abu-abu */
        border: 1px solid #DADCE0; /* Border halus */
        border-radius: 12px; /* Sudut lebih tumpul */
        padding: 20px;
    }

    /* Kustomisasi Tombol Submit */
    [data-testid="stFormSubmitButton"] button {
        background-color: #1a73e8; /* Warna biru Google */
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #185abc;
        box-shadow: 0 1px 3px 1px rgba(60,64,67,0.15);
    }
    
    /* Kustomisasi Kotak Input Teks */
    .stTextInput, .stTextArea {
        border-radius: 8px;
    }

    /* Memberi bayangan pada gambar hasil generasi */
    [data-testid="stImage"] img {
        border-radius: 12px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 6px 20px 0 rgba(0, 0, 0, 0.1);
    }
    
    /* Memberi bayangan pada pemutar audio */
    [data-testid="stAudio"] {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1);
        border-radius: 50px; /* Membuat pemutar audio lebih modern */
    }

</style>
"""

# ------------------- AKHIR DARI KODE CSS -------------------


# --- LOGIKA APLIKASI ANDA (TETAP SAMA) ---

# Mengambil API key dari secrets
STABILITY_API_KEY = st.secrets.get("STABILITY_API_KEY")

# Mengaplikasikan CSS ke halaman
st.markdown(css, unsafe_allow_html=True)

# Konfigurasi Halaman dan Judul
st.set_page_config(page_title="Jago Konten Maker", page_icon="✨", layout="wide")
st.title("🎨🔊 Jago Konten Maker")
st.write("Ditenagai oleh AI dari Stability.ai, didesain ulang untuk tampilan yang lebih modern.")
st.markdown("---")

# Membuat dua kolom untuk tata letak yang lebih baik
col1, col2 = st.columns(2, gap="large")

# Kolom Kiri untuk Generasi Gambar
with col1:
    st.header("Buat Gambar")
    with st.form("image_form"):
        image_prompt = st.text_area("Deskripsi gambar yang diinginkan:", "Seekor anjing golden retriever memakai topi koki, sedang memasak pancake, gaya foto studio.", height=150)
        negative_prompt = st.text_area("Hal yang dihindari (opsional):", "kartun, 3d, buram")
        aspect_ratio = st.selectbox("Rasio Aspek:", ["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16"], index=1)
        submitted_image = st.form_submit_button("✨ Buat Gambar Sekarang!", use_container_width=True)

    if submitted_image:
        if not STABILITY_API_KEY:
            st.error("Kunci API Stability tidak ditemukan! Harap konfigurasikan di Streamlit Secrets.")
        elif not image_prompt:
            st.warning("Mohon masukkan deskripsi gambar.")
        else:
            with st.spinner("AI sedang menggambar... Mohon tunggu..."):
                try:
                    response = requests.post(
                        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
                        headers={"authorization": f"Bearer {STABILITY_API_KEY}", "accept": "image/*"},
                        files={"none": ''},
                        data={"prompt": image_prompt, "negative_prompt": negative_prompt, "aspect_ratio": aspect_ratio, "output_format": "png"},
                    )
                    if response.status_code == 200:
                        st.image(response.content, caption="Gambar berhasil dibuat!", use_column_width=True)
                    else:
                        st.error(f"Gagal membuat gambar: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# Kolom Kanan untuk Generasi Audio
with col2:
    st.header("Buat Audio")
    with st.form("audio_form"):
        audio_prompt = st.text_area("Deskripsi audio yang diinginkan:", "Lagu rock epik dengan solo gitar listrik yang membara, tempo cepat.", height=150)
        duration_seconds = st.number_input("Durasi (detik):", min_value=1, max_value=30, value=10)
        submitted_audio = st.form_submit_button("🎵 Buat Audio Sekarang!", use_container_width=True)

    if submitted_audio:
        if not STABILITY_API_KEY:
            st.error("Kunci API Stability tidak ditemukan! Harap konfigurasikan di Streamlit Secrets.")
        elif not audio_prompt:
            st.warning("Mohon masukkan deskripsi audio.")
        else:
            with st.spinner("AI sedang membuat audio... Mohon tunggu..."):
                try:
                    response = requests.post(
                        "https://api.stability.ai/v2beta/stable-audio/generate"",
                        headers={"authorization": f"Bearer {STABILITY_API_KEY}"},
                        json={"text": audio_prompt, "model_id": "stable-audio-1.0", "duration_seconds": duration_seconds}
                    )
                    if response.status_code == 200:
                        st.audio(response.content, format='audio/wav')
                        st.success("Audio berhasil dibuat!")
                    else:
                        st.error(f"Gagal membuat audio: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
