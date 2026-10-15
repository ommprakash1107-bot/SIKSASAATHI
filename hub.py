"""
SikshaSaathi HUB - step 2 + 3: /health and /brain

Put this file in D:\\study_agent (next to tutor.py), then run in the VS Code terminal:

    & d:/study_agent/.venv/Scripts/python.exe -m uvicorn hub:app --port 8000

Open http://localhost:8000/docs in the browser to try every endpoint.

It REUSES your code: concept graph, find_topic, book index and model all come from tutor.py,
and /brain "answer" is the same logic as ask.py. Nothing in tutor.py or ask.py is changed.

If Ollama is off, every job still answers using simple rules ("brain": "rules"),
so the phone app never breaks - this is the slide's "AI off" fallback.
"""
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import re
import time
from typing import Literal, Optional

import ollama
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import tutor   # your file: loads G (63 concepts), the book index and the embedder
import stt     # speech-to-text (stt.py)
import math
from collections import Counter

MODEL = os.environ.get("HUB_MODEL", tutor.MODEL)          # qwen2.5:3b, or set HUB_MODEL=gemma4:e2b
TRANSLATE_MODEL = os.environ.get("HUB_TRANSLATE_MODEL", "gemma4:e2b")   # Odia <-> English
HUB_TOKEN = os.environ.get("HUB_TOKEN", "")               # empty = no password (OK while testing)
LLM_TIMEOUT = float(os.environ.get("HUB_LLM_TIMEOUT", "180"))
llm = ollama.Client(timeout=LLM_TIMEOUT)

app = FastAPI(title="SikshaSaathi Hub", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ------------------------------------------------------------------ helpers
def check_token(token: Optional[str]):
    if HUB_TOKEN and token != HUB_TOKEN:
        raise HTTPException(status_code=401, detail="Wrong or missing X-Hub-Token")


def ask_llm(prompt: str, model: Optional[str] = None) -> str:
    r = llm.chat(model=model or MODEL, options={"temperature": 0},
                 messages=[{"role": "user", "content": prompt}])
    text = r["message"]["content"]
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)   # drop any "thinking" text
    return text.strip()


def ollama_ok() -> bool:
    try:
        llm.list()
        return True
    except Exception:
        return False


def concept(cid: str) -> dict:
    if cid not in tutor.G:
        raise HTTPException(status_code=404, detail=f"Unknown concept_id '{cid}'")
    return tutor.G[cid]


def words(s: str) -> set:
    return {w for w in re.findall(r"[a-z0-9']+", s.lower()) if len(w) > 2}


def rules_verdict(expected: str, answer: str) -> str:
    """No-AI marking: how many key words of the expected answer did the student use?"""
    exp, got = words(expected), words(answer)
    if not exp or not got:
        return "wrong"
    overlap = len(exp & got) / len(exp)
    return "correct" if overlap >= 0.6 else "partial" if overlap >= 0.3 else "wrong"
# ------------------------------------------------------------------ BM25 (port of the TypeScript one)
BM_STOP = set("kya hai hain hota ka ki ke me mein aur what is the how why explain".split())


def bm_tokenize(text: str) -> list:
    toks = re.findall(r"\w+", (text or "").lower())
    return [t for t in toks if t not in BM_STOP and (len(t) > 1 or t.isdigit())]


class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.docs, self.k1, self.b = docs, k1, b
        self.toks = [bm_tokenize(d["text"]) for d in docs]
        self.counts = [Counter(t) for t in self.toks]
        self.N = len(docs)
        self.avg_len = (sum(len(t) for t in self.toks) / max(1, self.N)) or 1
        self.df = Counter()
        for t in self.toks:
            self.df.update(set(t))

    def search(self, query: str):
        q = set(bm_tokenize(query))
        hits = []
        for i, d in enumerate(self.docs):
            score = 0.0
            for w in q:
                f = self.counts[i].get(w, 0)
                if not f:
                    continue
                n = self.df.get(w, 0)
                idf = math.log(1 + (self.N - n + 0.5) / (n + 0.5))
                score += idf * f * (self.k1 + 1) / (
                    f + self.k1 * (1 - self.b + self.b * len(self.toks[i]) / self.avg_len))
            if score > 0:
                hits.append((d["id"], score))
        return sorted(hits, key=lambda h: -h[1])


