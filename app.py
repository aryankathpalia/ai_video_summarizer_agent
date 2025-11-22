import streamlit as st
import os
import base64
import yt_dlp
import hashlib
from main import video_to_summary
from transcriber import extract_audio, transcribe_audio

# page config
st.set_page_config(page_title="Vistoria", page_icon="🎧", layout="wide")

# loading css
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# logo part
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64_image("assets/logo.png")

# header
st.markdown(
    f"""
<div class="header">
    <div class="header-left">
        <img 
            src="data:image/png;base64,{logo_base64}" 
            class="header-logo" 
            alt="Vistoria Logo"
        >
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# hero-section
st.markdown(
    """
<div class="hero-section">
    <h1 class="hero-title">Video Summarizer</h1>
    <div class="hero-subtext">
        <span class="hero-line line1">Transform any video into accurate text summaries instantly using Aivra’s AI video summarizer.</span>
        <span class="hero-line line2">Generate transcriptions, extract insights, and download summaries or transcripts — all in one click.</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# example section
examples_html = """
<style>
.examples { display:flex; gap:18px; justify-content:center; flex-wrap:wrap; margin:6px 0 10px; }
.example-card { width:230px; height:215px; background:#f4f4f4; border-radius:10px; overflow:hidden; cursor:pointer; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.06); }
.example-card img { width:100%; height:150px; object-fit:cover; border-bottom:1px solid #ddd; }
.example-card p { font-weight:600; padding:6px 8px; font-size:0.95rem; margin:0; }
.example-desc { display:block; font-size:0.8rem; color:#555; padding:0 8px 8px; }
.example-card:hover { transform: translateY(-3px); transition: transform 0.12s ease; }
</style>

<div class="examples">
  <div class="example-card" data-url="https://www.youtube.com/watch?v=RsdoJ9x8IBs">
    <img src="https://img.youtube.com/vi/RsdoJ9x8IBs/0.jpg" alt="Alan Watts">
    <p> Happiness ≠ Meaning - Alan Watts</p>
  </div>
  <div class="example-card" data-url="https://www.youtube.com/watch?v=LlT3O7DdDRM">
    <img src="https://img.youtube.com/vi/LlT3O7DdDRM/0.jpg" alt="Adam Leipzig">
    <p> Life Purpose — Adam Leipzig</p>
    <span class="example-desc">How to know your purpose in 2 minutes</span>
  </div>
  <div class="example-card" data-url="https://www.youtube.com/watch?v=ZmNpeXTj2c4">
    <img src="https://img.youtube.com/vi/ZmNpeXTj2c4/0.jpg" alt="Jenny Hoyos">
    <p> Storycraft — Jenny Hoyos</p>
    <span class="example-desc">The secret to telling a great story in 60s.</span>
  </div>
  <div class="example-card" data-url="https://www.youtube.com/watch?v=OqlfWDyS1Io">
    <img src="https://img.youtube.com/vi/OqlfWDyS1Io/0.jpg" alt="Naval">
    <p> The Modern Struggle - Naval Ravikant</p>
  </div>
</div>

<script>
(function() {
  function setNativeValue(element, value) {
    const valueSetter = Object.getOwnPropertyDescriptor(element.__proto__, 'value')?.set;
    const prototype = Object.getPrototypeOf(element);
    const valueSetter2 = Object.getOwnPropertyDescriptor(prototype, 'value')?.set;
    if (valueSetter && valueSetter2) {
      valueSetter.call(element, value);
      valueSetter2.call(element, value);
    } else {
      element.value = value;
    }
  }

  const waitForInput = setInterval(() => {
    const candidates = Array.from(window.parent.document.querySelectorAll('input[type="text"]'));
    let input = null;
    for (const c of candidates) {
      if (c.placeholder && c.placeholder.includes("Paste a video URL")) { input = c; break; }
    }
    if (!input && candidates.length === 1) input = candidates[0];
    if (input) {
      clearInterval(waitForInput);
      document.querySelectorAll('.example-card').forEach(card => {
        card.addEventListener('click', () => {
          const url = card.getAttribute('data-url');
          setNativeValue(input, url);
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
          input.scrollIntoView({ behavior: 'smooth', block: 'center' });
          input.focus();
          try { input.click(); } catch (e) {}
        });
      });
    }
  }, 250);
})();
</script>
"""

# custom upload box
def render_upload_box_default():
    st.markdown(
        """
    <style>
    [data-testid="stFileUploader"] { display: none !important; }
    .upload-box {
        border: 2px dashed #4CD3C2;
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        background-color: #F9FEFF;
        transition: 0.3s ease;
    }
    .upload-box:hover { background-color: #F1FAFB; border-color: #35BEB0; }
    .upload-btn { background-color: #17A589; color: white; padding: 12px 24px; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; margin-top: 10px; }
    .upload-btn:hover { background-color: #148F77; }
    </style>

    <div class="upload-box">
        <strong>📂 Drag & Drop or Upload Your File</strong>
        <p>Max 1GB per file • Supported formats: MP4, MOV, AVI, MKV</p>
        <button class="upload-btn" id="customUploadBtn">Upload Video</button>
    </div>
    """,
        unsafe_allow_html=True,
    )

def render_upload_box_with_filename(filename: str):
    st.markdown(
        f"""
    <div class="upload-box">
        <strong>✅ {filename}</strong>
        <p>File ready to process.</p>
        <button class="upload-btn" id="customUploadBtn">Change File</button>
    </div>
    """,
        unsafe_allow_html=True,
    )



def main():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)

    # Widget keys (read-only from session_state) 
    URL_WIDGET_KEY = "video_url_widget"       
    UPLOAD_WIDGET_KEY = "video_upload_widget" 

    # Ensure stable non-widget session keys exist
    if "last_url" not in st.session_state:
        st.session_state["last_url"] = ""
    if "last_uploaded_name" not in st.session_state:
        st.session_state["last_uploaded_name"] = ""
    if "active_mode" not in st.session_state:
        st.session_state["active_mode"] = None
    # file paths



    # example + url input
    with st.container():
        st.components.v1.html(examples_html, height=240, scrolling=False)
        # gave the widget a key, but will never write to st.session_state[URL_WIDGET_KEY]
        video_url = st.text_input(
            "",
            placeholder="Paste a video URL (YouTube, Vimeo, etc)",
            key=URL_WIDGET_KEY
        ).strip()


    # file uploader(read only)
    uploaded_file = st.file_uploader(
        "Upload Video",
        type=["mp4", "mov", "avi", "mkv"],
        label_visibility="collapsed",
        key=UPLOAD_WIDGET_KEY
    )


    # Mode detection & transition logic (pure session_state, no widget writes) 
    
    # If user typed a new URL (Enter or changed input), treat as URL action.
    if video_url:
        # If the URL changed since last run, treat that as the user pressing Enter/new URL input.
        if video_url != st.session_state["last_url"]:
            st.session_state["last_url"] = video_url
            st.session_state["active_mode"] = "url"
            # clear any previous url_video_path (we'll produce a fresh one on download)
            st.session_state.pop("url_video_path", None)

    # If user uploaded a new file (filename changed), treat it as upload action.
    if uploaded_file is not None:
        if uploaded_file.name != st.session_state.get("last_uploaded_name", ""):
            st.session_state["last_uploaded_name"] = uploaded_file.name
            st.session_state["active_mode"] = "upload"
            # clear any previous upload path (we'll create a fresh file below)
            st.session_state.pop("upload_video_path", None)

    mode = st.session_state.get("active_mode")
    prev_mode = None
    # previous mode for debug: try to infer from earlier run (optional)
    # we don't touch widget keys, so prev_mode is just informative
    prev_mode = st.session_state.get("_prev_active_mode", None)
    st.session_state["_prev_active_mode"] = mode



    # Render upload box UI (external helpers) 
    # Use the widget values to decide which UI to show
    if not uploaded_file:
        render_upload_box_default()
    else:
        render_upload_box_with_filename(uploaded_file.name) 

    # JS hook for custom upload button 
    st.components.v1.html("""
        <script>
        (function() {
            const interval = setInterval(() => {
                const input = window.parent.document.querySelector('input[type=file]');
                const btn = window.parent.document.getElementById('customUploadBtn');
                if (input && btn) {
                    btn.onclick = () => input.click();
                    clearInterval(interval);
                }
            }, 300);
        })();
        </script>
    """, height=0)

    # Handle URL mode: download when needed
    video_path = None
    if mode == "url" and video_url:
        # If we already downloaded this URL in an earlier run, reuse it.
        video_path = st.session_state.get("url_video_path")
        if not video_path or not os.path.exists(video_path):
            try:
                st.info("📥 Downloading video...")
                filename = hashlib.md5(video_url.encode()).hexdigest()[:10] + ".mp4"
                ydl_opts = {"outtmpl": filename, "format": "mp4/best", "quiet": True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                st.session_state["url_video_path"] = filename
                video_path = filename
                st.success("✅ Download complete!")
            except Exception as e:
                st.error(f"❌ Failed to download video: {e}")
                # keep app alive; don't write to widget keys
                video_path = None

    # Handle upload mode: save uploaded file to disk and persist path
    if mode == "upload" and uploaded_file:
        # If we already saved in this session, reuse
        upload_path = st.session_state.get("upload_video_path")
        if not upload_path or not os.path.exists(upload_path) or st.session_state.get("last_uploaded_name") == uploaded_file.name:
            try:
                filename = f"uploaded_{uploaded_file.name}"
                # write file to disk
                with open(filename, "wb") as f:
                    f.write(uploaded_file.read())
                st.session_state["upload_video_path"] = filename
                video_path = filename
                st.success("✅ Upload complete!")
            except Exception as e:
                st.error(f"❌ Failed to save uploaded file: {e}")
                video_path = None
        else:
            video_path = upload_path

    # Determine if video is ready 
    video_ready = video_path is not None and os.path.exists(video_path)

    # Action buttons 
    col1, col2 = st.columns(2)
    with col1:
        generate_transcript = st.button("📝 Generate Transcript", use_container_width=True, disabled=not video_ready)
    with col2:
        generate_summary = st.button("✨ Generate Summary", use_container_width=True, disabled=not video_ready)

    # Disabled style
    st.markdown("""
        <style>
        div.stButton > button:disabled {
            opacity: 0.5 !important;
            cursor: not-allowed !important;
            background-color: #d3d3d3 !important;
            color: #666 !important;
            border: 1px solid #ccc !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Processing 
    if video_ready:
        audio_path = f"{mode}_temp_audio.wav"

        if generate_transcript:
            with st.spinner("🎧 Extracting & transcribing..."):
                try:
                    extract_audio(video_path, audio_path)
                    transcript_text, transcript_path = transcribe_audio(audio_path, model_size="base", save_as_srt=False)
                    st.session_state[f"{mode}_transcript_text"] = transcript_text
                    st.session_state[f"{mode}_transcript_path"] = transcript_path
                    st.success("✅ Transcript ready!")
                except Exception as e:
                    st.error(f"❌ Transcript failed: {e}")

        if generate_summary:
            with st.spinner("✨ Generating summary..."):
                try:
                    transcript_text = st.session_state.get(f"{mode}_transcript_text")
                    if not transcript_text:
                        extract_audio(video_path, audio_path)
                        transcript_text, transcript_path = transcribe_audio(audio_path, model_size="base", save_as_srt=False)
                        st.session_state[f"{mode}_transcript_text"] = transcript_text
                        st.session_state[f"{mode}_transcript_path"] = transcript_path

                    summary = video_to_summary(video_path, "base", existing_transcript=transcript_text)
                    st.session_state[f"{mode}_summary_result"] = summary
                    st.success("✅ Summary complete!")
                except Exception as e:
                    st.error(f"❌ Summary failed: {e}")

        # Show results if present 
        if st.session_state.get(f"{mode}_summary_result"):
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.subheader("📄 Summary")
            st.write(st.session_state[f"{mode}_summary_result"])
            st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.get(f"{mode}_transcript_text"):
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.subheader("📝 Transcript")
            st.text_area("Transcript:", st.session_state[f"{mode}_transcript_text"], height=350)
            transcript_path = st.session_state.get(f"{mode}_transcript_path")
            if transcript_path and os.path.exists(transcript_path):
                with open(transcript_path, "rb") as f:
                    st.download_button(
                        "📥 Download Transcript",
                        f,
                        os.path.basename(transcript_path),
                        mime="text/plain",
                        key=f"download_{mode}"
                    )


# ENTRY POINT 
if __name__ == "__main__":
    main()
