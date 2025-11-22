import subprocess
import whisper
import os

# subprocess executes shell commands
def extract_audio(video_path: str, audio_path: str = "temp.audio.wav") -> str:
    # If audio already exists, delete it
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # Always extract new audio
    command = [
        "ffmpeg",
        "-i", video_path,
        "-q:a", "0",
        "-map", "a", audio_path,
        "-y"
    ]

    # Run the ffmpeg command
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return audio_path
    
# Transcribes audio -> returns transcript text + saves to file
def transcribe_audio(audio_path: str, model_size: str = "base", save_as_srt: bool = False):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)

    transcript_text = result["text"].strip()
    segments = result.get("segments", [])

    # Always use SRT timestampformat both for preview and download
    formatted_transcript = ""
    for i, segment in enumerate(segments):
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        segment_text = segment['text'].strip()

        formatted_transcript += f"{i}\n{start_time} --> {end_time}\n{segment_text}\n\n" 
   
    # Save transcript to file
    if save_as_srt:
        transcript_path = "transcript.srt"
    else:
        transcript_path = "transcript.txt"

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(formatted_transcript)

    return transcript_text, transcript_path


    # Helper to format timestamp in HH:MM:SS,mmm for SRT
def format_timestamp(seconds: float) -> str:
    millisec = int((seconds % 1) * 1000)
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

 