_chunks, _bm25 = {}, None


def build_bm25():
    """Book ke saare chunks Chroma se leke BM25 index banata hai (hub start hote hi, ek baar)."""
    global _chunks, _bm25
    if tutor.col is None:
        return
    data = tutor.col.get(include=["documents", "metadatas"])
    _chunks = {i: (d, m) for i, d, m in zip(data["ids"], data["documents"], data["metadatas"])}
    _bm25 = BM25([{"id": i, "text": d} for i, (d, m) in _chunks.items()])


build_bm25()

def retrieve(question: str, n: int = 4):
    if tutor.col is None:
        return [], []
    qe = tutor.embedder.encode("Represent this sentence for searching relevant passages: " + question,
                               normalize_embeddings=True)
    r = tutor.col.query(query_embeddings=[qe.tolist()], n_results=n)
    docs, metas = r["documents"][0], r["metadatas"][0]
    sources = []
    for m in metas:
        s = f"{m['book']} page {m['page']}"
        if s not in sources:
            sources.append(s)
    return docs, sources


# ------------------------------------------------------------------ /health
@app.get("/health")
def health():
    """The phone's Capability Resolver reads this to choose: hub AI, phone 1B model, or rules."""
    up = ollama_ok()
    models = []
    if up:
        resp = llm.list()
        items = resp.get("models", []) if isinstance(resp, dict) else resp.models
        models = [(m.get("model") or m.get("name")) if isinstance(m, dict) else m.model for m in items]
    free_ram_mb = None
    try:
        import psutil
        free_ram_mb = round(psutil.virtual_memory().available / 1e6)
    except Exception:
        pass
    return {
        "hub": "ok",
        "ollama": up,
        "model": MODEL,
        "model_loaded": any(m == MODEL or m.startswith(MODEL + "-") for m in models),
        "book_index": tutor.col is not None,
        "book_chunks": tutor.col.count() if tutor.col is not None else 0,
        "concepts": len(tutor.G),
        "free_ram_mb": free_ram_mb,
        "stt": stt.available(),
        "token_required": bool(HUB_TOKEN),
    }


# ------------------------------------------------------------------ /stt
MAX_UPLOAD_MB = 10


@app.post("/stt")
async def speech_to_text(audio: UploadFile = File(..., description="recording: webm, ogg, m4a, mp3 or wav"),
                         x_hub_token: Optional[str] = Header(None)):
    """Student's voice -> text in Odia script + Roman script. The student can edit it before sending."""
    check_token(x_hub_token)
    if not stt.available():
        raise HTTPException(503, "Speech model not downloaded. Run: python stt.py --download")
    data = await audio.read()
    if len(data) > MAX_UPLOAD_MB * 1_000_000:
        raise HTTPException(413, f"Recording too big (max {MAX_UPLOAD_MB} MB)")
    try:
        return stt.transcribe(data)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(400, f"Could not read this audio: {e}")


# ------------------------------------------------------------------ /brain
class BrainRequest(BaseModel):
    job: Literal["find_topic", "check", "simplify", "answer"]
    text: Optional[str] = Field(None, description="find_topic: the student's doubt")
    concept_id: Optional[str] = Field(None, description="check / simplify: e.g. 'dna_replication'")
    kind: Literal["probe", "check"] = Field("check", description="check: which question was asked")
    answer: Optional[str] = Field(None, description="check: the student's answer")
    question: Optional[str] = Field(None, description="answer: a free doubt for the books")
    history: list[list[str]] = Field(default_factory=list,
                                     description="answer: last turns as [[student, tutor], ...]")


