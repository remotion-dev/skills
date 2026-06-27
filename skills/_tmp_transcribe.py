import os, sys

# ffmpeg on PATH
ff = r"C:\Users\Graeham Watts\Documents\Claude\ffmpegvideoprocessingengine\bin"
os.environ["PATH"] = ff + os.pathsep + os.environ.get("PATH", "")

# Try to add NVIDIA CUDA DLLs (GPU path)
def add_nvidia_dlls():
    try:
        import importlib.util
        for pkg in ["nvidia.cublas.bin", "nvidia.cudnn.bin", "nvidia.cuda_runtime.bin"]:
            try:
                mod = __import__(pkg, fromlist=["x"])
                p = os.path.dirname(mod.__file__)
                if os.path.isdir(p):
                    os.add_dll_directory(p)
            except Exception:
                pass
    except Exception:
        pass

add_nvidia_dlls()

from faster_whisper import WhisperModel

def load_model():
    try:
        m = WhisperModel("large-v3", device="cuda", compute_type="float16")
        print("MODEL: large-v3 on CUDA (float16)", file=sys.stderr)
        return m
    except Exception as e:
        print(f"CUDA failed ({e}); falling back to CPU base.en", file=sys.stderr)
        return WhisperModel("base.en", device="cpu", compute_type="int8")

model = load_model()

for path in sys.argv[1:]:
    print("\n" + "=" * 70)
    print(f"TRANSCRIPT: {os.path.basename(path)}")
    print("=" * 70)
    segments, info = model.transcribe(path, vad_filter=True, beam_size=5)
    print(f"[lang={info.language}, dur={info.duration:.1f}s]\n", file=sys.stderr)
    for seg in segments:
        m, s = divmod(int(seg.start), 60)
        print(f"[{m:02d}:{s:02d}] {seg.text.strip()}")
