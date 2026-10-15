"""
SikshaSaathi - speech-to-text (used by hub.py's /stt).

Swappable: to try a better model later, change load_model() only.
Model: IndicConformer Odia (AI4Bharat, MIT licence), ONNX int8, runs on CPU, offline.
It is trained on ODIA, not Sambalpuri - test with real Sambalpuri speakers.

Expects the model files in  D:\\study_agent\\models\\asr-or
(download once with:  python stt.py --download)
"""
import io
import os
import sys
import time
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
MODEL_DIR = BASE / "models" / "asr-or"
MODEL_REPO = "OpenVoiceOS/ai4bharat-indicconformer-or-onnx"
MAX_SECONDS = 25          # the model handles about 20-30 s at once
_model = None


def available() -> bool:
    return (MODEL_DIR / "model.int8.onnx").exists()


def load_model():
    global _model
    if _model is None:
        import onnx_asr
        _model = onnx_asr.load_model("nemo-conformer-ctc", str(MODEL_DIR), quantization="int8")
    return _model


def decode_audio(data: bytes) -> np.ndarray:
    """Any browser/phone recording (webm, ogg, m4a, mp3, wav) -> 16 kHz mono float32."""
    import av
    chunks = []
    with av.open(io.BytesIO(data)) as container:
        resampler = av.AudioResampler(format="flt", layout="mono", rate=16000)
        for frame in container.decode(audio=0):
            for out in resampler.resample(frame):
                chunks.append(out.to_ndarray().reshape(-1))
        for out in resampler.resample(None):            # flush
            chunks.append(out.to_ndarray().reshape(-1))
    if not chunks:
        raise ValueError("no audio found in the file")
    return np.concatenate(chunks).astype(np.float32)


def to_roman(odia: str) -> str:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    return transliterate(odia, sanscript.ORIYA, sanscript.ITRANS)


def transcribe(data: bytes) -> dict:
    t0 = time.time()
    wave = decode_audio(data)
    seconds = len(wave) / 16000
    if seconds < 0.3:
        raise ValueError("recording is too short - please speak again")
    if seconds > MAX_SECONDS:
        wave = wave[: MAX_SECONDS * 16000]
    text = load_model().recognize(wave, sample_rate=16000).strip()
    return {
        "odia": text,
        "roman": to_roman(text) if text else "",
        "audio_seconds": round(min(seconds, MAX_SECONDS), 1),
        "cut_to_25s": seconds > MAX_SECONDS,
        "model": "indicconformer-or-int8",
        "ms": round((time.time() - t0) * 1000),
    }


def download():
    os.environ.pop("HF_HUB_OFFLINE", None)
    from huggingface_hub import snapshot_download
    print(f"Downloading {MODEL_REPO} into {MODEL_DIR} ...")
    snapshot_download(repo_id=MODEL_REPO, local_dir=str(MODEL_DIR),
                      allow_patterns=["config.json", "vocab.txt", "model.int8.onnx", "README.md"])
    print("Done." if available() else "Something went wrong - model.int8.onnx is missing.")


if __name__ == "__main__":
    if "--download" in sys.argv:
        download()
    elif len(sys.argv) > 1:                     # python stt.py my_recording.m4a
        print(transcribe(Path(sys.argv[1]).read_bytes()))
    else:
        print("Usage:  python stt.py --download   |   python stt.py recording.wav")
