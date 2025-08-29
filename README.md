# mini-senior (TMPT baseline + OCR + M²PT-inspired A/B)

Goal: reproduce study1 baseline, then add:
- OCR branch
- Option A (multi-layer visual prompts + projector + late fusion)
- Option B (visual prompts + reducer → pseudo-visual tokens into frozen BERT)

Folders:
- data/ (gitignored): raw IDs, hydrated JSONL, images, tables, OCR cache
- scripts/: hydrate IDs, download media, cache OCR, build splits
- src/: dataset, models, training, eval
- configs/: data & train/eval configs
- runs/ (gitignored): checkpoints, metrics
