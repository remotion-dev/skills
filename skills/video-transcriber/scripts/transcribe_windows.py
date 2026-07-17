# transcribe_windows.py
# Local Windows transcription using faster-whisper (CPU, int8).
# Handles both local file paths and URLs (yt-dlp downloads audio first for URLs).
#
# Usage from PowerShell:
#   python transcribe_windows.py "C:\path\to\video.mp4"
#   python transcribe_windows.py "https://www.youtube.com/watch?v=..."
#   python transcribe_windows.py "C:\path\to\video.mp4" --model small.en --timestamps
#
# Why faster-whisper instead of openai-whisper:
#   - 4-10x faster on CPU
#   - Smaller install (no PyTorch dependency)
#   - Same accuracy
# Why int8 quantization:
#   - Roughly 2x faster on CPU vs fp32 with negligible quality loss for English speech

import argparse
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import timedelta

# Graeham's ffmpeg location. Adjust if it moves.
FFMPEG_DIR = r"C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\ffmpegvideoprocessingengine\bin"


def ensure_ffmpeg_on_path():
    """faster-whisper shells out to ffmpeg to decode audio. Add it to PATH if not visible."""
    if FFMPEG_DIR and os.path.isdir(FFMPEG_DIR):
        if FFMPEG_DIR not in os.environ.get("PATH", ""):
            os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")


def is_url(s: str) -> bool:
    return s.lower().startswith(("http://", "https://"))


def download_audio_with_ytdlp(url: str, tmpdir: str) -> str:
    """For URL inputs: pull just the audio track to a temp mp3 with yt-dlp."""
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        print("[*] Installing yt-dlp (one-time)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "--quiet"])

    out_template = os.path.join(tmpdir, "audio.%(ext)s")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", out_template,
        "--quiet", "--no-warnings",
        url,
    ]
    print(f"[*] Downloading audio from URL...")
    subprocess.check_call(cmd)
    audio_path = os.path.join(tmpdir, "audio.mp3")
    if not os.path.exists(audio_path):
        raise RuntimeError("yt-dlp completed but no audio.mp3 was produced")
    return audio_path


def slugify(name: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-")
    return base[:80] if base else "transcript"


def transcribe(source: str, model_size: str, output_dir: str, with_timestamps: bool):
    ensure_ffmpeg_on_path()

    # Resolve source to a local audio/video path
    tmpdir_obj = None
    if is_url(source):
        tmpdir_obj = tempfile.TemporaryDirectory()
        audio_path = download_audio_with_ytdlp(source, tmpdir_obj.name)
        source_label = source
        slug = slugify(source.split("/")[-1] or "url")
    else:
        if not os.path.exists(source):
            print(f"[!] ERROR: file not found: {source}")
            sys.exit(1)
        audio_path = source
        source_label = os.path.basename(source)
        slug = slugify(os.path.splitext(os.path.basename(source))[0])

    size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"[*] Source: {source_label}")
    print(f"[*] Size: {size_mb:.1f} MB")
    print(f"[*] Model: {model_size} (int8 quantization, CPU)")
    print(f"[*] Loading faster-whisper... (first run downloads the model)")

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[!] faster-whisper not installed. Run:  pip install faster-whisper")
        sys.exit(1)

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print(f"[*] Model loaded. Starting transcription...")

    start = time.time()
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    print(f"[*] Detected language: {info.language} (confidence: {info.language_probability:.2f})")
    print(f"[*] Audio duration: {timedelta(seconds=int(info.duration))} ({info.duration/60:.1f} min)")

    all_segments = []
    for i, seg in enumerate(segments):
        all_segments.append(seg)
        if i % 20 == 0:
            elapsed = time.time() - start
            progress = seg.end / info.duration * 100
            eta = (elapsed / max(seg.end, 1)) * (info.duration - seg.end)
            print(f"    [{progress:5.1f}%]  t={timedelta(seconds=int(seg.end))}  elapsed={int(elapsed)}s  eta~{int(eta)}s")

    elapsed = time.time() - start
    print(f"[*] Transcription complete in {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"[*] Got {len(all_segments)} segments")

    # Write outputs
    os.makedirs(output_dir, exist_ok=True)
    plain_path = os.path.join(output_dir, f"{slug}_transcript.txt")
    ts_path = os.path.join(output_dir, f"{slug}_transcript_timestamped.txt")

    with open(plain_path, "w", encoding="utf-8") as f:
        f.write(f"Transcript: {source_label}\n")
        f.write(f"Duration: {timedelta(seconds=int(info.duration))}\n")
        f.write(f"Language: {info.language}\n")
        f.write(f"Model: faster-whisper {model_size} (int8)\n")
        f.write("=" * 70 + "\n\n")
        para = []
        for i, seg in enumerate(all_segments):
            para.append(seg.text.strip())
            if (i + 1) % 5 == 0:
                f.write(" ".join(para) + "\n\n")
                para = []
        if para:
            f.write(" ".join(para) + "\n")

    if with_timestamps:
        with open(ts_path, "w", encoding="utf-8") as f:
            f.write(f"Transcript (timestamped): {source_label}\n")
            f.write("=" * 70 + "\n\n")
            for seg in all_segments:
                start_str = str(timedelta(seconds=int(seg.start)))
                f.write(f"[{start_str}] {seg.text.strip()}\n")

    print(f"\n[OK] Plain transcript:        {plain_path}")
    if with_timestamps:
        print(f"[OK] Timestamped transcript:  {ts_path}")
    print(f"\nDone.")

    if tmpdir_obj:
        tmpdir_obj.cleanup()


def main():
    p = argparse.ArgumentParser(description="Local Windows transcription using faster-whisper")
    p.add_argument("source", help="Local file path OR URL")
    p.add_argument("--model", default="base.en",
                   help="Model size. base.en (default, fast), small.en (slower, more accurate), medium.en (slowest, best)")
    p.add_argument("--output-dir", default=None,
                   help="Where to write transcript .txt files. Default: same folder as input.")
    p.add_argument("--timestamps", action="store_true",
                   help="Also write a timestamped version")
    args = p.parse_args()

    if args.output_dir is None:
        if is_url(args.source):
            args.output_dir = os.getcwd()
        else:
            args.output_dir = os.path.dirname(os.path.abspath(args.source))

    transcribe(args.source, args.model, args.output_dir, args.timestamps)


if __name__ == "__main__":
    main()
