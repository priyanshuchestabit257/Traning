import json
import numpy as np
from pathlib import Path
import torch
import open_clip
from PIL import Image


EMB_DIR = Path("src/data/embeddings")

IMAGE_EMB_FILE = EMB_DIR / "clip_image_embeddings.npy"
META_FILE = Path("src/data/embeddings/clip_metadata.jsonl")



image_embeddings = np.load(IMAGE_EMB_FILE)

image_paths = []
metadata = {}

with open(META_FILE, "r", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        image_paths.append(r["image_path"])
        metadata[r["image_path"]] = r

print(f"Loaded {len(image_paths)} images")


device = "cuda" if torch.cuda.is_available() else "cpu"

model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="openai"
)
tokenizer = open_clip.get_tokenizer("ViT-B-32")

model = model.to(device)
model.eval()


def normalize(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)

#
def text_to_image(query, top_k=5):
    with torch.no_grad():
        tokens = tokenizer([query]).to(device)
        text_feat = model.encode_text(tokens)
        text_feat = text_feat / text_feat.norm(dim=-1, keepdim=True)

    scores = image_embeddings @ text_feat.cpu().numpy().T
    scores = scores.squeeze()

    top_idx = np.argsort(scores)[::-1][:top_k]

    return top_idx, scores


def image_to_image(image_path, top_k=5):
    image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)

    with torch.no_grad():
        img_feat = model.encode_image(image)
        img_feat = img_feat / img_feat.norm(dim=-1, keepdim=True)

    scores = image_embeddings @ img_feat.cpu().numpy().T
    scores = scores.squeeze()

    top_idx = np.argsort(scores)[::-1][:top_k]

    return top_idx, scores


def image_to_text_answer(image_path):
    meta = metadata.get(image_path)

    if not meta:
        return "No metadata found."

    answer = f"""
 Image: {image_path}

 Caption:
{meta.get("caption", "N/A")}

 OCR Extract:
{meta.get("ocr_text", "N/A")}
"""
    return answer.strip()


if __name__ == "__main__":
    print(
        "\nModes:\n"
        "1 → Text → Image\n"
        "2 → Image → Image\n"
        "3 → Image → Text Answer\n"
        "exit → Quit"
    )

    while True:
        mode = input("\nSelect mode: ").strip()

        if mode == "exit":
            break

        if mode == "1":
            q = input("🔍 Text query: ")
            idxs, scores = text_to_image(q)

        elif mode == "2":
            img = input("🖼 Image path: ")
            idxs, scores = image_to_image(img)

        elif mode == "3":
            img = input("🖼 Image path: ")
            print(image_to_text_answer(img))
            continue

        else:
            print(" Invalid mode")
            continue

        for i in idxs:
            path = image_paths[i]
            meta = metadata[path]

            print("\nImage:", path)
            print("Score:", round(float(scores[i]), 4))
            print("Caption:", meta.get("caption", "N/A"))
            print("OCR:", meta.get("ocr_text", "")[:300], "...")
