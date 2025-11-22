import os
from transcriber import extract_audio, transcribe_audio
from summarizer import summarize_text

def video_to_summary(
        video_path: str,
        model_size: str = "base",
        existing_transcript: str | None = None
) -> str:
    """
    Generates a summary from a video file.
    - If `existing_transcript` is provided, uses that directly (skips re-transcription).
    - Otherwise, extracts audio and performs transcription automatically.
    """

    audio_path = "temp_audio.wav"

    # Step 1: Get transcript (use existing or create new)
    if existing_transcript is None:
        extract_audio(video_path, audio_path)
        transcript_text, _ = transcribe_audio(audio_path, model_size=model_size)
        # Cleanup temp audio
        if os.path.exists(audio_path):
            os.remove(audio_path)
    else:
        transcript_text = existing_transcript

    # Step 2: Summarize transcript using Groq
    final_summary = summarize_text(transcript_text)

    return final_summary


if __name__ == "__main__":
    # Example usage
    video_file = "example_video.mp4"
    summary_output = video_to_summary(
        video_path=video_file,
        model_size="base"
    )
    print("Final Summary:")
    print(summary_output)
