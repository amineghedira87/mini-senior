import argparse, os, json, pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--hydrated", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    lab = pd.read_csv(args.labels)
    texts, paths = {}, {}

    with open(args.hydrated, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            d = obj["data"][0]
            tid = str(d["id"])
            texts[tid] = d.get("text", "")
            mkeys = d.get("attachments", {}).get("media_keys", [])
            if mkeys:
                paths[tid] = f"data/images/{tid}_{mkeys[0]}.jpg"

    rows = []
    for _, r in lab.iterrows():
        tid = str(r["tweet_id"])
        if tid in texts and tid in paths:
            rows.append({
                "tweet_id": tid,
                "target": r["target"],
                "label": r["label"],
                "text": texts[tid],
                "image_path": paths[tid],
                "split": "train"
            })
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_parquet(args.out, index=False)
    print(f"[table] wrote {len(df)} rows -> {args.out}")

if __name__ == "__main__":
    main()
