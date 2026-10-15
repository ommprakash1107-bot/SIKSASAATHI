"""
Add an NCERT chapter PDF into the team's existing database (index / books),
using the same bge-small-local model that ask.py uses.

Usage:
    python add_chapter.py "lebo104.pdf" "Principles of Inheritance and Variation"
"""
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import sys
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

CHUNK_SIZE = 1000
OVERLAP = 200


def split_into_chunks(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def main():
    if len(sys.argv) < 3:
        print('Usage: python add_chapter.py "file.pdf" "Chapter name"')
        sys.exit(1)
    pdf_path, chapter_name = sys.argv[1], sys.argv[2]

    base = os.path.dirname(os.path.abspath(__file__))
    embedder = SentenceTransformer(os.path.join(base, "bge-small-local"), device="cpu")
    col = chromadb.PersistentClient(path=os.path.join(base, "index")).get_or_create_collection("books")

    reader = PdfReader(pdf_path)
    documents, metadatas, ids = [], [], []
    for page_num, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue
        for i, chunk in enumerate(split_into_chunks(text)):
            documents.append(chunk)
            metadatas.append({"book": chapter_name, "page": page_num})
            ids.append(f"{chapter_name}-p{page_num}-{i}")

    if not documents:
        print("No text found. The PDF may be a scanned image.")
        sys.exit(1)

    # Same model as ask.py (documents are embedded without the query prefix)
    embeddings = embedder.encode(documents, normalize_embeddings=True,
                                 show_progress_bar=True).tolist()

    col.upsert(documents=documents, embeddings=embeddings,
               metadatas=metadatas, ids=ids)
    print(f"Added {len(documents)} chunks from '{chapter_name}'.")
    print(f"Total chunks in index/books: {col.count()}")


if __name__ == "__main__":
    main()


    