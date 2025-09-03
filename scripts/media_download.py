import argparse, json, os
from PIL import Image, ImageDraw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hydrated", required=True, help="JSONL from hydrate.py")
    ap.add_argument("--outdir", required=True, help="Folder to write images")
    ap.add_argument("--dry-run", action="store_true", help="Create placeholder images")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    made = 0
    with open(args.hydrated, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            data = obj["data"][0]
            tid = str(data["id"])
            media_keys = data.get("attachments", {}).get("media_keys", [])
            for k in media_keys:
                out = os.path.join(args.outdir, f"{tid}_{k}.jpg")
                if args.dry_run:
                    img = Image.new("RGB", (224, 224), "white")
                    d = ImageDraw.Draw(img)
                    d.rectangle([20, 20, 204, 204], outline="black", width=3)
                    d.text((26, 26), f"{tid}", fill="black")
                    img.save(out, "JPEG")
                    made += 1
                else:
                    raise SystemExit("This smoke script only supports --dry-run for now.")
    print(f"[media] created {made} placeholder image(s) in {args.outdir}")

if __name__ == "__main__":
    main()
