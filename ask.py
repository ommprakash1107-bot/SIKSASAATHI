import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import chromadb, ollama
from sentence_transformers import SentenceTransformer

MODEL = "qwen2.5:3b"   # Gemma test ke baad yahan "gemma4:e2b" likh sakte hain

base = os.path.dirname(os.path.abspath(__file__))
embedder = SentenceTransformer(os.path.join(base, "bge-small-local"), device="cpu")
col = chromadb.PersistentClient(path=os.path.join(base, "index")).get_collection("books")

history = []   # (student question, tutor answer) pairs


def ask_llm(prompt):
    r = ollama.chat(model=MODEL, options={"temperature": 0},
                    messages=[{"role": "user", "content": prompt}])
    return r["message"]["content"].strip()


def convo_text(n):
    return "\n".join(f"Student: {a}\nTutor: {b}" for a, b in history[-n:])


def rewrite(q):
    # Follow-up (cross) question ko poora, akela sawal bana deta hai
    if not history:
        return q
    p = ("Below is a conversation between a student and a biology tutor, "
         "then a new student message. If the new message depends on the earlier "
         "conversation (for example it says 'why', 'explain more', 'it', 'that', "
         "'give an example'), rewrite it as ONE complete standalone question. "
         "If it is already complete, repeat it unchanged. Output ONLY the question.\n\n"
         f"Conversation:\n{convo_text(3)}\n\nNew message: {q}\n\nStandalone question:")
    out = ask_llm(p).split("\n")[0].strip().strip('"')
    return out or q


print("Taiyaar hoon! Sawal poochiye.")
print("(Naya topic shuru karne ke liye: reset | Band karne ke liye: exit)")
while True:
    q = input("\nSawal: ").strip()
    if q.lower() in ("exit", "quit", ""):
        break
    if q.lower() == "reset":
        history.clear()
        print("Baatcheet saaf kar di. Naya topic poochiye.")
        continue

    sq = rewrite(q)
    if sq != q:
        print(f"(Maine aapka sawal aise samjha: {sq})")

    qe = embedder.encode("Represent this sentence for searching relevant passages: " + sq,
                         normalize_embeddings=True)
    r = col.query(query_embeddings=[qe.tolist()], n_results=4)
    docs, metas = r["documents"][0], r["metadatas"][0]
    ctx = "\n\n".join(docs)

    prompt = ("You are a careful biology tutor for school students. "
              "Use ONLY facts written in the context below. Do not add any outside facts. "
              "The earlier conversation is only to help you understand what the student means. "
              "Answer in 3 to 4 short, simple sentences. "
              "If the context does not contain the answer, reply exactly: "
              "'This is not in my books.'\n\n"
              f"Earlier conversation:\n{convo_text(2) or '(none)'}\n\n"
              f"Context:\n{ctx}\n\nQuestion: {sq}")

    print("\nJawab: ", end="", flush=True)
    parts = []
    for part in ollama.chat(model=MODEL, stream=True, options={"temperature": 0},
                            messages=[{"role": "user", "content": prompt}]):
        t = part["message"]["content"]
        parts.append(t)
        print(t, end="", flush=True)
    print()
    ans = "".join(parts).strip()

    if ans.startswith("This is not in my books"):
        continue

    seen = []
    for m in metas:
        s = f"{m['book']} page {m['page']}"
        if s not in seen:
            seen.append(s)
    print("\nSources:", "; ".join(seen))
    history.append((q, ans[:500]))
