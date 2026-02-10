import json
import numpy as np
from pathlib import Path
from tqdm import tqdm
from PIL import Image
import pytesseract

from src.embeddings.clip_embedder import CLIPEmbedder

# FIXED PATH — YOUR REAL IMAGE LOCATION
IMAGE_DIR = Path(
    "src/data/raw/archive (1)/EnterpriseRAG_2025_02_markdown"
)

OUT_DIR = Path("src/data/embeddings")
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_EMB_FILE = OUT_DIR / "clip_image_embeddings.npy"
META_FILE = OUT_DIR / "clip_metadata.jsonl"


class ImageIngestor:
    def __init__(self):
        self.clip = CLIPEmbedder()

    def ingest(self):
        images = (
            list(IMAGE_DIR.rglob("*.jpg")) +
            list(IMAGE_DIR.rglob("*.jpeg")) +
            list(IMAGE_DIR.rglob("*.png"))
        )

        if not images:
            raise RuntimeError(f"No images found under {IMAGE_DIR}")

        image_embeddings = []

        with open(META_FILE, "w", encoding="utf-8") as meta_out:
            for img_path in tqdm(images, desc="Processing images"):
                print(f"🖼 {img_path}")

                # OCR
                try:
                    ocr_text = pytesseract.image_to_string(
                        Image.open(img_path)
                    ).strip()
                except Exception:
                    ocr_text = ""

                # CLIP embedding
                emb = self.clip.embed_image(str(img_path))
                image_embeddings.append(emb)

                meta_out.write(json.dumps({
                    "image_path": str(img_path),
                    "ocr_text": ocr_text
                }, ensure_ascii=False) + "\n")

        image_embeddings = np.array(image_embeddings, dtype="float32")
        np.save(IMAGE_EMB_FILE, image_embeddings)

        print("\nIMAGE INGEST COMPLETE")
        print(f"Embeddings → {IMAGE_EMB_FILE}")
        print(f"Metadata   → {META_FILE}")


if __name__ == "__main__":
    ImageIngestor().ingest()
