import io
import re

import pdfplumber
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI(title="PDF Text Extractor")


def _clean(text: str) -> str:
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract")
async def extract(
    file: UploadFile = File(...),
    mode: str = "pages",
    clean: bool = False,
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    if mode not in ("pages", "full"):
        raise HTTPException(status_code=400, detail="mode must be 'pages' or 'full'.")

    contents = await file.read()
    pages_text: list[str] = []

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        total = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text(layout=True) or ""
            if clean:
                text = _clean(text)
            pages_text.append(text)

    if mode == "pages":
        return JSONResponse({
            "total_pages": total,
            "pages": [{"page": i + 1, "text": t} for i, t in enumerate(pages_text)],
        })

    return JSONResponse({
        "total_pages": total,
        "text": " ".join(pages_text) if clean else "\n\n".join(pages_text),
    })