@app.post("/brain")
def brain(req: BrainRequest, x_hub_token: Optional[str] = Header(None)):
    """One endpoint, four small jobs. Every reply says which brain answered (Glass Box)."""
    check_token(x_hub_token)
    t0 = time.time()
    out = {"job": req.job}

    if req.job == "find_topic":
        if not req.text:
            raise HTTPException(422, "find_topic needs 'text'")
        cid = tutor.find_topic(req.text)               # your alias matcher - no AI needed
        out.update(concept_id=cid, title=tutor.G[cid]["title"] if cid else None, brain="rules")

    elif req.job == "check":
        if not (req.concept_id and req.answer is not None):
            raise HTTPException(422, "check needs 'concept_id' and 'answer'")
        c = concept(req.concept_id)
        q, expected = (c["probe_q"], c["probe_a"]) if req.kind == "probe" else (c["check_q"], c["check_a"])
        verdict, used = None, "rules"
        if req.answer.strip().lower() in ("", "idk", "i dont know", "i don't know", "pata nahi", "nahi pata", "?"):
            verdict = "wrong"
        elif ollama_ok():
            try:
                raw = ask_llm(
                    "You are marking a school student's answer. Be lenient about spelling, grammar and language "
                    "(English or Hinglish). Accept the same idea even if worded differently.\n\n"
                    f"Question: {q}\nExpected key idea: {expected}\nStudent answer: {req.answer}\n\n"
                    "Reply with exactly one word: CORRECT, PARTIAL or WRONG.").upper()
                verdict = ("wrong" if "WRONG" in raw else "partial" if "PARTIAL" in raw
                           else "correct" if "CORRECT" in raw else None)
                used = f"hub-{MODEL}" if verdict else "rules"
            except Exception:
                verdict = None
        if verdict is None:
            verdict, used = rules_verdict(expected, req.answer), "rules"
        out.update(concept_id=req.concept_id, verdict=verdict, expected=expected, brain=used)

    elif req.job == "simplify":
        if not req.concept_id:
            raise HTTPException(422, "simplify needs 'concept_id'")
        c = concept(req.concept_id)
        text, used = c["explain"], "rules"            # fallback: the verified lesson itself
        if ollama_ok():
            try:
                text = ask_llm("Explain the following facts to a school student in 3 short, very simple "
                               "sentences. Use ONLY these facts. Do not add any new facts or examples.\n\n"
                               f"Facts: {c['explain']}")
                used = f"hub-{MODEL}"
            except Exception:
                pass
        out.update(concept_id=req.concept_id, text=text, brain=used)

    elif req.job == "answer":
        if not req.question:
            raise HTTPException(422, "answer needs 'question'")
        out.update(answer_from_books(req.question, req.history))

    out["ms"] = round((time.time() - t0) * 1000)
    return out


def answer_from_books(question: str, history: list) -> dict:
    """The ask.py logic: follow-up rewrite -> book search -> grounded answer (English)."""
    hist = history[-3:]
    convo = "\n".join(f"Student: {a}\nTutor: {b}" for a, b in hist)
    sq, used = question, "rules"
    ai = ollama_ok()
    if ai and hist:                                # same follow-up rewrite as ask.py
        try:
            sq = ask_llm(
                "Below is a conversation between a student and a biology tutor, then a new student message. "
                "If the new message depends on the earlier conversation (for example it says 'why', "
                "'explain more', 'it', 'that', 'give an example'), rewrite it as ONE complete standalone "
                "question. If it is already complete, repeat it unchanged. Output ONLY the question.\n\n"
                f"Conversation:\n{convo}\n\nNew message: {question}\n\nStandalone question:"
            ).split("\n")[0].strip().strip('"') or question
        except Exception:
            pass
    docs, sources = retrieve(sq)
    if not docs:
        answer = NOT_IN_BOOKS
    elif ai:
        try:
            answer = ask_llm(
                "You are a careful biology tutor for school students. "
                "Use ONLY facts written in the context below. Do not add any outside facts. "
                "Answer in 3 to 4 short, simple sentences. If the context does not contain the answer, "
                f"reply exactly: '{NOT_IN_BOOKS}'\n\n"
                f"Context:\n" + "\n\n".join(docs) + f"\n\nQuestion: {sq}")
            used = f"hub-{MODEL}"
        except Exception:
            answer = None
        if not answer:
            answer, used = "AI is busy right now. Read these book pages:", "rules"
    else:
        answer = "AI is off right now. Read these book pages:"
    if answer.startswith(NOT_IN_BOOKS.rstrip(".")):
        sources = []
    return {"standalone_question": sq, "answer": answer, "sources": sources, "brain": used}


