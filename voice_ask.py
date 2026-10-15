"""
SikshaSaathi - bolke poocho, jawab pao (one command).

    & d:/study_agent/.venv/Scripts/python.exe voice_ask.py "C:\\Users\\shubh\\Downloads\\my_question.ogg"

Needs both running:  ollama serve   and   uvicorn hub:app --port 8000
The Odia answer is saved to last_answer.txt (the terminal cannot show Odia letters properly).
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

import stt

HUB = "http://127.0.0.1:8000"
OUT = Path(__file__).resolve().parent / "last_answer.txt"


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: python voice_ask.py "path\\to\\recording.ogg"   [odia | sambalpuri_experimental | english]')
    audio = Path(sys.argv[1])
    answer_in = sys.argv[2] if len(sys.argv) > 2 else "odia"
    if not audio.exists():
        sys.exit(f"File not found: {audio}")

    print("1/2  Sun raha hoon (speech-to-text)...")
    heard = stt.transcribe(audio.read_bytes())
    print(f"     Suna (Roman): {heard['roman']}   [{heard['ms'] / 1000:.1f}s]")

    print("2/2  Jawab dhoondh raha hoon (pehli baar 1-3 minute lag sakte hain)...")
    body = json.dumps({"text": heard["odia"], "answer_in": answer_in}).encode("utf-8")
    req = urllib.request.Request(HUB + "/ask", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            res = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit("Hub mein /ask nahi mila: hub.py purana hai. Naya hub.py lagao aur uvicorn restart karo.")
        sys.exit(f"Hub error {e.code}: {e.read().decode('utf-8', 'ignore')}")
    except urllib.error.URLError:
        sys.exit("Hub se baat nahi ho payi. Kya 'uvicorn hub:app --port 8000' chal raha hai?")

    print("\n================ RESULT ================")
    print("Sawal (English):", res.get("question_english"))
    print("Topic          :", res.get("concept_title"))
    print("Jawab (Roman)  :", res.get("answer_roman") or res.get("answer"))
    print("Jawab (English):", res.get("answer_english"))
    print("Book pages     :", "; ".join(res.get("sources", [])))
    print("Kisne kya kiya :", " | ".join(res.get("trace", [])))
    print(f"Time           : {res.get('ms', 0) / 1000:.1f}s")

    OUT.write_text(
        f"SAWAL (suna):\n{heard['odia']}\n\nSAWAL (English):\n{res.get('question_english')}\n\n"
        f"JAWAB:\n{res.get('answer')}\n\nJAWAB (Roman):\n{res.get('answer_roman')}\n\n"
        f"JAWAB (English):\n{res.get('answer_english')}\n\nBOOK PAGES:\n" + "\n".join(res.get("sources", [])),
        encoding="utf-8")
    print(f"\nOdia jawab yahan save hua: {OUT.name}  (VS Code mein kholo)")


if __name__ == "__main__":
    main()
