import argparse, os
os.environ.setdefault("TOKENIZERS_PARALLELISM","false")
import torch, torch.nn as nn
from src.dataio import DemoDataset
from src.models import TinyBaseline

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", default="data/tables/demo.parquet")
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()

    ds = DemoDataset(args.table)
    assert len(ds) >= 2, "Need at least 2 rows in demo table"
    batch = [ds[i] for i in range(2)]
    texts = [b["text"] for b in batch]
    imgs  = [b["image"] for b in batch]
    labels_map = {"FAVOR":0, "AGAINST":1, "NONE":2}
    labels = torch.tensor([labels_map[b["label"]] for b in batch], dtype=torch.long)

    model = TinyBaseline(num_labels=3)
    optim = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=1e-3)
    crit  = nn.CrossEntropyLoss()

    model.train()
    optim.zero_grad()
    logits = model(texts, imgs)
    loss = crit(logits, labels)
    loss.backward()
    optim.step()
    print(f"[train] Smoke OK. Loss={loss.item():.4f}")

if __name__ == "__main__":
    main()