# ------------------------------------------------------------------ /ask  (voice/Odia question -> Odia answer)
NOT_IN_BOOKS = "This is not in my books."
ODIA_RANGE = re.compile(r"[଀-୿]")
NOT_IN_BOOKS_ODIA = "ଏହା ମୋ ବହିରେ ନାହିଁ।"


def has_odia(s: str) -> bool:
    return bool(ODIA_RANGE.search(s or ""))


def odia_to_english(text: str) -> str:
    return ask_llm(
        "Translate this school student's question from Odia (it may be Sambalpuri dialect) into simple English. "
        "Keep science words like DNA, RNA, gene, enzyme as they are. "
        "Output ONLY the English question, nothing else.\n\n"
        f"Odia: {text}\n\nEnglish:", model=TRANSLATE_MODEL).split("\n")[0].strip().strip('"')


def english_to_odia(text: str, dialect: str) -> str:
    style = ("simple spoken Odia, the way a friendly village teacher talks to a Class 12 student"
             if dialect == "odia" else
             "Sambalpuri (Western Odisha dialect), written in Odia script. If you are not sure of a "
             "Sambalpuri word, use the simple Odia word")
    return ask_llm(
        f"Rewrite this biology explanation in {style}. Keep science words like DNA, RNA, gene, enzyme, "
        "replication in English letters. Do not add or remove any facts. Output ONLY the rewritten text.\n\n"
        f"English: {text}\n\nRewritten:", model=TRANSLATE_MODEL).strip()


class AskRequest(BaseModel):
    text: str = Field(..., description="the student's question: Odia script (from /stt), Roman or English")
    history: list[list[str]] = Field(default_factory=list,
                                     description="earlier turns in English as [[question, answer], ...]")
    answer_in: Literal["odia", "sambalpuri_experimental", "english"] = "odia"


@app.post("/ask")
def ask(req: AskRequest, x_hub_token: Optional[str] = Header(None)):
    """Full voice flow: student's (edited) transcript -> English -> book answer -> Odia + Roman.
    Every step reports which brain did it (Glass Box)."""
    check_token(x_hub_token)
    t0 = time.time()
    text = req.text.strip()
    if not text:
        raise HTTPException(422, "Empty question")
    trace = []
    ai = ollama_ok()

    # 1. Odia -> English (the books and the embedder are English)
    question_en = text
    if has_odia(text):
        if not ai:
            return {"question": text, "answer": "AI is off right now. Please type your question in English.",
                    "answer_roman": "", "sources": [], "trace": ["translate: rules (AI off)"],
                    "ms": round((time.time() - t0) * 1000)}
        try:
            question_en = odia_to_english(text) or text
            trace.append(f"translate question: hub-{TRANSLATE_MODEL}")
        except Exception as e:
            raise HTTPException(504, f"Translation timed out or failed: {e}")

    # 2. Which lesson is this? (your tutor.py matcher - lets the app open the full lesson)
    cid = tutor.find_topic(question_en)

    # 3. Answer from the books (ask.py logic, English)
    res = answer_from_books(question_en, req.history)
    trace.append(f"answer: {res['brain']}")
    answer_en = res["answer"]

    # 4. English -> Odia / Sambalpuri
    answer = answer_en
    if req.answer_in != "english":
        if answer_en == NOT_IN_BOOKS:
            answer = NOT_IN_BOOKS_ODIA
        elif res["brain"] != "rules":
            try:
                answer = english_to_odia(answer_en, "odia" if req.answer_in == "odia" else "sambalpuri")
                trace.append(f"translate answer: hub-{TRANSLATE_MODEL}")
            except Exception:
                trace.append("translate answer: failed, showing English")

    roman = ""
    if has_odia(answer):
        try:
            roman = stt.to_roman(answer)
        except Exception:
            pass

    return {
        "question": text,
        "question_english": question_en,
        "concept_id": cid,
        "concept_title": tutor.G[cid]["title"] if cid else None,
        "answer": answer,
        "answer_roman": roman,
        "answer_english": answer_en,
        "answer_in": req.answer_in,
        "sources": res["sources"],
        "trace": trace,
        "ms": round((time.time() - t0) * 1000),
    }
