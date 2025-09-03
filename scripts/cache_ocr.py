import argparse, os, pandas as pd, pytesseract
from PIL import Image

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True, help="Parquet table with image_path and tweet_id")
    ap.add_argument("--out", required=True, help="Parquet path to write OCR cache")
    args = ap.parse_args()

    df = pd.read_parquet(args.table)
    rows = []
    for _, r in df.iterrows():
        path = r["image_path"]
        try:
            txt = pytesseract.image_to_string(Image.open(path))
        except Exception:
            txt = ""
        rows.append({"tweet_id": r["tweet_id"], "ocr_text": txt})
    out = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    out.to_parquet(args.out, index=False)
    print(f"[ocr] cached OCR for {len(out)} images \u2192 {args.out}")

if __name__ == "__main__":
    main()
