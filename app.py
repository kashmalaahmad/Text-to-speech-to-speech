import streamlit as st
import pdfplumber
from gtts import gTTS
from TTS.api import TTS
from pydub import AudioSegment
import os


def pull_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            all_text += page_text
    all_text = " ".join(all_text.split())
    return all_text

def split_into_chunks(text, max_chars=500):
    chunks = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    return chunks


def make_speech_from_chunks(text_chunks, language="en"):
    audio_files = []
    for idx, chunk in enumerate(text_chunks):
        tts = gTTS(text=chunk, lang=language)
        temp_file = f"temp_{idx}.mp3"
        tts.save(temp_file)
        audio_files.append(temp_file)
    return audio_files

def stitch_audio_files(audio_files, output_path="default_audiobook.mp3"):
    combined_sound = AudioSegment.empty()
    for audio in audio_files:
        sound_clip = AudioSegment.from_mp3(audio)
        combined_sound += sound_clip
        os.remove(audio)  # Clean up
    combined_sound.export(output_path, format="mp3")
    return output_path


def clone_text_chunks_to_audiobook(text_chunks, voice_sample_path, output_path="cloned_audiobook.wav", language="en"):
    model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    audio_chunks = []
    for i, chunk in enumerate(text_chunks):
        temp_wav = f"cloned_temp_chunk_{i}.wav"
        try:
            model.tts_to_file(text=chunk, speaker_wav=voice_sample_path, language=language, file_path=temp_wav)
            audio_chunks.append(temp_wav)
        except Exception as e:
            st.error(f"Error processing chunk {i}: {e}")
    if audio_chunks:
        combined = AudioSegment.empty()
        for chunk in audio_chunks:
            combined += AudioSegment.from_wav(chunk)
            os.remove(chunk)
        combined.export(output_path, format="wav")
        return output_path
    return None

st.title("PDF to Audiobook Generator")
st.write("Upload a PDF book to create an audiobook. For cloned voice, upload a voice sample.")

pdf_file = st.file_uploader("Upload PDF Book", type="pdf")
voice_mode = st.radio("Select Voice Mode", ("Default Voice (gTTS)", "Cloned Voice (Coqui TTS)"))
voice_sample = None
if voice_mode == "Cloned Voice (Coqui TTS)":
    voice_sample = st.file_uploader("Upload Voice Sample (WAV, 3-10 seconds)", type="wav")
language = st.selectbox("Select Language", ["en", "es", "fr"])

if st.button("Generate Audiobook"):
    if pdf_file:
       
        pdf_path = "temp_book.pdf"
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())
        
       
        with st.spinner("Extracting text from PDF..."):
            text = pull_text_from_pdf(pdf_path)
            text_chunks = split_into_chunks(text)
        
        output_path = None
        if voice_mode == "Default Voice (gTTS)":
            with st.spinner("Generating audiobook in default voice..."):
                audio_files = make_speech_from_chunks(text_chunks, language=language)
                output_path = stitch_audio_files(audio_files, "default_audiobook.mp3")
        else:  
            if voice_sample:
                voice_path = "temp_voice.wav"
                with open(voice_path, "wb") as f:
                    f.write(voice_sample.read())
                with st.spinner("Generating audiobook in cloned voice..."):
                    output_path = clone_text_chunks_to_audiobook(text_chunks, voice_path, "cloned_audiobook.wav", language=language)
                os.remove(voice_path)
            else:
                st.error("Please upload a voice sample for cloned voice.")
        
        if output_path and os.path.exists(output_path):
            st.success(f"Audiobook generated successfully in {voice_mode}!")
            audio_format = "audio/mp3" if output_path.endswith(".mp3") else "audio/wav"
            st.audio(output_path, format=audio_format)
            with open(output_path, "rb") as f:
                file_name = os.path.basename(output_path)
                st.download_button("Download Audiobook", f.read(), file_name=file_name)
            os.remove(pdf_path)
            os.remove(output_path)
        else:
            st.error("Failed to generate audiobook.")
    else:
        st.error("Please upload a PDF.")

st.write("*Note*: Large PDFs may take longer to process. Ensure your voice sample is clear and 3-10 seconds long for cloned voice.")