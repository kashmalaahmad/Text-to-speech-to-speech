# PDF to Audiobook Generator

This application is a **Streamlit-based tool** that converts PDF documents into audiobooks. It offers two primary modes of speech synthesis: a standard text-to-speech engine for quick results and a voice cloning feature (via Coqui TTS) for a personalized audio experience.

---

## Features

* **PDF Text Extraction:** Seamlessly extracts and cleans text from uploaded PDF files.
* **Dual Speech Modes:**
* **Default (gTTS):** Lightweight and fast text-to-speech engine.
* **Cloned Voice (Coqui TTS):** Uses XTTS v2 to clone a provided voice sample for a more natural, personalized narration.


* **Chunking Logic:** Automatically splits long documents into manageable segments to ensure processing reliability.
* **Multi-language Support:** Supports English, Spanish, and French.
* **Downloadable Audio:** Provides an easy interface to listen to or download the generated audio file.

---

## Getting Started

### Prerequisites

* Python 3.9+
* `ffmpeg` must be installed on your system (required for audio processing with `pydub`).

### Installation

1. **Clone the repository** (or save the code to your local machine).
2. **Install the required dependencies:**
```bash
pip install streamlit pdfplumber gTTS pydub TTS torch

```


*Note: `TTS` and `torch` are only strictly necessary if you intend to use the Cloned Voice feature.*

### Running the Application

Execute the following command in your terminal:

```bash
streamlit run app.py

```

---

## How to Use

1. **Upload PDF:** Select the PDF file you wish to convert.
2. **Select Mode:**
* **Default:** Choose this for standard text-to-speech.
* **Cloned Voice:** Choose this to upload a 3-10 second `.wav` file as a reference for voice cloning.


3. **Select Language:** Choose your preferred language from the dropdown menu.
4. **Generate:** Click the **"Generate Audiobook"** button.
5. **Download:** Once processing is complete, you can play the audio directly in your browser or download the file.

---

## ⚙️ Technical Notes

* **Temporary Storage:** The app utilizes `/tmp/` for processing. Ensure your operating system has sufficient permissions for read/write operations in that directory.
* **Performance:** For the best voice cloning results, ensure the uploaded voice sample is clear, high-quality, and does not contain background noise.
* **Environment:** The app includes a patch for `torch.load` to ensure compatibility with modern security settings while using the Coqui TTS engine.
