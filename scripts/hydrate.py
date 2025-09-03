import argparse, json, csv, os, random
random.seed(13)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="CSV with columns: tweet_id,target,label")
    ap.add_argument("--out", required=True, help="Output JSONL (fake hydrated)")
    ap.add_argument("--dry-run", action="store_true", help="Generate fake hydration (no API)")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    n, keep = 0, 0
    with open(args.ids, newline="", encoding="utf-8") as f_in, open(args.out, "w", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        for row in reader:
            n += 1
            tid = str(row["tweet_id"])
            target = row["target"]
            if args.dry_run:
                txt = f"Demo tweet about {target}. This is sample #{n}."
                obj = {
                    "data": [{"id": tid, "text": txt, "attachments": {"media_keys": ["m1"]}}],
                    "includes": {"media": [{"media_key": "m1", "type": "photo", "url": "PLACEHOLDER"}]}
                }
                f_out.write(json.dumps(obj, ensure_ascii=False) + "\n")
                keep += 1
            else:
                raise SystemExit("This smoke script only supports --dry-run for now.")
    print(f"[hydrate] wrote {keep}/{n} hydrated lines to {args.out}")

if __name__ == "__main__":
    main()
