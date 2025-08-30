# scripts/splits.py
import argparse, os, csv, random
random.seed(13)

LABELS = ["FAVOR", "AGAINST", "NONE"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="CSV path to write demo ids+labels")
    ap.add_argument("--n", type=int, default=5, help="How many demo rows")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tweet_id", "target", "label"])
        for i in range(args.n):
            tid = str(10_000 + i)          # fake IDs: 10000, 10001, ...
            target = f"TGT_{i % 2}"        # two fake targets: TGT_0, TGT_1
            label = random.choice(LABELS)  # random label
            w.writerow([tid, target, label])
    print(f"[splits] wrote demo CSV with {args.n} rows to {args.out}")

if __name__ == "__main__":
    main()
