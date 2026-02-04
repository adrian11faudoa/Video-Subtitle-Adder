# Video Subtitle Adder

Arquitectura simple
Archivo de audio/video
        ↓
Whisper detecta japonés
        ↓
Traduce a inglés
        ↓
Genera archivo .srt
        ↓
UI permite seleccionar archivo y convertir

Instalar dependencias

En PowerShell (sé que usas PowerShell 👍):

pip install openai-whisper
pip install ffmpeg-python


Y necesitas FFmpeg instalado en Windows.



V1.2

Extrae audio del video
Convierte audio japonés → texto (Whisper)
Traduce japonés → inglés
Genera archivo .srt de subtítulos

(Agregar subtítulos al video final también se puede, pero primero generamos los subs — es como se hace profesionalmente).

🧠 Requisitos

Instala esto primero:

pip install openai-whisper moviepy deep-translator pysrt


También necesitas FFmpeg instalado:
👉 https://ffmpeg.org/download.html

